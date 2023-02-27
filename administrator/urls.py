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
    path("dashboard", views.admin_dashboard,
         name="admin_dashboard"),
    
    path("admin_management", views.admin_management,
         name="admin_management"),
    path("add_admin", views.add_admin,
        name="add_admin"),
    path("update_admin/<int:pk>/", views.update_admin, 
        name="update_admin"),
    path("delete_admin/<int:pk>/", views.delete_admin, 
        name="delete_admin"),

    path("donor_management", views.donor_management,
         name="donor_management"),
    path("add_donor", views.add_donor,
         name="add_donor"),
    path("update_donor/<int:pk>/", views.update_donor, 
        name="update_donor"),
    path("delete_donor/<int:pk>/", views.delete_donor, 
        name="delete_donor"),
    
    path("orphan_management", views.orphan_management,
         name="orphan_management"),
    path("add_orphan", views.add_orphan,
         name="add_orphan"),
    path("update_orphan/<int:pk>/", views.update_orphan,
         name="update_orphan"),
         path("delete_orphan/<int:pk>/", views.delete_orphan,
         name="delete_orphan"),
     path("update_orphan2/<int:pk>/", views.update_orphan2,
         name="update_orphan2"),
    
    path("outing_management", views.outing_management,
         name="outing_management"),
     path("add_outing", views.add_outing,
         name="add_outing"),
    path("update_outing/<int:pk>/", views.update_outing,
         name="update_outing"),
         path("delete_outing/<int:pk>/", views.delete_outing,
         name="delete_outing"),
    
    path("adoption_management", views.adoption_management,
         name="adoption_management"),
     path("add_adoption", views.add_adoption,
         name="add_adoption"),
    path("update_adoption/<int:pk>/", views.update_adoption,
         name="update_adoption"),
         path("delete_adoption/<int:pk>/", views.delete_adoption,
         name="delete_adoption"),
    
    path("guardian_management", views.guardian_management,
         name="guardian_management"),
    path("add_guardian", views.add_guardian,
         name="add_guardian"),
    path("update_guardian/<int:pk>/", views.update_guardian,
         name="update_guardian"),
         path("delete_guardian/<int:pk>/", views.delete_guardian,
         name="delete_guardian"),

     path("item_management", views.item_management,
         name="item_management"),
     path("add_item", views.add_item,
         name="add_item"),
     path("update_item/<int:pk>/", views.update_item,
         name="update_item"),
     path("delete_item/<int:pk>/", views.delete_item,
         name="delete_item"),
     
     path("itemdonation_management", views.itemdonation_management,
         name="itemdonation_management"),
     path("add_itemdonation", views.add_itemdonation,
         name="add_itemdonation"),
     path("update_itemdonation/<int:pk>/", views.update_itemdonation,
         name="update_itemdonation"),
     path("delete_itemdonation/<int:pk>/", views.delete_itemdonation,
         name="delete_itemdonation"),
     
     path("cashdonation_management", views.cashdonation_management,
         name="cashdonation_management"),
     path("add_cashdonation", views.add_cashdonation,
         name="add_cashdonation"),
     path("update_cashdonation/<int:pk>/", views.update_cashdonation,
         name="update_cashdonation"),
     path("delete_cashdonation/<int:pk>/", views.delete_cashdonation,
         name="delete_cashdonation"),
    
    path("sms_item", views.sms_item, name="sms_item"),

    path("invoice_pdf", views.render_pdf_view, name="invoice_pdf"),

    path("donation_invoice/<int:pk>/", views.donation_invoice_pdf_view, 
    name="donation_invoice"),
]
