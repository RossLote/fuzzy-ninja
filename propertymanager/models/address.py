from django.db import models

class Address(models.Model):
    slug =          models.SlugField()
    first_names =   models.CharField(max_length=255, blank=True, default='')
    last_name =     models.CharField(max_length=255, blank=True, default='')
    house_number =  models.PositiveSmallIntegerField(null=True, default=None)
    flat_number =   models.PositiveSmallIntegerField(null=True, default=None)
    house_name =    models.CharField(max_length=255, blank=True, default='')
    street =        models.CharField(max_length=255, blank=True, default='')
    town =          models.CharField(max_length=255, blank=True, default='')
    city =          models.CharField(max_length=255, blank=True, default='')
    state =         models.CharField(max_length=255, blank=True, default='')
    country =       models.CharField(max_length=255, blank=True, default='')
    postcode =      models.CharField(max_length=255, blank=True, default='')
    latitude =      models.CharField(max_length=255, blank=True, default='')
    longitude =     models.CharField(max_length=255, blank=True, default='')
    
    def getLine1(self):
        if self.house_name:
            part1 = self.house_name
        else:
            part1 = str(self.house_number)
            if self.flat_number:
                part1 = 'Flat %d, %s' % (self.flat_number, part1)
            
        return '%s %s' % (part1, self.street)