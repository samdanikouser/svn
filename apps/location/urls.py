from django.urls import path

from . import views

urlpatterns = [
    path('list', views.location_list, name='locationlist'),
    path('add', views.add_location, name='addlocation'),
    path('delete/<int:id>', views.delete_location, name='deletelocation'),
    path('update/<int:id>', views.update_location, name='updatelocation'),
    path('<str:name>/control_point/add', views.add_control_point, name='add_control_point'),
    path('control-point/list/<int:id>',views.list_control_point, name='list_control_point'),
    path('control_point/update/<int:id>',views.update_control_point,name='update_control_point'),
    path('control_point/delete/<int:id>',views.delete_control_point,name='delete_control_point'),
    path('corrective_actions/list/<int:id>', views.list_corrective_actions, name='list_corrective_actions'),
    path('corrective_actions/add/<int:id>', views.add_corrective_actions, name='add_corrective_actions'),
    path('corrective_actions/delete/<int:id>', views.delete_corrective_actions, name='delete_corrective_actions'),
    path('corrective_actions/update/<int:id>', views.update_corrective_actions, name='delete_corrective_actions')
]