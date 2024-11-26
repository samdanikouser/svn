from django.contrib import admin

from apps.authentication.models import UserProfile

# Register your models here.
admin.site.register(UserProfile)