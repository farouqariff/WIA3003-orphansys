from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import *
from accounts.models import *
from accounts.forms import *
from donor.models import *
from donor.forms import *
from orphanage.models import *
from orphanage.forms import *
from donation.models import *
from donation.forms import *
from accounts.decorators import *

import numpy as np
import tensorflow as tf
from tensorflow import keras
import random

from twilio.rest import Client

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

from django.core.mail import EmailMessage, send_mail
from django.conf import settings

from django.db import IntegrityError
from django.contrib import messages

############################################### ADMIN DASHBOARD #################################################

@allowed_users(allowed_role=[1])
def admin_dashboard(request):
    return render(request=request, template_name="administrator/dashboard.html")

############################################ DAE MODEL ###########################################################

# Estimate age
def dae(imagefile):
    filename = "C:/orphansystem/media/x-rays/" + imagefile                                       # Save image file directory
    model = tf.keras.models.load_model('C:/orphansystem/media/models/daev1.h5')                 # Load the model
    class_names = np.array(['5', '6'])                                                          # Estimated age class
    img_height = 224                                                                            # Height image requirement
    img_width = 224                                                                             # Width image requirement
    img = tf.keras.utils.load_img(filename, target_size=(img_height, img_width))                # Modify image
    img_array = tf.keras.utils.img_to_array(img)                                                # Change image into array of numbers
    img_array = tf.expand_dims(img_array, 0)                                                    # Insert an addition dimension into array
    predictions = model.predict(img_array)                                                      # Predict score
    score = tf.nn.softmax(predictions[0])                                                       # Predict estimate age class
    return class_names[np.argmax(score)]                                                        # Return result

############################################ ADMIN CRUD ###########################################################

@allowed_users(allowed_role=[1])
def admin_management(request):
    context = {
        'a_list': Account.objects.filter(role=1)
    }
    return render(request=request, template_name="administrator/admin_management.html", context=context)


@allowed_users(allowed_role=[1])
def add_admin(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST or None)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.is_active = True
            user.role = 1
            user.save()
            return redirect('admin_management')
        else:
            print(user_form.errors)
            return render(request, "administrator/add_admin.html", {'cu_form': user_form})
    return render(request, "administrator/add_admin.html", {'cu_form': CustomUserCreationForm()})


@allowed_users(allowed_role=[1])
def update_admin(request, pk):
    if request.method == "POST":
        # Pass POST data into AdminUserChangeForm
        user_form = DonorUserChangeForm(
            request.POST or None, instance=get_object_or_404(Account, pk=pk))
        # Check if form is valid
        if user_form.is_valid():
            # Save form and set privileges to True
            user = user_form.save(commit=False)
            user.is_active = True
            user.save()
        else:
            print(user_form.errors)
            context = {
                'cu_form': DonorUserChangeForm(instance=Account.objects.get(id=pk)),
            }
            return render(request, 'administrator/update_admin.html', context)
        # Redirect to User Management page
        return redirect('admin_management')
    context = {
        'cu_form': DonorUserChangeForm(instance=Account.objects.get(id=pk)),
    }
    return render(request, 'administrator/update_admin.html', context) 


@allowed_users(allowed_role=[1])
def delete_admin(request, pk):
    # Save soon-to-be-deleted donor's object
    deleted_admin = Account.objects.get(
        id=pk)
    # Delete donor record from Donor and Account
    Account.objects.get(id=pk).delete()
    messages.success(
        request, f"Admin ({deleted_admin.get_full_name()}) deleted successfully.")
    return redirect('admin_management')


#################################### DONOR CRUD ##########################################################

@allowed_users(allowed_role=[1])
def donor_management(request):
    context = {
        'd_list': Donor.objects.all()
    }
    return render(request=request, template_name="administrator/donor_management.html", context=context)


@allowed_users(allowed_role=[1])
def add_donor(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST or None)
        donor_form = DonorForm(request.POST or None)
        if user_form.is_valid() and donor_form.is_valid():
            user = user_form.save(commit=False)
            user.is_active = True
            user.save()
            donor = donor_form.save(commit=False)
            donor.acc_fk = Account.objects.get(id=user.id)
            donor.save()
            return redirect('donor_management')
        else:
            print(user_form.errors)
            print(donor_form.errors)
            return render(request, "administrator/add_donor.html", {'cu_form': user_form, 'd_form': donor_form})
    return render(request, "administrator/add_donor.html", {'cu_form': CustomUserCreationForm(), 'd_form': DonorForm()})


