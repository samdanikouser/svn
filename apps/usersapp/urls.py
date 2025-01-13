from django.urls import path

from . import views

urlpatterns = [
    path('/daily_activity/', views.daily_activity, name='daily_activity'),
    path('/daily_activity/<str:location>', views.daily_activity, name='daily_activity'),
    path('/daily_activity/user/check-range/', views.check_range, name='check_range'),
    path('/daily_activity/user/save-data/', views.save_data, name='save_data'),
    path('/daily_activity/user/check-daily-update/', views.check_daily_update, name='check_daily_update'),
    path('/pending_approvals/', views.pending_approvals, name='pending_approvals'),
    path('/approve_tasks/', views.approve_tasks, name='approve_tasks'),
    path('/Cooling/add/<str:location>/', views.cooling_data_entry, name='cooling_data_entry'),
    path('/Cooling/add/', views.cooling_data_entry, name='cooling_data_entry'),
    path('/Cooling/view/<int:id>', views.cooling_data_view, name='cooling_data_view'),
    path('/Cooling/list/<str:location>/', views.cooling_data_list, name='cooling_data_list'),
    path('/Cooking/add/<str:location>/', views.cooking_data_entry, name='cooking_data_entry'),
    path('/Cooking/add/', views.cooking_data_entry, name='cooking_data_entry'),
    path('/Cooking/list/<str:location>/', views.cooking_data_list, name='cooking_data_list'),
    path('/Cooking/view/<int:id>', views.cooking_data_view, name='cooking_data_view'),
    path('/Re-Heating/add/<str:location>/', views.reheating_data_entry, name='reheating_data_entry'),
    path('/Re-Heating/add/', views.reheating_data_entry, name='reheating_data_entry'),
    path('/Re-Heating/list/<str:location>', views.reheating_data_list, name='reheating_data_list'),
    path('/Re-Heating/view/<int:id>', views.reheating_data_view, name='reheating_data_view'),

]