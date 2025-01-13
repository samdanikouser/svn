from django.contrib import admin

from .models import HaccpAdminData,CoolingData,CookingData,ReHeatingData

admin.site.register(HaccpAdminData)
admin.site.register(CoolingData)
admin.site.register(CookingData)
admin.site.register(ReHeatingData)