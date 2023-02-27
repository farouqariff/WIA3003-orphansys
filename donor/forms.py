from django.forms import ModelForm
from accounts.models import *
from accounts.forms import *
from django import forms
from .models import *


class DateInput(forms.DateInput):
    input_type = 'date'


class DonorUserChangeForm(CustomUserChangeForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        self.fields.pop('role')
        self.fields.pop('date_joined')
        self.fields.pop('last_login')


class DonorForm(forms.ModelForm):
    class Meta:
        model = Donor
        exclude = ('acc_fk',)
        widgets = {'date_of_birth': DateInput()}
