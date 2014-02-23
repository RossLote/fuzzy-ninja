from django.db import models
from django.conf import settings
from .subscription import SubscriptionModel

class PaymentPlan(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    
    description = models.TextField()
    
    price_gbp = models.DecimalField(max_digits=8, decimal_places=2, null=True, default=None)
    price_eur = models.DecimalField(max_digits=8, decimal_places=2, null=True, default=None)
    price_cad = models.DecimalField(max_digits=8, decimal_places=2, null=True, default=None)
    price_aud = models.DecimalField(max_digits=8, decimal_places=2, null=True, default=None)
    price_nzd = models.DecimalField(max_digits=8, decimal_places=2, null=True, default=None)
    price_usd = models.DecimalField(max_digits=8, decimal_places=2, null=True, default=None)
    
    subscription_type = models.ForeignKey(SubscriptionModel)
    
    @property
    def price(self):
        if settings.CURRENCY == 'GBP':
            price = self.price_gbp
        elif settings.CURRENCY == 'EUR':
            price = self.price_eur
        elif settings.CURRENCY == 'USD':
            price = self.price_usd
        elif settings.CURRENCY == 'CAD':
            price = self.price_cad
        elif settings.CURRENCY == 'NZD':
            price = self.price_nzd
        else:
            price = self.price_aud
        
        return price