@allowed_users(allowed_role=[1])
def update_donor(request, pk):
    if request.method == "POST":
        user_form = DonorUserChangeForm(
            request.POST or None, instance=get_object_or_404(Account, pk=Donor.objects.get(id=pk).acc_fk.id))
        donor_form = DonorForm(
            request.POST or None, instance=get_object_or_404(Donor, pk=pk))
        if user_form.is_valid() and donor_form.is_valid():
            # Save form and set privileges to True
            user = user_form.save(commit=False)
            user.is_active = True
            user.save()
            donor = donor_form.save(commit=False)
            donor.acc_fk = Account.objects.get(id=user.id)
            donor.save()
        else:
            print(user_form.errors)
            print(donor_form.errors)
            context = {
                'cu_form': DonorUserChangeForm(instance=Account.objects.get(id=Donor.objects.get(id=pk).acc_fk.id)),
                'd_form': DonorForm(instance=Donor.objects.get(id=pk)),
            }
            return render(request, 'administrator/update_donor.html', context)
        return redirect('donor_management')
    context = {
        'cu_form': DonorUserChangeForm(instance=Account.objects.get(id=Donor.objects.get(id=pk).acc_fk.id)),
        'd_form': DonorForm(instance=Donor.objects.get(id=pk)),
        'd_list': Donor.objects.all()
    }
    return render(request, 'administrator/update_donor.html', context)


@allowed_users(allowed_role=[1])
def delete_donor(request, pk):
    # Save soon-to-be-deleted donor's object
    deleted_donor = Account.objects.get(
        id=Donor.objects.get(id=pk).acc_fk.id)
    # Delete donor record from Donor and Account
    Account.objects.get(id=Donor.objects.get(id=pk).acc_fk.id).delete()
    messages.success(
        request, f"Donor ({deleted_donor.get_full_name()}) deleted successfully.")
    return redirect('donor_management')

##################################### Orphan CRUD ########################################################################333333

@allowed_users(allowed_role=[1])
def orphan_management(request):
    context = {
        'o_list': Orphan.objects.all()
    }
    return render(request=request, template_name="administrator/orphan_management.html", context=context)


@allowed_users(allowed_role=[1])
def add_orphan(request):
    if request.method == 'POST':
        guardian_form = GuardianForm(request.POST or None, prefix='guardian')
        orphan_form = OrphanForm(request.POST or None, request.FILES, prefix='orphan')
        if guardian_form.is_valid() and orphan_form.is_valid():
            guardian = guardian_form.save(commit=False)
            orphan = orphan_form.save(commit=False)
            guardian.save()  
            orphan.guardian_fk = Guardian.objects.get(id=guardian.id)  
            orphan.save()
            orphan.dental_img = orphan_form.cleaned_data.get('dental_img')                                       
            orphan.est_age = dae(str(orphan.dental_img))
            # orphan.est_age = str(random.randint(5,6))
            orphan.save()
            return redirect('orphan_management')
        else:
            print(guardian_form.errors)
            print(orphan_form.errors)
            return render(request, "administrator/add_orphan.html", {'g_form': guardian_form, 'o_form': orphan_form})
    return render(request, "administrator/add_orphan.html", {'g_form': GuardianForm(prefix='guardian'), 'o_form': OrphanForm(prefix='orphan')})


@allowed_users(allowed_role=[1])
def update_orphan(request, pk):
    if request.method == "POST":
        guardian_form = GuardianForm(
            request.POST or None, prefix='guardian',instance=get_object_or_404(Guardian, pk=Orphan.objects.get(id=pk).guardian_fk.id))
        orphan_form = OrphanForm(
            request.POST or None, request.FILES, prefix='orphan',instance=get_object_or_404(Orphan, pk=pk))
        if guardian_form.is_valid() and orphan_form.is_valid():
            # Save form and set privileges to True
            guardian = guardian_form.save(commit=False)
            guardian.save()
            orphan = orphan_form.save(commit=False)
            orphan.guardian_fk = Guardian.objects.get(id=guardian.id)
            orphan.save()
        else:
            print(guardian_form.errors)
            print(orphan_form.errors)
            context = {
                'g_form': GuardianForm(prefix='guardian', instance=Guardian.objects.get(id=Orphan.objects.get(id=pk).guardian_fk.id)),
                'o_form': OrphanForm(prefix='orphan', instance=Orphan.objects.get(id=pk)),
            }
            return render(request, 'administrator/update_orphan.html', context)
        return redirect('orphan_management')
    context = {
        'g_form': GuardianForm(prefix='guardian',instance=Guardian.objects.get(id=Orphan.objects.get(id=pk).guardian_fk.id)),
        'o_form': OrphanForm(prefix='orphan' ,instance=Orphan.objects.get(id=pk)),
        'o_list': Orphan.objects.all()
    }
    return render(request, 'administrator/update_orphan.html', context)


