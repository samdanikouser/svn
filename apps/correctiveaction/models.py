from django.db import models


# Create your models here.

class CorrectiveAction(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, unique=True, error_messages={"action": "Action required"})
    status = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"
