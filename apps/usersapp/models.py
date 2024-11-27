from django.db import models

# Create your models here.
# class DailyUpdates(models):
#     pass


class Employees(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, unique=True)
    employee_id = models.IntegerField(unique=True)
    position = models.CharField(max_length=200, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"



