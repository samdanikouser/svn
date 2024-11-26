# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.urls import path, include  # add this

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("apps.authentication.urls")),
    path("add", include("apps.home.urls")),
    path("haccp", include("apps.haccp.urls")),
    path("action", include("apps.correctiveaction.urls")),
    path("location", include("apps.location.urls")),
    path("role", include("apps.roles.urls")),
    path("user", include("apps.usersapp.urls")),
]
