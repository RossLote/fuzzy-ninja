from __future__ import absolute_import

from base64 import b32encode
import hashlib
import uuid
import sys
import calendar
import datetime

from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy

import requests
from requests.exceptions import RequestException
from jsonfield import JSONField

from .utils import (format_money_value, encode_transaction_request,
    decode_transaction_response, truncate_overlong_fields)

User = get_user_model()

VPS_PROTOCOL = '2.23'

# SagePay uses the MD5 hash of these fields to create the request signature
HASH_FIELDS = ('VPSTxId', 'VendorTxCode', 'Status', 'TxAuthNo', 'Vendor',
    'AVSCV2', 'SecurityKey', 'AddressResult', 'PostCodeResult', 'CV2Result',
    'GiftAid', '3DSecureStatus', 'CAVV', 'AddressStatus', 'PayerStatus',
    'CardType', 'Last4Digits')


class SagePayError(Exception):
    status = None


class SagePayTransaction(models.Model):
    # This is the unique string (supplied by us) which SagePay will use to
    # identify our transaction
    vendor_tx_id = models.CharField(unique=True, max_length=40)

    date_created = models.DateTimeField(auto_now_add=True)

    # The data sent to SagePay in order to create the transaction
    request = JSONField()
    # SagePay's response
    response = JSONField()
    # Any additional data which you would like to store on the transaction but
    # doesn't form part of the data to be sent to SagePay
    extra_data = JSONField()

    # The time at which we received notification from SagePay that the
    # transaction has completed
    notification_date = models.DateTimeField(null=True)
    # The transaction status data
    notification_data = JSONField(null=True)
    # The data we sent back to SagePay to acknowledge reciept of the
    # transaction
    acknowledgement_data = JSONField(null=True)

    def is_valid_signature(self, notification_data):
        md5 = hashlib.md5()
        for f in HASH_FIELDS:
            if f == 'Vendor':
                value = self.request.get(f, '')
            elif f == 'SecurityKey':
                value = self.response.get(f, '')
            else:
                value = notification_data.get(f, '')
            md5.update(value)
        signature = md5.hexdigest().upper()
        return signature == notification_data.get('VPSSignature')


def start_transaction(transaction_data, extra_data={}, request=None,
                       url_base=None):
    # Default transaction parameters
    data = {
        'VPSProtocol': VPS_PROTOCOL,
        'TxType': 'PAYMENT',
        # Generate a new transaction ID
        'VendorTxCode': b32encode(uuid.uuid4().bytes).strip('=').lower()
    }
    # Add defaults from settings, if defined
    data.update(getattr(settings, 'SAGEPAY_DEFAULTS', {}))
    # Add user supplied data
    data.update(transaction_data)
    # Ensure all URLs are absolute
    data['NotificationURL'] = ensure_absolute_url(data['NotificationURL'],
            request=request, url_base=url_base)
    for key in ['success_url', 'failure_url']:
        if key in extra_data:
            extra_data[key] = ensure_absolute_url(extra_data[key],
                 request=request, url_base=url_base)

    # Truncate any (non-essential) fields that exceed SagePay's limits; it's
    # better to lose a bit of descriptive data than bork the whole transaction
    data = truncate_overlong_fields(data)
    request_body = encode_transaction_request(data)

    try:
        # Fire request to SagePay which creates the transaction
        response = requests.post(settings.PAYMENT_URL, data=request_body,
                                 prefetch=True, verify=True)
        # Does nothing on 200, but raises exceptions for other statuses
        response.raise_for_status()
    # RequestException covers network/DNS related problems as well as non-200
    # responses
    except RequestException as e:
        raise SagePayError(repr(e)), None, sys.exc_info()[2]

    response_data = decode_transaction_response(response.text)

    # Anything other than a status of OK throws an exception (Note that SagePay
    # can return the status 'OK REPEATED' if the VendorTxCode refers to an in-
    # progress transaction, but because we generate unique IDs every time we
    # hit SagePay we should never get this -- if we do, it's an error)
    if response_data['Status'] != 'OK':
        exc = SagePayError(response_data['StatusDetail'])
        exc.status = response_data['Status']
        raise exc

    # If all went well, save the transaction object and return the URL to
    # redirect the user to
    tx = SagePayTransaction.objects.create(
        vendor_tx_id=data['VendorTxCode'],
        request=data,
        response=response_data,
        extra_data=extra_data
    )
    # Return the URL to which to redirect the user
    return tx


