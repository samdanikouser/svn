# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include  # add this

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("apps.authentication.urls")),
    path("add/", include("apps.home.urls")),
    path("haccp/", include("apps.haccp.urls")),
    path("action/", include("apps.correctiveaction.urls")),
    path("location/", include("apps.location.urls")),
    path("role/", include("apps.roles.urls")),
    path("user/", include("apps.usersapp.urls")),
    path("personalhygiene/",include("apps.personalhygiene.urls")),
    path("department/",include("apps.department.urls")),
    path("attendance/",include("apps.attendance.urls")),
    path("attendance/",include("apps.attendance.urls")),
    path("disciplinary_record/",include("apps.disciplinary_record.urls")),
    path("internal_orders/",include("apps.internal_orders.urls")),
    path("stewarding/",include("apps.stewarding.urls"))

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)