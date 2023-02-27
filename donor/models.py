from django.utils.translation import gettext as _
from django.db import models
from django.conf import settings


class Donor(models.Model):
    GENDER = (
        ('',  _('Select')),
        (1,  _('Male')),
        (2, _('Female')),
        (3, _('Other')),
    )

    acc_fk = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    gender = models.PositiveSmallIntegerField(choices=GENDER, default=1)
    date_of_birth = models.DateField()
    occupation = models.CharField(max_length=100)
    annual_income = models.PositiveBigIntegerField(_('RM'))
    address = models.TextField()

    def __str__(self):
        return str(self.acc_fk.username)
