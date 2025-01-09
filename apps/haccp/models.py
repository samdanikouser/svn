from django.db import models
from django.contrib.auth.models import User
from apps.authentication.models import UserProfile
from apps.location.models import ControlPoint, Location
from django.core.exceptions import ValidationError


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
    food_item = models.CharField(max_length=255)
    internal_temp_at_0_hrs = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    internal_temp_at_1_hrs = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    internal_temp_at_2_hrs = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    internal_temp_at_3_hrs = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    internal_temp_at_4_hrs = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    internal_temp_at_5_hrs = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    internal_temp_at_6_hrs = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    cooling_methods = models.CharField(max_length=255, null=True, blank=True)
    data_entered_by = models.ForeignKey(UserProfile, related_name='entered_cooling_data', on_delete=models.SET_NULL, null=True)
    corrective_actions = models.TextField(null=True,blank=True)
    text_message = models.TextField(null=True,blank=True)
    supervisor_approved_by = models.CharField(max_length=200, null=True, blank=True)
    supervisor_approved_status = models.CharField(max_length=200, null=True, blank=True)
    manager_approved_by = models.CharField(max_length=200, null=True, blank=True)
    manager_approved_status = models.CharField(max_length=200, null=True, blank=True)
    supervisor_comments = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True, 
        blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True, 
        blank=True)
    created_by = models.ForeignKey(UserProfile, related_name='created_cooling_updates', on_delete=models.SET_NULL, null=True)
    modified_by = models.ForeignKey(UserProfile, related_name='modified_cooling_updates', on_delete=models.SET_NULL, null=True)

def __str__(self):
        return f"{self.food_item} - {self.storage_location} ({self.created_at})"


class CookingData(models.Model):
    id = models.AutoField(primary_key=True)
    storage_location = models.ForeignKey(Location,on_delete=models.CASCADE,null=True,blank=True)
    sub_storage_location = models.ForeignKey(ControlPoint,on_delete=models.CASCADE,null=True,blank=True)
    meal_period = models.CharField(max_length=100,null=True,blank=True)
    item_name = models.CharField(max_length=200,null=True,blank=True)
    time = models.TimeField(null=True,blank=True)
    temperature = models.DecimalField(max_digits=5,decimal_places=2,null=True,blank=True) 
    food_type = models.CharField(max_length=100,null=True,blank=True)
    supervisor_approved_by = models.CharField(max_length=200,null=True,blank=True)
    supervisor_approved_status = models.CharField(max_length=200,null=True,blank=True)
    corrective_actions = models.TextField(null=True,blank=True)
    text_message = models.TextField(null=True,blank=True)
    manager_approved_by = models.CharField(
        max_length=200, 
        null=True, 
        blank=True
    )
    manager_approved_status = models.CharField(
        max_length=200, 
        null=True, 
        blank=True
    )
    supervisor_comments = models.TextField(
        null=True, 
        blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,null=True, 
        blank=True
    )
    updated_at = models.DateTimeField(
        auto_now=True,null=True, 
        blank=True
    )
    created_by = models.ForeignKey(
        User, 
        related_name='created_cooking_data', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    modified_by = models.ForeignKey(
        User, 
        related_name='modified_cooking_data', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )

    def __str__(self):
        return f"CookingData {self.id} - {self.item_name or 'Unnamed'}"

    
class ReHeatingData(models.Model):
    id = models.AutoField(primary_key=True)
    storage_location = models.ForeignKey(
        Location, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    sub_storage_location = models.ForeignKey(
        ControlPoint, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    food_item = models.CharField(
        max_length=200, 
        null=True, 
        blank=True
    )
    date_of_reheating = models.DateField(
        null=True, 
        blank=True
    )
    reheating_temperature = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="Temperature must be at least 75°C"
    )
    time_taken_for_reheating = models.DurationField(
        null=True, 
        blank=True,
        help_text="Time must be less than 2 hours"
    )
    supervisor_approved_by = models.CharField(
        max_length=200, 
        null=True, 
        blank=True
    )
    supervisor_approved_status = models.CharField(
        max_length=200, 
        null=True, 
        blank=True
    )
    manager_approved_by = models.CharField(
        max_length=200, 
        null=True, 
        blank=True
    )
    manager_approved_status = models.CharField(
        max_length=200, 
        null=True, 
        blank=True
    )
    supervisor_comments = models.TextField(
        null=True, 
        blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,null=True, 
        blank=True
    )
    updated_at = models.DateTimeField(
        auto_now=True,null=True, 
        blank=True
    )
    created_by = models.ForeignKey(
        User, 
        related_name='created_reheating_data', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    modified_by = models.ForeignKey(
        User, 
        related_name='modified_reheating_data', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )

    def __str__(self):
        return f"ReHeatingData {self.id} - {self.food_item or 'Unnamed'}"
