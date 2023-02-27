from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from accounts.decorators import unauthenticated_user
from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from accounts.models import *
from django.contrib import messages
from dotenv import load_dotenv
import os

# Create your views here.


def home(request):
    return render(request=request, template_name="home/home.html")


@unauthenticated_user
def login(request):
    if request.method == "POST":
        # Pass POST data into AuthenticationForm
        form = AuthenticationForm(request, data=request.POST)
        # Check if user exists (username exists in system)
        if Account.objects.filter(username=form.data['username']).exists():
            # Check if form is valid
            if form.is_valid():
                # Get cleaned form fields
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                # Authenticate user (check if user with username and password exists)
                user = auth.authenticate(username=username, password=password)
                if user is not None:
                    # Login as user if credentials match
                    auth.login(request, user,
                               'django.contrib.auth.backends.ModelBackend')
                    messages.success(
                        request, f"Successfully signed in as {username}.")
                    if request.user.role == 1:
                        # Redirect administrators to admin dashboard
                        return redirect('admin_dashboard')
                    elif request.user.role == 2:
                        # Redirect donor to donor dashboard
                        return redirect('cashdonation_records')
                    else:
                        # Redirect to error page
                        code = 403
                        title = "Forbidden"
                        message = "Unauthenticated access are not allowed. Please sign in to access this page"
                        return render(request=request, template_name="error/error.html", context={"code": code, "title": title, "message": message})
                else:
                    # Display error message if login unsuccessful
                    messages.error(request, "Invalid username or password.")
            else:
                print(form.errors)
                # Display error message if login unsuccessful
                messages.error(request, "Invalid username or password.")
        else:
            # Display error message if login unsuccessful
            messages.error(request, "Invalid username or password.")
    # For GET request, display login page with login form
    form = AuthenticationForm()
    return render(request=request, template_name="authentication/login.html", context={"form": form})


@login_required(login_url='login')
def logout(request):
    # # Display logout message
    # msg = 'You have been successfully signed out.'
    # messages.success(request, msg)

    # Logout user
    auth.logout(request)

    # Render logout page
    # return render(request=request, template_name='authentication/logout.html')
    return redirect('home')