@allowed_users(allowed_role=[1])
def delete_orphan(request, pk):
    deleted_orphan = Orphan.objects.get(id=pk)
    Orphan.objects.get(id=pk).delete()
    messages.success(
        request, f"Orphan ({deleted_orphan}) deleted successfully.")
    return redirect('orphan_management')


@allowed_users(allowed_role=[1])
def update_orphan2(request, pk):
    if request.method == "POST":
        orphan_form = OrphanForm(
            request.POST or None, request.FILES, prefix='orphan',instance=get_object_or_404(Orphan, pk=pk))
        if orphan_form.is_valid():
            # Save form and set privileges to True
            orphan = orphan_form.save(commit=False)
            orphan.save()
        else:
            print(orphan_form.errors)
            context = {
                'o_form': OrphanForm(prefix='orphan', instance=Orphan.objects.get(id=pk)),
            }
            return render(request, 'administrator/update_orphan2.html', context)
        return redirect('orphan_management')
    context = {
        'o_form': OrphanForm(prefix='orphan' ,instance=Orphan.objects.get(id=pk)),
        'o_list': Orphan.objects.all()
    }
    return render(request, 'administrator/update_orphan2.html', context)

######################################## Guardian CRUD #####################################################

@allowed_users(allowed_role=[1])
def guardian_management(request):
    context = {
        'g_list': Guardian.objects.all()
    }
    return render(request=request, template_name="administrator/guardian_management.html", context=context)


@allowed_users(allowed_role=[1])
def add_guardian(request):
    if request.method == 'POST':
        guardian_form = GuardianForm(request.POST or None, prefix='guardian')
        if guardian_form.is_valid():
            guardian = guardian_form.save(commit=False)
            guardian.save()
            return redirect('guardian_management')
        else:
            print(guardian_form.errors)
            return render(request, "administrator/add_guardian.html", {'g_form': guardian_form})
    return render(request, "administrator/add_guardian.html", {'g_form': GuardianForm()})


@allowed_users(allowed_role=[1])
def update_guardian(request, pk):
    if request.method == "POST":
        guardian_form = GuardianForm(
            request.POST or None, prefix='guardian', instance=get_object_or_404(Guardian, pk=pk))
        if guardian_form.is_valid():
            # Save form and set privileges to True
            guardian = guardian_form.save(commit=False)
            guardian.save()
        else:
            print(guardian_form.errors)
            context = {
                'g_form': GuardianForm(instance=Guardian.objects.get(id=pk)),
            }
            return render(request, 'administrator/update_guardian.html', context)
        return redirect('guardian_management')
    context = {
        'g_form': GuardianForm(prefix='guardian' ,instance=Guardian.objects.get(id=pk)),
        'g_list': Guardian.objects.all()
    }
    return render(request, 'administrator/update_guardian.html', context)


@allowed_users(allowed_role=[1])
def delete_guardian(request, pk):
    # Save soon-to-be-deleted guardian's object
    deleted_guardian = Guardian.objects.get(id=pk)
    # Delete guardian record
    Guardian.objects.get(id=pk).delete()
    messages.success(
        request, f"Guardian ({deleted_guardian}) deleted successfully.")
    return redirect('guardian_management')

############################################# Outing CRUD #######################################################

@allowed_users(allowed_role=[1])
def outing_management(request):
    context = {
        'out_list': Outing.objects.all()
    }
    return render(request=request, template_name="administrator/outing_management.html", context=context)


