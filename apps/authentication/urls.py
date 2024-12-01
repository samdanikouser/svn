# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from .views import login_view, user_logout,register_user,password_change_view,home,update_user,delete_user,list_user,add_single_user_profile,upload_excel_user_profiles

urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path('user/update/<int:id>', update_user, name="update_user"),
    path('user/update/password/<int:id>', password_change_view, name="update_user_password"),
    path('user/delete/<int:id>', delete_user, name="delete_user"),
    path('user/list/', list_user, name="list_user"),
    path('userprofile/add-single/', add_single_user_profile, name='add_single_user_profile'),
    path('userprofile/upload-excel/', upload_excel_user_profiles, name='upload_excel_user_profiles'),
    path("logout/", user_logout, name="logout"),
    path('',home, name='home'),
]
