from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Roles(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, unique=True, error_messages={"location": "Role name required"})
    created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='created_roles_updates', on_delete=models.SET_NULL, null=True)
    modified_by = models.ForeignKey(User, related_name='modified_roles_updates', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.name}"
