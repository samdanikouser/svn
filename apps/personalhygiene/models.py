from django.db import models

from apps.authentication.models import UserProfile

class PersonalHygiene(models.Model):
    id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(UserProfile, on_delete=models.CASCADE,null=True, blank=True,related_name="personal_hygiene_employee")
    inspected_date = models.DateField(null=True, blank=True)
    inspected_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE,null=True, blank=True,related_name="personal_hygiene_inspector")
    parameters_checked = models.TextField(null=True, blank=True)
    inspector_signature = models.TextField(null=True, blank=True)
    employee_signature = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=False)
    photos = models.ManyToManyField('UploadedPhoto', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Inspection by {self.inspected_by} on {self.inspected_date}"


class UploadedPhoto(models.Model):
    photo = models.ImageField(upload_to='personal_hygiene_photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo {self.id} uploaded on {self.uploaded_at}"
