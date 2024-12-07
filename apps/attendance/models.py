from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=100)
    facial_encoding = models.TextField()

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    time_in = models.DateTimeField()
    time_out = models.DateTimeField(null=True, blank=True)
