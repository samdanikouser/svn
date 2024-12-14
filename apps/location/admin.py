from django.contrib import admin

from apps.location.models import Location,ControlPoint

# Register your models here.

admin.site.register(Location)
admin.site.register(ControlPoint)