from django.urls import path

from . import views

urlpatterns = [
    path('/list', views.department_list, name='departmentlist'),
    path('/add', views.add_department, name='adddepartment'),
    path('/delete/<int:id>', views.delete_department, name='deletedepartment'),
    path('/update/<int:id>', views.update_department, name='updatedepartment'),

]