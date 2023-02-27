from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm
from django import forms
from .models import *
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget

# ---------------------------------------------------------------------------- #
#                      CUSTOM USER CREATION & CHANGE FORM                      #
# ---------------------------------------------------------------------------- #


class CustomUserCreationForm(UserCreationForm):
    phone_number = PhoneNumberField(widget = PhoneNumberPrefixWidget(initial='MY'))

    class Meta:
        model = Account
        fields = ("username", "email", "first_name",
                  "last_name", "role", "password1", "password2", "phone_number")

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)

        # Set administrative privileges if user's role is Administrator
        if user.role == 1:
            user.is_staff = True
            user.is_superuser = True

        if commit:
            user.save()

        return user


class CustomUserChangeForm(UserChangeForm):
    phone_number = PhoneNumberField(widget = PhoneNumberPrefixWidget(initial='MY'))
    
    class Meta:
        model = Account
        fields = '__all__'