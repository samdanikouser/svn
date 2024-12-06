from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.department.models import Department


class UserProfile(models.Model):
    """User Profile model, created on creating user while registration"""
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True,blank=True)
    role = models.CharField(max_length=50, choices=[('admin', 'Admin'), ('line_staff', 'Line Staff'),
                                                    ('supervisor', 'Supervisor'),('managers','Managers'),('e_learning','e-Learning')],null=True,blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    employee_id = models.IntegerField(unique=True, null=True, blank=True)
    department = models.OneToOneField(Department, on_delete=models.CASCADE,null=True,blank=True)
    data_of_joining = models.DateField(null=True, blank=True)  # Changed to DateField
    job_title = models.CharField(max_length=200, null=True, blank=True)
    status = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # face_data = models.BinaryField()

    def __str__(self):
        """string representation of the object"""
        return f"{self.user.username}"


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     """Signal function used to create entry in user profile table on creating a entry in user table(model)"""
#     if created:
#         UserProfile.objects.create(user=instance)

# post_save.connect(create_user_profile, sender=User)




