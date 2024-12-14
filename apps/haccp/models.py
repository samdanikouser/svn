from django.db import models
from django.contrib.auth.models import User
from apps.location.models import ControlPoint, Location


class Day(models.Model):
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]

    name = models.CharField(max_length=10, choices=DAY_CHOICES, unique=True)

    def __str__(self):
        return self.name

class HaccpAdminData(models.Model):
    id = models.AutoField(primary_key=True)
    storage_location = models.ForeignKey(Location, on_delete=models.CASCADE,null=True, blank=True)
    sub_storage_location = models.ForeignKey(ControlPoint, on_delete=models.CASCADE,null=True, blank=True)
    name = models.CharField(max_length=200)
    used_for = models.CharField(max_length=200)
    assign_task_to = models.CharField(max_length=200)
    repeat_every = models.IntegerField()
    repeat_frequency = models.CharField(max_length=200)
    time_on = models.JSONField()
    min_temp = models.FloatField()
    max_temp = models.FloatField()
    corrective_action = models.ManyToManyField('correctiveaction.CorrectiveAction')
    assign_verifiers = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='created_haccp_admin_updates', on_delete=models.SET_NULL, null=True)
    modified_by = models.ForeignKey(User, related_name='modified_haccp_admin_updates', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name[:50]
    

class CoolingData(models.Model):
    id = models.AutoField(primary_key=True)
    storage_location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    sub_storage_location = models.ForeignKey(ControlPoint, on_delete=models.CASCADE, null=True, blank=True)
    food_item = models.CharField(max_length=255)  # Food item name or description
    internal_temp_at_0_hrs = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Temperature at 0 hours
    internal_temp_at_1_hrs = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Temperature at 1 hour
    internal_temp_at_2_hrs = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Temperature at 2 hours
    internal_temp_at_3_hrs = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Temperature at 3 hours
    internal_temp_at_4_hrs = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Temperature at 4 hours
    internal_temp_at_5_hrs = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Temperature at 5 hours
    internal_temp_at_6_hrs = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Temperature at 6 hours
    cooling_methods = models.CharField(max_length=255, null=True, blank=True)  # Cooling methods used
    data_entered_by = models.ForeignKey(User, related_name='entered_cooling_data', on_delete=models.SET_NULL, null=True)
    corrective_actions = models.TextField(null=True,blank=True)
    text_message = models.TextField(null=True,blank=True)
    supervisor_approved_by = models.CharField(max_length=200, null=True, blank=True)
    supervisor_approved_status = models.CharField(max_length=200, null=True, blank=True)
    manager_approved_by = models.CharField(max_length=200, null=True, blank=True)
    manager_approved_status = models.CharField(max_length=200, null=True, blank=True)
    supervisor_comments = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='created_cooling_updates', on_delete=models.SET_NULL, null=True)
    modified_by = models.ForeignKey(User, related_name='modified_cooling_updates', on_delete=models.SET_NULL, null=True)

def __str__(self):
        return f"{self.food_item} - {self.storage_location} ({self.created_at})"



class CookingData(models.Model):
    id = models.AutoField(primary_key=True)
    storage_location = models.ForeignKey(Location, on_delete=models.CASCADE,null=True, blank=True)
    sub_storage_location = models.ForeignKey(ControlPoint, on_delete=models.CASCADE,null=True, blank=True)
    


class ReHeatingData(models.Model):
    id = models.AutoField(primary_key=True)
    storage_location = models.ForeignKey(Location, on_delete=models.CASCADE,null=True, blank=True)
    sub_storage_location = models.ForeignKey(ControlPoint, on_delete=models.CASCADE,null=True, blank=True)


