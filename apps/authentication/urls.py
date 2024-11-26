# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from .views import login_view, register_user,daily_activity,password_change_view,home,update_user,delete_user,list_user
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path('user/update/<int:id>', update_user, name="update_user"),
    path('user/update/password/<int:id>', password_change_view, name="update_user_password"),
    path('user/delete/<int:id>', delete_user, name="delete_user"),
    path('user/list/', list_user, name="list_user"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('daily_activity/', daily_activity, name='daily_activity'),
    path('',home, name='home'),

    # path('/list', views.user_list, name='user_list'),
    # path('/delete/<int:id>', views.delete_user, name='delete_user'),
]
