from django.urls import path

from . import views

urlpatterns = [
    path('/users_first_page', views.usersFirstDisplay, name='users_first_page'),
    path('/user_login/<str:name>', views.userLogin, name='user_login'),
]