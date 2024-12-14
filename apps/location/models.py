from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class Location(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, unique=True, error_messages={"location": "Location name required"})
    status = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='created_location_updates', on_delete=models.SET_NULL, null=True)
    modified_by = models.ForeignKey(User, related_name='modified_location_updates', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.name}"


class ControlPoint(models.Model):
    id = models.AutoField(primary_key=True)
    location = models.ForeignKey(Location, related_name='control_points', on_delete=models.CASCADE,null=True, blank=True)
    name = models.CharField(max_length=100,null=True, blank=True)
    daily_activity = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='created_control_point_updates', on_delete=models.SET_NULL, null=True)
    modified_by = models.ForeignKey(User, related_name='modified_control_point_updates', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.name} at {self.location.name}" if self.location else "Location not specified"
