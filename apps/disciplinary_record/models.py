from django.db import models
from django.contrib.auth.models import User

from apps.authentication.models import UserProfile

# Create your models here.

class DisciplinaryRecord(models.Model):
    id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(UserProfile, on_delete=models.CASCADE,null=True, blank=True,related_name="disciplinary_record_employee")
    recorded_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE,null=True, blank=True,related_name="disciplinary_record_inspector")
    issues_realted_to = models.CharField(max_length=200,null=True,blank=True)
    incident_date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    inspector_signature = models.TextField(null=True, blank=True)
    employee_signature = models.TextField(null=True, blank=True)
    reason = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='created_disciplinary_record_updates', on_delete=models.SET_NULL, null=True)
    modified_by = models.ForeignKey(User, related_name='modified_disciplinary_record_updates', on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f"RAISED by {self.recorded_by} on {self.incident_date}"

