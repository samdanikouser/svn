from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """User Profile model, created on creating user while registration"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=[('admin', 'Admin'), ('line_staff', 'Line Staff'),
                                                    ('supervisors', 'Supervisors'),('managers','Managers'),('e_learning','e-Learning')])
    status = models.BooleanField(default=True)
    # face_data = models.BinaryField()

    def __str__(self):
        """string representation of the object"""
        return f"{self.user.username}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Signal function used to create entry in user profile table on creating a entry in user table(model)"""
    if created:
        UserProfile.objects.create(user=instance)


post_save.connect(create_user_profile, sender=User)