@allowed_users(allowed_role=[1])
def add_outing(request):
    if request.method == 'POST':
        outing_form = OutingForm(request.POST or None)
        if outing_form.is_valid():
            outing = outing_form.save(commit=False)
            outing.save()
            return redirect('outing_management')
        else:
            print(outing_form.errors)
            return render(request, "administrator/add_outing.html", {'out_form': outing_form,})
    return render(request, "administrator/add_outing.html", {'out_form': OutingForm(),})


@allowed_users(allowed_role=[1])
def update_outing(request, pk):
    if request.method == "POST":
        outing_form = OutingForm(
            request.POST or None, instance=get_object_or_404(Outing, pk=pk))
        if outing_form.is_valid():
            outing = outing_form.save(commit=False)
            outing.save()
        else:
            print(outing_form.errors)
            context = {
                'out_form': OutingForm(instance=Outing.objects.get(id=pk)),
            }
            return render(request, 'administrator/update_outing.html', context)
        return redirect('outing_management')
    context = {
        'out_form': OutingForm(instance=Outing.objects.get(id=pk)),
        'out_list': Outing.objects.all()
    }
    return render(request, 'administrator/update_outing.html', context)


@allowed_users(allowed_role=[1])
def delete_outing(request, pk):
    # Save soon-to-be-deleted donor's object
    deleted_outing = Outing.objects.get(id=pk)
    # Delete donor record from Donor and Account
    Outing.objects.get(id=pk).delete()
    messages.success(
        request, f"Outing ({deleted_outing.orphan_fk}) deleted successfully.")
    return redirect('outing_management')


########################################### Adoption CRUD ##########################################################

@allowed_users(allowed_role=[1])
def adoption_management(request):
    context = {
        'ad_list': Adoption.objects.all()
    }
    return render(request=request, template_name="administrator/adoption_management.html", context=context)


@allowed_users(allowed_role=[1])
def add_adoption(request):
    if request.method == 'POST':
        adoption_form = AdoptionForm(request.POST or None)
        if adoption_form.is_valid():
            adoption = adoption_form.save(commit=False)
            adoption.save()
            return redirect('adoption_management')
        else:
            print(adoption_form.errors)
            return render(request, "administrator/add_adoption.html", {'ad_form': adoption_form,})
    return render(request, "administrator/add_adoption.html", {'ad_form': AdoptionForm(),})


@allowed_users(allowed_role=[1])
def update_adoption(request, pk):
    if request.method == "POST":
        adoption_form = AdoptionForm(
            request.POST or None, instance=get_object_or_404(Adoption, pk=pk))
        if adoption_form.is_valid():
            adoption = adoption_form.save(commit=False)
            adoption.save()
        else:
            print(adoption_form.errors)
            context = {
                'ad_form': AdoptionForm(instance=Adoption.objects.get(id=pk)),
            }
            return render(request, 'administrator/update_adoption.html', context)
        return redirect('adoption_management')
    context = {
        'ad_form': AdoptionForm(instance=Adoption.objects.get(id=pk)),
        'ad_list': Adoption.objects.all()
    }
    return render(request, 'administrator/update_adoption.html', context)


@allowed_users(allowed_role=[1])
def delete_adoption(request, pk):
    # Save soon-to-be-deleted donor's object
    deleted_adoption = Adoption.objects.get(
        id=pk)
    # Delete donor record from Donor and Account
    Adoption.objects.get(id=pk).delete()
    messages.success(
        request, f"Adoption ({deleted_adoption.orphan_fk.get_id()}) deleted successfully.")
    return redirect('adoption_management')

########################################### Item CRUD ######################################################

@allowed_users(allowed_role=[1])
def item_management(request):
    context = {
        'i_list': Item.objects.all()
    }
    return render(request=request, template_name="administrator/item_management.html", context=context)


@allowed_users(allowed_role=[1])
def add_item(request):
    if request.method == 'POST':
        item_form = ItemForm(request.POST or None)
        if item_form.is_valid():
            try:
                item = item_form.save(commit=False)
                item.name = item.name.upper()
                item.save()
                return redirect('item_management')
            except IntegrityError as e:
                if 'UNIQUE constraint' in str(e.args):
                    message = "Item name already exists. Please choose a different name."
                    messages.error(
                    request, message)
                    return render(request, "administrator/add_item.html", {'i_form': item_form})
        else:
            print(item_form.errors)
            return render(request, "administrator/add_item.html", {'i_form': item_form})
    return render(request, "administrator/add_item.html", {'i_form': ItemForm()})


