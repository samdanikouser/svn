from django.urls import path

from . import views

urlpatterns = [
    path('/list', views.action_list, name='action_list'),
    path('/add', views.add_action, name='add_action'),
    path('/delete/<int:id>', views.delete_action, name='delete_action'),
    path('/update/<int:id>', views.update_action, name='update_action'),

]