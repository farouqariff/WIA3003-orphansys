from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import *
from donor.models import *


@admin.register(Account)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = Account

    list_display = ('username', 'email',
                    'role', 'is_superuser', 'is_active', 'last_login', 'phone_number')
    list_filter = ('email', 'is_staff', 'is_active', 'phone_number')

    # readonly_fields = ('date_joined', 'last_login')

    fieldsets = (
        ('Personal info', {'fields': (
            'username', 'email', 'role', 'first_name', 'last_name', 'password', 'date_joined', 'last_login', 'phone_number')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(Donor)
