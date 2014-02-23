from django.db import models
from django.contrib.auth.models import User
from annoying.functions import get_object_or_None
from annoying.fields import AutoOneToOneField
from account.models import Account

def create_api_key():
    while True:
        key = ''.join(
           random.choice('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_')
           for i in range(64)
        )
        if not get_object_or_None(Company, api_key=key):
            break
    return key

class Company(models.Model):
    slug =      models.SlugField()
    name =      models.CharField(max_length=255)
    account =   AutoOneToOneField(Account)
    api_key =   models.CharField(max_length=64, unique=True, default=create_api_key)
    website =   models.URLField(blank=True, default='')
    members =   models.ManyToManyField(User, through='CompanyMember')
    allow_multiple_members = models.BooleanField(default=False)
    
class CompanyMember(models.Model):
    ADMIN       = 1
    MANAGER     = 2
    MEMBER      = 3
    ROLES = (
        (ADMIN,     'administrator'),
        (MANAGER,   'manager'),
        (MEMBER,    'member'),
    )
    user =          models.ForeignKey(User)
    company =       models.ForeignKey(Company)
    role =          models.PositiveSmallIntegerField(choices=ROLES)
    date_joined =   models.DateField(auto_now_add=True)