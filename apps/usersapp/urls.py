from django.urls import path

from . import views

urlpatterns = [
    path('/users_first_page', views.usersFirstDisplay, name='users_first_page'),
    path('/user_login/<str:name>', views.userLogin, name='user_login'),
    path('/daily_activity/', views.daily_activity, name='daily_activity'),
    path('/daily_activity/user/check-range/', views.check_range, name='check_range'),
    path('/daily_activity/user/save-data/', views.save_data, name='save_data'),

]