def ensure_absolute_url(url, request=None, url_base=None):
    if not url.startswith('http://') and not url.startswith('https://'):
        if not url_base:
            if not request:
                raise SagePayError('No url_base or request supplied: cannot '
                                   'construct absolute URL')
            url = request.build_absolute_uri(url)
        else:
            url = '{0}{1}'.format(url_base.rstrip('/'), url)
    # Cast to string in case we've been supplied with a lazily reversed
    # URL object
    return unicode(url)

class CardAddress(object):
    def __init__(self,
                 surname,
                 firstnames,
                 street,
                 city,
                 state,
                 country,
                 house_number=None,
                 flat_number=None,
                 house_name=None,
                 postcode=None
                 ):
        
        self.firstnames = firstnames
        self.surname = surname
        self.address_1 = get_first_line(street, house_name, house_number, flat_number)
        self.country = country
        self.city = city
        self.postcode = postcode if postcode else '000'
        self.state = state[:2]
    
    def get_first_line(self, street, house_name, house_number, flat_number):
        if house_name:
            part_1 = '{0},'.format(house_name)
        else:
            part_1 = house_number
            if flat_number:
                part_1 = 'Flat {0}, {1}'.format(flat_number, part_1)
            
        return '{0} {1}'.format(part_1, street)
    
    def format_for_sagepay(self, prefix=''):
        return {
            prefix + 'Firstnames' : self.firstnames,
            prefix + 'Surname' : self.surname,
            prefix + 'Address1' : self.address_1,
            prefix + 'City' : self.city,
            prefix + 'Country' : self.country,
            prefix + 'Postcode' : self.postcode
        }
    

class CardManager(models.Manager):
    def create_card(self, card_holder, card_number, start_month, start_year,
         expiry_month, expiry_year, cv2, card_type, user=None):

        # Start date
        if start_month:
            start_date = datetime.date(start_year, start_month, 1)
        else:
            start_date = None

        # Expiry date
        last_day = calendar.monthrange(expiry_year, expiry_month)[1]
        expiry_date = datetime.date(expiry_year, expiry_month, last_day)

        # Check card_holder doesn't exceed SagePay maximum
        if len(card_holder) > 50:
            card_holder = card_holder[:50]

        # Store card at SagePay
        raw_params = {
            'VPSProtocol': '2.23',
            'TxType': 'TOKEN',
            'Vendor': settings.VENDOR,
            'Currency': settings.CURRENCY,
            'CardHolder': card_holder.encode('utf8'),
            'CardNumber': card_number,
            'ExpiryDate': expiry_date.strftime('%m%y'),
            'CV2': cv2,
            'CardType': card_type
        }
        if start_date:
            raw_params['StartDate'] = start_date.strftime('%m%y')

        params = urllib.urlencode(raw_params)
        request = urllib2.Request(settings.REGISTER_URL, params)
        try:
            response = urllib2.urlopen(request)
        except urllib2.URLError:
            logger.error('Network failed connecting to card processor.')
            return 'Network failed connecting to card processor.'

        for line in response.readlines():
            if line.startswith('Status='):
                status = line[7:].strip()
            if line.startswith('StatusDetail='):
                status_detail = line[13:].strip()
            if line.startswith('Token='):
                token = line[6:].strip()

        if status != 'OK':
            logger.error('%s failed to store %s ending %s %s "%s"' % (
                card_holder, card_type, card_number[-4:], status, status_detail
            ))
            if status_detail.startswith('4022'):
                return _('The Card Type selected does not match card number.')
            else:
                return _(
                    'There is something wrong with the details entered. '
                    'Please contact us for help.'
                )

        # Create Card
        card = Card(
            user=user,
            currency=settings.CURRENCY,
            card_holder=card_holder,
            card_type=card_type,
            first_four_digits=card_number[:4],
            last_four_digits=card_number[-4:],
            expiry_date=expiry_date,
            start_date=start_date,
            token=token
        )
        card.save()

        logger.info('%s stored card #%d %s ending %s' % (
            card_holder, card.id, card_type, card_number[-4:]
        ))

        return card


