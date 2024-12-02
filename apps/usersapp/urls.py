from django.urls import path

from . import views

urlpatterns = [
    path('/daily_activity/', views.daily_activity, name='daily_activity'),
    path('/daily_activity/user/check-range/', views.check_range, name='check_range'),
    path('/daily_activity/user/save-data/', views.save_data, name='save_data'),
    path('/daily_activity/user/check-daily-update/', views.check_daily_update, name='check_daily_update'),
    path('/pending_approvals/', views.pending_approvals, name='pending_approvals'),
    path('/approve_tasks/', views.approve_tasks, name='approve_tasks'),

]