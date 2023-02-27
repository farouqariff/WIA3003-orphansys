from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from donor.models import *

admin.site.register(Orphan)
admin.site.register(Outing)
admin.site.register(Guardian)
admin.site.register(Adoption)