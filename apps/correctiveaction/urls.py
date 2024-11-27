from django.urls import path

from . import views

urlpatterns = [
    path('/list', views.action_list, name='action_list'),
    path('/add', views.add_action, name='add_action'),
    path('/delete/<int:id>', views.delete_action, name='delete_action'),
    path('/update/<int:id>', views.update_action, name='update_action'),
    path('employees/list', views.employee_list, name='employee_list'),
    path('employees/add', views.add_employee, name='add_'),
    path('employees/delete/<int:id>', views.delete_employee, name='delete_action'),
    path('employees/update/<int:id>', views.update_employee, name='update_action')
]