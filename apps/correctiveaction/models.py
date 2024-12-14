from django.db import models
from django.contrib.auth.models import User
from apps.haccp.models import ControlPoint


# Create your models here.

class CorrectiveAction(models.Model):
    id = models.AutoField(primary_key=True)
    control_point = models.ForeignKey(ControlPoint, related_name='corrective_actions', on_delete=models.CASCADE,null=True, blank=True)
    name = models.CharField(max_length=200, error_messages={"action": "Action required"})
    status = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='created_action_updates', on_delete=models.SET_NULL, null=True)
    modified_by = models.ForeignKey(User, related_name='modified_action_updates', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.name}"
    

    