@allowed_users(allowed_role=[1])
def update_item(request, pk):
    if request.method == "POST":
        item_form = ItemForm(
            request.POST or None, instance=get_object_or_404(Item, pk=pk))
        if item_form.is_valid():
            item = item_form.save(commit=False)
            item.save()
        else:
            print(item_form.errors)
            context = {
                'i_form': ItemForm(instance=Item.objects.get(id=pk)),
            }
            return render(request, 'administrator/update_item.html', context)
        return redirect('item_management')
    context = {
        'i_form': ItemForm(instance=Item.objects.get(id=pk)),
        'i_list': Item.objects.all()
    }
    return render(request, 'administrator/update_item.html', context)


@allowed_users(allowed_role=[1])
def delete_item(request, pk):
    # Save soon-to-be-deleted donor's object
    deleted_item = Item.objects.get(
        id=pk)
    # Delete donor record from Donor and Account
    Item.objects.get(id=pk).delete()
    messages.success(
        request, f"Item ({deleted_item.name}) deleted successfully.")
    return redirect('item_management')

######################################## Item Donation CRUD ####################################################

@allowed_users(allowed_role=[1])
def itemdonation_management(request):
    context = {
        'ido_list': ItemDonation.objects.all()
    }
    return render(request=request, template_name="administrator/itemdonation_management.html", context=context)


@allowed_users(allowed_role=[1])
def add_itemdonation(request):
    if request.method == 'POST':
        itemdonate_form = ItemDonationForm(request.POST or None)
        if itemdonate_form.is_valid():
            itemd = itemdonate_form.save(commit=False)
            items = Item.objects.get(id=itemd.item.id)
            if itemd.qty > 0:
                if items.rqd > itemd.qty:
                    Item.objects.filter(id=itemd.item.id).update(rqd=items.rqd - itemd.qty)
                else:
                    Item.objects.filter(id=itemd.item.id).update(rqd=0)
            itemd.save()
            return redirect('itemdonation_management')
        else:
            print(itemdonate_form.errors)
            return render(request, "administrator/add_itemdonation.html", {'ido_form': itemdonate_form})
    return render(request, "administrator/add_itemdonation.html", {'ido_form': ItemDonationForm()})


@allowed_users(allowed_role=[1])
def update_itemdonation(request, pk):
    if request.method == "POST":
        itemdonate_form = ItemDonationForm(
            request.POST or None, instance=get_object_or_404(ItemDonation, pk=pk))
        if itemdonate_form.is_valid():
            itemd = itemdonate_form.save(commit=False)
            items = Item.objects.get(id=itemd.item.id)
            if itemd.qty > 0:
                if items.rqd > itemd.qty:
                    Item.objects.filter(id=itemd.item.id).update(rqd=items.rqd - itemd.qty)
                else:
                    Item.objects.filter(id=itemd.item.id).update(rqd=0)
            itemd.save()
        else:
            print(itemdonate_form.errors)
            context = {
                'ido_form': ItemDonationForm(instance=ItemDonation.objects.get(id=pk)),
            }
            return render(request, 'administrator/update_itemdonation.html', context)
        return redirect('itemdonation_management')
    context = {
        'ido_form': ItemDonationForm(instance=ItemDonation.objects.get(id=pk)),
        'ido_list': ItemDonation.objects.all()
    }
    return render(request, 'administrator/update_itemdonation.html', context)


@allowed_users(allowed_role=[1])
def delete_itemdonation(request, pk):
    deleted_itemd = ItemDonation.objects.get(
        id=pk)
    # Delete donor record from Donor and Account
    ItemDonation.objects.get(id=pk).delete()
    messages.success(
        request, f"Item Donation ({deleted_itemd}) deleted successfully.")
    return redirect('itemdonation_management')

####################################### Cash Donation CRUD #####################################################

@allowed_users(allowed_role=[1])
def cashdonation_management(request):
    context = {
        'cd_list': CashDonation.objects.all()
    }
    return render(request=request, template_name="administrator/cashdonation_management.html", context=context)


