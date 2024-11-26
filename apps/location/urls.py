from django.urls import path

from . import views

urlpatterns = [
    path('/list', views.location_list, name='locationlist'),
    path('/add', views.add_location, name='addlocation'),
    path('/delete/<int:id>', views.delete_location, name='deletelocation'),
    path('/update/<int:id>', views.update_location, name='updatelocation'),

]