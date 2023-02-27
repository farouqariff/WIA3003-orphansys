from django.db import models
from django.utils.timezone import now
from django.core.validators import RegexValidator
from django.utils.translation import gettext as _
from phonenumber_field.modelfields import PhoneNumberField
import datetime


GENDER = (
        ('',  _('Select')),
        (1,  _('Male')),
        (2, _('Female')),
        (3, _('Other')),
    )


class Guardian(models.Model):

  idn = models.IntegerField(unique=True, null=True, blank=True)
  first_name = models.CharField(max_length=64, null=True, blank=True)
  last_name = models.CharField(max_length=64, null=True, blank=True)
  dob = models.DateField(null=True, blank=True)
  gender = models.PositiveSmallIntegerField(choices=GENDER, default=1)
  job = models.CharField(max_length=100, null=True, blank=True)
  email = models.EmailField(null=True, blank=True)
  phone = PhoneNumberField(max_length=16, unique=True)
  add = models.TextField()

  def __str__(self):
    fname = self.first_name + " " + self.last_name
    return fname


class Orphan(models.Model):
  ADOPT_STATUS = (
        ('',  _('Select')),
        (1,  _('Not adopted')),
        (2, _('Adopted')),
    )
  idn = models.IntegerField(unique=True)
  first_name = models.CharField(max_length=64)
  last_name = models.CharField(max_length=64)
  gender = models.PositiveSmallIntegerField(choices=GENDER, default=1)
  dental_img = models.ImageField(upload_to="x-rays/", null=True, blank=True)
  est_age = models.CharField(max_length=4, null=True, blank=True)
  status = models.PositiveSmallIntegerField(choices=ADOPT_STATUS, default=1)
  guardian_fk = models.ForeignKey(Guardian, on_delete=models.CASCADE)

  def __str__(self):
    fname = self.first_name + " " + self.last_name
    return fname
 

class Outing(models.Model):
  OUT_STATUS = (
        ('',  _('Select')),
        (1,  _('Outing')),
        (2, _('Arrived')),
    )
  date_out = models.DateField(default=datetime.date.today)
  time_out = models.TimeField(default=datetime.datetime.now().time())
  reason = models.TextField()
  accompany_first_name = models.CharField(max_length=64)
  accompany_last_name = models.CharField(max_length=64)
  accompany_idn = models.IntegerField()
  accompany_phone = PhoneNumberField(max_length=16, unique=True)
  date_in = models.DateField(blank=True, null=True)
  time_in = models.TimeField(blank=True, null=True)
  status = models.PositiveSmallIntegerField(blank=True, choices=OUT_STATUS, default=1)
  orphan_fk = models.ForeignKey(Orphan, on_delete=models.CASCADE)


class Adoption(models.Model):
  idn = models.IntegerField(unique=True)
  first_name = models.CharField(max_length=64)
  last_name = models.CharField(max_length=64)
  dob = models.DateField()
  gender = models.PositiveSmallIntegerField(choices=GENDER, default=1)
  job = models.CharField(max_length=100)
  email = models.EmailField(unique=True)
  phone = PhoneNumberField(max_length=16, unique=True)
  add = models.TextField()
  orphan_fk = models.OneToOneField(Orphan, on_delete=models.CASCADE)