class Card(models.Model):
    user = models.ForeignKey(User, default=None, editable=False, null=True)
    currency = models.CharField(max_length=3, editable=False)
    card_holder = models.CharField(ugettext_lazy('Name on Card'), max_length=50)
    card_type = models.CharField(
        ugettext_lazy('Card Type'), choices=settings.CARD_TYPE, max_length=7
    )
    first_four_digits = models.CharField(editable=False, max_length=4)
    last_four_digits = models.CharField(editable=False, max_length=4)
    expiry_date = models.DateField(editable=False)
    start_date = models.DateField(editable=False, null=True)
    token = models.CharField(editable=False, max_length=38, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    objects = CardManager()

    class Meta:
        get_latest_by = 'id'

    def __unicode__(self):
        return '%s ending %s' % (
            self.get_card_type_display(), self.last_four_digits
        )

    def charge(self, amount, description, billing_address, delivery_address, customer_email, client_ip_address=None,
        repeat_payment=False, cv2=None):

        # Charge card at SagePay
        raw_params = {
            'VPSProtocol': '2.23',
            'TxType': 'PAYMENT',
            'Vendor': settings.VENDOR,
            'Amount': amount,
            'Currency': settings.CURRENCY,
            'Description': description,
            'Token': self.token,
            'StoreToken': '1',
            'CustomerEMail': customer_email
        }
        raw_params.update(billing_address.format_for_sagepay(prefix = 'Billing'))
        raw_params.update(delivery_address.format_for_sagepay(prefix = 'Delivery'))

        if client_ip_address:
            raw_params['ClientIPAddress'] = client_ip_address

        # State is compulsory for addresses in USA (2 characters)
        if billing_country == 'US':
            raw_params['BillingState'] = billing_address.state
        if delivery_country == 'US':
            raw_params['DeliveryState'] = delivery_address.state

        if repeat_payment:
            if self.card_type != 'AMEX':
                # Use Continuous Authority Account
                raw_params['AccountType'] = 'C' 

            if cv2:
                # CV2 is required for AMEX but not Visa/MasterCard
                raw_params['CV2'] = cv2
            else:
                # The CV2 field is compulsory despite what the SagePay docs say
                raw_params['CV2'] = '000'

        tx = start_transaction(raw_params)

        return tx

    def cv2_required(self):
        return self.card_type == 'AMEX'

    def expired(self):
        return datetime.date.today() > self.expiry_date

    def logo(self):
        if self.card_type in ('VISA', 'DELTA', 'UKE'):
            return 'img/visa.png'
        elif self.card_type == 'MC':
            return 'img/mastercard.png'
        elif self.card_type == 'AMEX':
            return 'img/amex.png'
        else:
            return 'img/paypal.png'

    def remove(self):
        # Remove token at SagePay
        raw_params = {
            'VPSProtocol': '2.23',
            'TxType': 'REMOVETOKEN',
            'Vendor': settings.VENDOR,
            'Token': self.token
        }

        params = urllib.urlencode(raw_params)
        request = urllib2.Request(settings.REMOVE_URL, params)
        try:
            response = urllib2.urlopen(request)
        except urllib2.URLError:
            logger.error('Network failed connecting to card processor.')
            return None

        for line in response.readlines():
            if line.startswith('Status='):
                status = line[7:].strip()
            if line.startswith('StatusDetail='):
                status_detail = line[13:].strip()

        if status == 'OK':
            logger.info('Card %d token %s removed.' % (self.id, self.token))
        else:
            logger.error('Card %d token %s failed %s "%s"' % (
                self.id, self.token, status, status_detail
            ))

