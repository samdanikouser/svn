from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from apps.haccp.models import HaccpAdminData

class DailyUpdates(models.Model):
    id = models.AutoField(primary_key=True)
    haccp_link = models.ForeignKey(HaccpAdminData, on_delete=models.CASCADE,null=True,blank=True)
    temperature_value = models.FloatField()
    haccp_link_time_given = models.TimeField(null=True,blank=True)
    corrective_actions = models.TextField(null=True,blank=True)
    text_message = models.TextField(null=True,blank=True)
    supervisor_approved_by = models.CharField(max_length=200, null=True, blank=True)
    supervisor_approved_status = models.CharField(max_length=200, null=True, blank=True)
    manager_approved_by = models.CharField(max_length=200, null=True, blank=True)
    manager_approved_status = models.CharField(max_length=200, null=True, blank=True)
    supervisor_comments = models.TextField(null=True,blank=True)
    created_by = models.ForeignKey(User, related_name='created_daily_updates', on_delete=models.SET_NULL, null=True)
    modified_by = models.ForeignKey(User, related_name='modified_daily_updates', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(default=datetime.now,null=True,blank=True)
    modified_at = models.DateTimeField(auto_now=True,null=True,blank=True)

    def __str__(self):
        return f"Daily Update for {self.haccp_link}"

