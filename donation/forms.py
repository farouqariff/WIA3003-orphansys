from django.forms import ModelForm
from .models import *
from django import forms
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget


class DateInput(forms.DateInput):
    input_type = 'date'


class ItemForm(forms.ModelForm):
  class Meta:
    model = Item
    fields = ('name', 'rqd', 'date')
    widgets = {'date':DateInput()}


class ItemDonationForm(forms.ModelForm):
  class Meta:
    model = ItemDonation
    fields = ('item', 'donor', 'qty', 'date')
    widgets = {'date':DateInput()}


class CashDonationForm(forms.ModelForm):
  class Meta:
    model = CashDonation
    fields = ('amt', 'receipt', 'status', 'date', 'invoice')
    widgets = {'date':DateInput()}