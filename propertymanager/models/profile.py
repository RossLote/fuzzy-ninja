from django.db import models
from django.contrib.auth.models import User
from annoying.fields import AutoOneToOneField
from annoying.functions import get_object_or_None
from schedule.models import Calendar
from account.models import Account
from propertymanager.models import Company, CompanyMember

# Create your models here.

class ProfileManager(models.Manager):
    def create(seld, *args, **kwargs):
        user=kwargs['user']
        invited_user = get_object_or_None(InvitedUser, email=user.email)
        if invited_user:
            company = invited_user.company
            member = CompanyMember.objects.create(
                user = user,
                company = company,
                role = CompanyMember.MEMBER
            )
            
        profile = super(ProfileManager, self).create(*args, **kwargs)
        return profile

class Profile(models.Model):
    user =      models.OneToOneField(User, primary_key=True)
    calendar =  AutoOneToOneField(Calendar)
    account =   AutoOneToOneField(Account)
    
    objects = ProfileManager()
    
class InvitedUser(models.Model):
    email           = models.EmailField(primary_key=True)
    invited_by      = models.ForeignKey(User)
    date_invited    = models.DateField(auto_now_add=True)
    company         = models.ForeignKey(Company)