@allowed_users(allowed_role=[1])
def add_cashdonation(request):
    if request.method == 'POST':
        cashdonate_form = CashDonationForm(request.POST or None, request.FILES)
        if cashdonate_form.is_valid():
            cashd = cashdonate_form.save(commit=False)
            cashd.save()
            return redirect('cashdonation_management')
        else:
            print(cashdonate_form.errors)
            return render(request, "administrator/add_cashdonation.html", {'cd_form': cashdonate_form})
    return render(request, "administrator/add_cashdonation.html", {'cd_form': CashDonationForm()})


@allowed_users(allowed_role=[1])
def update_cashdonation(request, pk):
    if request.method == "POST":
        cashdonate_form = CashDonationForm(
            request.POST or None, request.FILES,instance=get_object_or_404(CashDonation, pk=pk))
        if cashdonate_form.is_valid():
            cashd = cashdonate_form.save(commit=False)
            cashd.save()
            invoice_email(request, cashd.status, cashd.donor.acc_fk.email)
        else:
            print(cashdonate_form.errors)
            context = {
                'cd_form': CashDonationForm(instance=CashDonation.objects.get(id=pk)),
            }
            return render(request, 'administrator/update_cashdonation.html', context)
        return redirect('cashdonation_management')
    context = {
        'cd_form': CashDonationForm(instance=CashDonation.objects.get(id=pk)),
        'cd_list': CashDonation.objects.all(),
        'cd_user': CashDonation.objects.get(id=pk),
        
    }
    return render(request, 'administrator/update_cashdonation.html', context)


@allowed_users(allowed_role=[1])
def delete_cashdonation(request, pk):
    deleted_cashd = CashDonation.objects.get(
        id=pk)
    # Delete donor record from Donor and Account
    CashDonation.objects.get(id=pk).delete()
    messages.success(
        request, f"Cash Donation from ({deleted_cashd.donor}) deleted successfully.")
    return redirect('cashdonation_management')

####################################### TWILIO SMS ####################################################

@allowed_users(allowed_role=[1])
def sms_item(request):
    account_sid = "AC4abd50d1979e3b4a8053e58779163eb1"
    auth_token = "4ee597548a966f70cce4584e32b46f1d"
    client = Client(account_sid, auth_token)

    phone_donor_list = list(Account.objects.filter(role='2').values_list('phone_number', flat=True))                                # Donor's phone     
    item_list = list(zip(list(Item.objects.values_list('name',flat=True)), list(Item.objects.values_list('rqd',flat=True))))        # Item list
    item_required_list = [i for i in item_list if i[1] > 0]                                                                         # Only required item
    msg = 'Required items from the orphanage are \n' + '\n'.join(map(lambda x: str(x[0]) + ' ' + str(x[1]), item_required_list))    # Create text message

    # for phone in phone_donor_list:                                   
    #     message = client.messages.create(
    #                                 body=msg,
    #                                 from_='+15628370727',
    #                                 to=phone,
    #                             )
    
    message = client.messages.create(
                                    body=msg,
                                    from_='+15628370727',
                                    to='+60123307614',
                                )
    return redirect('item_management')

################################# CASH DONATION INVOICE ###############################################

def render_pdf_view(request):
    template_path = 'administrator/pdf1.html'
    context = {'myvar': 'this is your template context'}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    """ If download
    response['Content-Disposition'] = 'attachment; filename="report.pdf"' """
    # If display on web
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


@allowed_users(allowed_role=[1])
def donation_invoice_pdf_view(request, pk):
    donation_info = CashDonation.objects.get(id=pk)
    template_path = 'administrator/pdf2.html'
    context = {'donation_info':donation_info}
    response = HttpResponse(content_type='application/pdf')
    filename = f"{donation_info.date}_{donation_info.donor.acc_fk.get_full_name()}.pdf"
    pdf_setting = 'attachment; filename="' + filename + '"'
    # If download
    response['Content-Disposition'] = pdf_setting
    # If display on web
    # response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

################################# EMAIL NOTIFICATION ###############################################

# Notify invoice
def invoice_email(request, status, user_email):
    if status >0 and status <4:
        if status !=2:
            if status == 3:
                email = EmailMessage(
                    'Donation Invoice',
                    'Your donation is valid, please check on your account to download invoice file.',
                    settings.EMAIL_HOST_USER,
                    [user_email],
                )
            elif status == 1:
                email = EmailMessage(
                    'Donation Invoice',
                    'Your donation is not valid.',
                    settings.EMAIL_HOST_USER,
                    [user_email],
                )
            email.fail_silently = True
            email.send()