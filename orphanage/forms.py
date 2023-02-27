from django.forms import ModelForm
from .models import *
from django import forms
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget


class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.TimeInput):
    input_type = 'time'


class GuardianForm(forms.ModelForm):
  phone = PhoneNumberField(widget = PhoneNumberPrefixWidget(initial='MY'))

  class Meta:
    model = Guardian
    fields = ('idn', 'first_name', 'last_name', 'dob', 'gender', 'job', 'email', 'phone', 'add')
    widgets = {'dob':DateInput()}


class OrphanForm(forms.ModelForm):
  class Meta:
    model = Orphan
    fields = ('idn', 'first_name', 'last_name', 'gender', 'dental_img', 'status')


class OutingForm(forms.ModelForm):
  accompany_phone = PhoneNumberField(widget = PhoneNumberPrefixWidget(initial='MY'))

  class Meta:
    model = Outing

    fields = ('orphan_fk', 'date_out', 'time_out', 'reason', 'accompany_first_name', 'accompany_last_name', 'accompany_idn', 'accompany_phone', 'date_in', 'time_in', 'status')

    labels = {
      'orphan_fk':'Orphan Name',
    }

    widgets = {
      'date_in':DateInput(),
      'date_out':DateInput(),
      'time_in':TimeInput(),
      'time_out':TimeInput(),
    }


class AdoptionForm(forms.ModelForm):
  phone = PhoneNumberField(widget = PhoneNumberPrefixWidget(initial='MY'))

  class Meta:
    model = Adoption

    fields = ('orphan_fk', 'idn', 'first_name', 'last_name', 'dob', 'gender', 'job', 'email', 'phone', 'add')

    labels = {
      'orphan_fk':'Orphan Name',
    }
    
    widgets = {'dob':DateInput()}
