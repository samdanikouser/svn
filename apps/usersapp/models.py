# from datetime import datetime
# from django.db import models

# from apps.authentication.models import UserProfile
# from apps.correctiveaction.models import CorrectiveAction

# class DailyUpdates(models):
#     id = models.AutoField(primary_key=True)
#     haccp_link = models.OneToOneField('HaccpLink', on_delete=models.CASCADE,null=True,blank=True)
#     min_value = models.FloatField()
#     max_value = models.FloatField()
#     corrective_actions = models.ManyToManyField(CorrectiveAction, related_name='daily_updates',blank=True)
#     text_message = models.TextField(null=True,blank=True)
#     supervisor_approved_by = models.CharField(max_length=200, null=True, blank=True)
#     manager_approved_by = models.CharField(max_length=200, null=True, blank=True)
#     supervisor_comments = models.TextField(null=True,blank=True)
#     created_by = models.ForeignKey(UserProfile, related_name='created_daily_updates', on_delete=models.SET_NULL, null=True)
#     modified_by = models.ForeignKey(UserProfile, related_name='modified_daily_updates', on_delete=models.SET_NULL, null=True)
#     created_at = models.DateTimeField(default=datetime.now,null=True,blank=True)
#     modified_at = models.DateTimeField(auto_now=True,null=True,blank=True)

#     def __str__(self):
#         return f"Daily Update for {self.haccp_link}"

