"""orphansys2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from . import views
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView

urlpatterns = [
    path("dashboard", views.donor_dashboard,
         name="donor_dashboard"),
    path("request_invoice", views.request_invoice,
    name="request_invoice"),
    path("add_cashdonation_donor", views.add_cashdonation_donor,
    name="add_cashdonation_donor"),
    path("cashdonation_records", views.cashdonation_records,
    name="cashdonation_records"),
    path("update_donor_user/<int:pk>/", views.update_donor_user,
    name="update_donor_user"),
]
