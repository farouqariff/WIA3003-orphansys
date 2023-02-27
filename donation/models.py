from django.db import models
from donor.models import *
import datetime
from django.utils.translation import gettext as _


class Item(models.Model):
  name = models.CharField(max_length=256, unique=True)
  rqd = models.IntegerField(blank=True, default=0)
  date = models.DateField(blank=True, default=datetime.date.today)

  def __str__(self):
    return self.name


class ItemDonation(models.Model):
  item = models.ForeignKey(Item, on_delete=models.CASCADE)
  donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
  qty = models.IntegerField()
  date = models.DateField(default=datetime.date.today)


class CashDonation(models.Model):
  DONATE_STATUS = (
        ('',  _('Select')),
        (1,  _('Rejected')),
        (2, _('Pending')),
        (3, _('Approved')),
    )

  donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
  amt = models.DecimalField(max_digits=8, decimal_places=2)
  receipt = models.ImageField(upload_to="receipts/")
  status = models.PositiveSmallIntegerField(choices=DONATE_STATUS, default=2, blank=True)
  date = models.DateField(default=datetime.date.today)
  invoice = models.FileField(upload_to="invoices/", null=True, blank=True)



