from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.role == 1:
                # Redirect administrators to admin dashboard
                return redirect('admin_dashboard')
            elif request.user.role == 2:
                # Redirect Smart Watch Users to SWU dashboard
                return redirect('donor_dashboard')
            else:
                code = 403
                title = "Forbidden"
                message = "You are not authorized to access this page."
                return render(request=request, template_name="error/error.html", context={"code": code, "title": title, "message": message})

        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def allowed_users(allowed_role):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if not request.user.is_authenticated:
                code = 403
                title = "Forbidden"
                message = "Unauthenticated access are not allowed. Please sign in to access this page"
                return render(request=request, template_name="error/error.html", context={"code": code, "title": title, "message": message})
            else:
                flag = False

                for i in range(len(allowed_role)):
                    if request.user.role == allowed_role[i]:
                        flag = True

                if (flag):
                    return view_func(request, *args, **kwargs)
                else:
                    code = 401
                    title = "Unauthorized"
                    message = "You are not authorized to access this page."
                    return render(request=request, template_name="error/error.html", context={"code": code, "title": title, "message": message})
        return wrapper_func
    return decorator
