from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from cargo.models import Dock


class Employee(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=20,
                                      verbose_name=_('bank account number'))
    is_supervisor = models.BooleanField(verbose_name=_('supervisor'))
    address = models.CharField(max_length=150, verbose_name=_('address'))
    dock = models.ForeignKey(to=Dock, related_name='employees')
