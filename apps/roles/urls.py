from django.urls import path

from . import views

urlpatterns = [
    path('/list', views.location_roles, name='roleslist'),
    path('/add', views.add_roles, name='addrole'),
    path('/delete/<int:id>', views.delete_roles, name='deleterole'),
    path('/update/<int:id>', views.update_roles, name='updatelrole'),

]