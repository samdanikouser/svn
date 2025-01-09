# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from .forms import LoginForm, SignUpForm, UsernamePasswordResetForm, UserUpdateForm,UserProfileForm
from .decorators import role_required
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.models import User
import pandas as pd

from ..haccp.models import HaccpAdminData
from ..location.models import Location


def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    locations = Location.objects.filter(status = True)
    if request.method == "POST":
        location = ""
        if 'location' in request.POST:
            location =Location.objects.get(id=int(request.POST['location'])).name
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                userPofile_role = UserProfile.objects.get(user=user).role
                if userPofile_role in ['admin', 'managers','supervisor'] and not location:
                    return redirect('home')
                elif location or (userPofile_role in ['admin', 'managers','supervisor'] and location):
                    url = reverse('daily_activity')
                    return redirect(f'{url}{location}')
                else:
                    error_message = 'Your line user ,Please Select location'
            else:
                error_message = 'Invalid credentials'
        else:
            error_message = 'Error validating the form'
    else:
        error_message = None
    return render(request, "accounts/login.html", {"form": form, "error_message": error_message,'locations':locations})


def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
@role_required(allowed_roles=['admin','managers'])
def register_user(request):
    msg = None
    success = False
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            user = User.objects.get(username=request.POST["username"])
            Userprofile = UserProfile.objects.create(user=user)
            Userprofile.save()
            messages.success(request, "User has been Registered successfully!")
            return redirect("register")
    else:
        form = SignUpForm()
    print(form.errors)
    return render(request, 'accounts/registration.html', {'form': form})


@login_required
@role_required(allowed_roles=['admin','managers'])
def password_change_view(request, id):
    user = User.objects.get(pk=id)

    if request.method == 'POST':
        form = UsernamePasswordResetForm(request.POST, user=user)
        if form.is_valid():
            username = form.cleaned_data['username']
            new_password = form.cleaned_data['new_password1']
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Password changed successful!')
            return redirect("/user/list")
    else:
        form = UsernamePasswordResetForm(user=user)

    return render(request, 'users/passwordchange.html', {"form": form})


@login_required
@role_required(allowed_roles=['admin','managers'])
def home(request):
    return render(request, 'home/index.html')



@login_required
@role_required(allowed_roles=['admin','managers'])
def list_user(request):
    users = UserProfile.objects.all()
    return render(request, "users/user_list.html", {'users': users})


@login_required
@role_required(allowed_roles=['admin','managers'])
def delete_user(request, id):
    user = UserProfile.objects.get(pk=id)
    if request.method == "POST":
        user.delete()
        messages.success(request, "User has been Deleted successfully!")
        return redirect("/user/list")
    return render(request,
                  'users/user_delete.html',
                  {'user': user})


@login_required
@role_required(allowed_roles=['admin','managers'])
def update_user(request, id):
    user = UserProfile.objects.get(pk=id)
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("/user/list")
    else:
        form = UserUpdateForm(instance=user)
    return render(request, 'users/user_update.html', {'form': form,"user": user})



@login_required
@role_required(allowed_roles=['admin', 'managers'])
def add_single_user_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user = User.objects.create_user(
                    username=str(user_profile.employee_id),
                    password=None 
                )
            user_profile.user = user  
            user_profile.save()  
            messages.success(request, "Profile Created successfully!")
            return redirect("/user/list")
    else:
        form = UserProfileForm()
    return render(request, 'users/add_single_user_profile.html', {'form': form})


@login_required
@role_required(allowed_roles=['admin', 'managers'])
def upload_excel_user_profiles(request):
    if request.method == 'POST' and request.FILES['excel_file']:
        excel_file = request.FILES['excel_file']
        df = pd.read_excel(excel_file)        
        for _, row in df.iterrows():
            user = User.objects.create_user(
                username=str(row['employee_id']),
                password=None  # No password set
            )
            UserProfile.objects.create(
                user=user,
                name=row['name'],
                role=row['role'],
                employee_id=row['employee_id'],
                data_of_joining=row['data_of_joining'],
                job_title=row['job_title'],
                status=row['status']
            )
        return redirect("/user/list")
    return render(request, 'users/upload_excel_user_profiles.html')
