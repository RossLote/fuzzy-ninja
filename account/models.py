from django.db import models

# Create your models here.
class Account(models.Model):
    balance = models.DecimalField(max_digits=14, decimal_places=2, default=0)

class Transaction(models.Model):
    
    WITHDRAWAL =    1
    PAYMENT =       2
    DIRECT_DEBIT =  3
    DEPOSIT =      4
    TYPES = (
        (WITHDRAWAL,    'withdrawal'),
        (PAYMENT,       'payment'),
        (DIRECT_DEBIT,  'direct debit'),
        (DEPOSIT,       'deposit'),
    )
    
    account =       models.ForeignKey(Account)
    
    description =   models.CharField(max_length=255)
    
    type =          models.PositiveSmallIntegerField(choices=TYPES)
    
    amount_in =     models.DecimalField(max_digits=14, decimal_places=2)
    amount_out =    models.DecimalField(max_digits=14, decimal_places=2)
    balance =       models.DecimalField(max_digits=14, decimal_places=2)