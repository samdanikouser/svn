# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm, UsernamePasswordResetForm, UserUpdateForm
from .decorators import role_required
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.models import User


from ..haccp.models import HaccpAdminData
from ..location.models import Location


def login_view(request):
    locations = Location.objects.filter(status=True)
    form = LoginForm(request.POST or None)
    msg = None
    print(request.method)
    if request.method == "POST":
        location = ""
        if 'location' in request.POST:
            location = request.POST['location']
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                userPofile_role = UserProfile.objects.get(user=user).role
                if userPofile_role in ['admin', 'managers']:
                    return redirect('home')
                elif location:
                    url = reverse('daily_activity')
                    return redirect(f'{url}?location={location}')
                else:
                    error_message = 'Your line user ,Please Select location'
            else:
                error_message = 'Invalid credentials'
        else:
            error_message = 'Error validating the form'
    else:
        error_message = None
    return render(request, "accounts/login.html", {"form": form, "error_message": error_message,"locations":locations})


@login_required
def daily_activity(request):
    location = Location.objects.get(id=request.GET.get('location')).name
    daily_activity = HaccpAdminData.objects.filter(storage_location = Location.objects.get(id=request.GET.get('location')))
    return render(request, 'users_first_page.html',{"location":location,"daily_activity":daily_activity})


def register_user(request):
    msg = None
    success = False
    locations = Location.objects.all()

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            user = User.objects.get(username=request.POST["username"])
            Userprofile = UserProfile.objects.get(user=user)
            Userprofile.role = request.POST["selected_options"]
            Userprofile.save()
            messages.success(request, "User has been Registered successfully!")
            return redirect("register")
    else:
        form = SignUpForm()
    print(form.errors)
    return render(request, 'accounts/registration.html', {'form': form,"locations":locations})


@login_required
@role_required(allowed_roles=['admin','managers'])
def password_change_view(request, id):
    locations = Location.objects.all()
    user = User.objects.get(pk=id)

    if request.method == 'POST':
        # Pass the user object, not just the username string
        form = UsernamePasswordResetForm(request.POST, user=user)
        if form.is_valid():
            # Get the username and new password from the form
            username = form.cleaned_data['username']
            new_password = form.cleaned_data['new_password1']

            # Find the user by username and update the password
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()

            # Show success message
            messages.success(request, 'Password changed successful!')
            return redirect("/user/list")
    else:
        # Pass the user object when initializing the form
        form = UsernamePasswordResetForm(user=user)

    return render(request, 'users/passwordchange.html', {"form": form,"locations":locations})


@login_required
@role_required(allowed_roles=['admin','managers'])
def home(request):
    locations= Location.objects.all()
    return render(request, 'home/index.html',{"locations":locations})



@login_required
@role_required(allowed_roles=['admin','managers'])
def list_user(request):
    locations = Location.objects.all()
    users = UserProfile.objects.all()
    return render(request, "users/user_list.html", {'users': users,"locations":locations})


@login_required
@role_required(allowed_roles=['admin','managers'])
def delete_user(request, id):
    locations = Location.objects.all()
    user = UserProfile.objects.get(pk=id)
    if request.method == "POST":
        user.delete()
        messages.success(request, "User has been Deleted successfully!")
        return redirect("/user/list")
    return render(request,
                  'users/user_delete.html',
                  {'user': user,"locations":locations})


# update employee
@login_required
@role_required(allowed_roles=['admin','managers'])
def update_user(request, id):
    locations = Location.objects.all()
    user = UserProfile.objects.get(pk=id)
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("/user/list")
    else:
        form = UserUpdateForm(instance=user)
    return render(request, 'users/user_update.html', {'form': form,"user": user,"locations":locations})