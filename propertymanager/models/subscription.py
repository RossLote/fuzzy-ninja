from django.db import models
from django.conf import settings
from .address import Address
from sagepay.models import CardAddress, Card

# Create your models here.

class SubscriptionModel(models.Model):
    ZERO_MONTH =    0
    ONE_MONTH =     1
    TWO_MONTH =     2
    THREE_MONTH =   3
    FOUR_MONTH =    4
    FIVE_MONTH =    5
    SIX_MONTH =     6
    PERIODS = (
        (ZERO_MONTH,    'none'),
        (ONE_MONTH,     'one month'),
        (TWO_MONTH,     'two months'),
        (THREE_MONTH,   'three months'),
        (FOUR_MONTH,    'four months'),
        (FIVE_MONTH,    'five months'),
        (SIX_MONTH,     'six months'),
    )
    price =             models.DecimalField(decimal_places=2)
    trial_period =      models.PositiveSmallIntegerField(choices=PERIODS, default=ZERO_MONTH)
    minimum_term =      models.PositiveSmallIntegerField(choices=PERIODS, default=ZERO_MONTH)
    repeat_interval =   models.PositiveSmallIntegerField(choices=PERIODS, default=ONE_MONTH)
    
    
class Subscription(models.Model):
    CARD =      1
    PAYMENT_METHODS = (
        (CARD,    'card'),
    )
    payment_method =    models.PositiveSmallIntegerField(choices=PAYMENT_METHODS, default=CARD)
    payment_card =      models.ForeignKey(Card)
    repeat_interval =   models.PositiveSmallIntegerField(choices=SubscriptionModel.PERIODS)
    trial_period =      models.PositiveSmallIntegerField(choices=SubscriptionModel.PERIODS)
    minimum_term =      models.PositiveSmallIntegerField(choices=SubscriptionModel.PERIODS)
    next_payment_due =  models.DateField()
    amount =            models.DecimalField(decimal_places=2)
    billing_address =   models.ForeignKey(Address)