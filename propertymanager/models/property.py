from django.db import models
from django.contrib.auth.models import User
from schedule.models import Calendar
from media.models import ImageGallery
from propertymanager.models import Address, Company
from annoying.fields import AutoOneToOneField, JSONField

# Create your models here.

class PropertyManager(models.Manager):
    def create(self, *args, **kwargs):
        kwargs['gallery'] =     ImageGallery.objects.create()
        
        return super(PropertyManager, self).create(*args, **kwargs)

class Property(models.Model):
    AVAILABLE =     1
    UNAVAILABLE =   2
    MAINTAINENCE =  3
    OCCUPIED =      4
    STATUS = (
        (AVAILABLE,     'available'),
        (UNAVAILABLE,   'unavailable'),
        (MAINTAINENCE,  'maintainence'),
        (OCCUPIED,      'occupied'),
    )
    
    HOUSE =     1
    BUNGALOW =  2
    FLAT =      3
    VILLA =     4
    ROOM =      5
    TYPES = (
        (HOUSE,         'house'),
        (BUNGALOW,      'bungalow'),
        (FLAT,          'flat'),
        (VILLA,         'villa'),
        (ROOM,          'room'),
    )
    
    HOUR =              1
    DAY =               2
    WEEK =              3
    FORTNIGHT =         4
    MONTH =             5
    CALENDER_MONTH =    6
    QUARTER =           7
    SIX_MONTH =         8
    ANNUAL =            9
    PAYMENT_INTERVALS = (
        (HOUR,              'hour'),
        (DAY,               'day'),
        (WEEK,              'week'),
        (FORTNIGHT,         'fortnight'),
        (MONTH,             'month'),
        (CALENDER_MONTH,    'calender month'),
        (QUARTER,           'quarter'),
        (SIX_MONTH,         'six months'),
        (ANNUAL,            'annual'),
    )
    
    FURNISHED =         1
    PART_FURNISHED =    2
    WHITE_GOODS =       3
    UNFURNISHED =       4
    FURNISHING = (
        (FURNISHED,         'furnished'),
        (PART_FURNISHED,    'part furnished'),
        (WHITE_GOODS,       'white goods'),
        (UNFURNISHED,       'unfurnished'),
    )
    
    image_gallery =     models.ForeignKey(ImageGallery)
    company =           models.ForeignKey(Company)
    occupant =          models.ForeignKey(User, null=True, blank=True, default=None)
    
    calendar =          AutoOneToOneField(Calendar)
    address =           models.OneToOneField('Address')
    
    managers =          models.ManyToManyField(User)
    
    bathrooms =         models.PositiveSmallIntegerField(default=1)
    bedrooms =          models.PositiveSmallIntegerField(default=1)
    epc_rating =        models.PositiveSmallIntegerField(default=1)
    furnishing =        models.PositiveSmallIntegerField(choices=FURNISHING, default=UNFURNISHED)
    payment_interval =  models.PositiveSmallIntegerField(choices=PAYMENT_INTERVALS, default=MONTH)
    status =            models.PositiveSmallIntegerField(choices=STATUS, default=UNAVAILABLE)
    type =              models.PositiveSmallIntegerField(choices=TYPES, default=HOUSE)
    
    price =             models.DecimalField(max_digits=8, decimal_places=2)
    
    date_available =    models.DateField()
    date_created =      models.DateField()
    
    last_time_saved =           models.DateTimeField(auto_now=True)
    last_time_json_updated =    models.DateTimeField()
    
    disabled_access =   models.BooleanField(default=False)
    pets_allowed =      models.BooleanField(default=False)
    published =         models.BooleanField(default=False)
    smoking =           models.BooleanField(default=False)

    
    description =       models.TextField(blank=True, default='')
    features =          models.TextField(blank=True, default='')
    
    objects =           PropertyManager()
    
    json =              JSONField(blank=True, default='')