from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import *
from accounts.models import *
from donor.models import *
from accounts.forms import *
from donor.forms import *
from accounts.decorators import *
from donation.models import CashDonation
from donation.forms import CashDonationForm

# Create your views here.
@allowed_users(allowed_role=[2])
def donor_dashboard(request):
    context = {
        'donor_id': Donor.objects.get(acc_fk__id=request.user.id).id,
    }
    return render(request=request, template_name="donor/dashboard.html")

@allowed_users(allowed_role=[2])
def request_invoice(request):
    context = {
        'donor_id': Donor.objects.get(acc_fk__id=request.user.id).id,
    }
    return render(request=request, template_name="donor/request_invoice.html", context=context)

@allowed_users(allowed_role=[2])
def cashdonation_records(request):
    context = {
        # 'cd_list': CashDonation.objects.all(),
        'cd_list': CashDonation.objects.filter(donor__acc_fk__id=request.user.id),
        'donor_id': Donor.objects.get(acc_fk__id=request.user.id).id,
    }
    return render(request=request, template_name="donor/cashdonation_records.html", context=context)

@allowed_users(allowed_role=[2])
def add_cashdonation_donor(request):
    if request.method == 'POST':
        cashdonate_form = CashDonationForm(request.POST or None, request.FILES)
 
        if cashdonate_form.is_valid():
            cashd = cashdonate_form.save(commit=False)
            cashd.donor = Donor.objects.get(acc_fk__id=request.user.id)
            cashd.save()
            return redirect('cashdonation_records')
        else:
            print(cashdonate_form.errors)
            return render(request, "donor/add_cashdonation_donor.html", {'cd_form': cashdonate_form, 'donor_id': Donor.objects.get(acc_fk__id=request.user.id).id})
    return render(request, "donor/add_cashdonation_donor.html", {'cd_form': CashDonationForm(), 'donor_id': Donor.objects.get(acc_fk__id=request.user.id).id})

@allowed_users(allowed_role=[2])
def update_donor_user(request, pk):
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
            return render(request, 'donor/update_donor_user.html', context)
        return redirect('cashdonation_records')
    context = {
        'cu_form': DonorUserChangeForm(instance=Account.objects.get(id=Donor.objects.get(id=pk).acc_fk.id)),
        'd_form': DonorForm(instance=Donor.objects.get(id=pk)),
        'd_list': Donor.objects.all(),
        'donor_id': Donor.objects.get(id=pk).id,
    }
    return render(request, 'donor/update_donor_user.html', context)

