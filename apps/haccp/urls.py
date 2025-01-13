from django.urls import path
from . import views

urlpatterns = [
    path('list', views.HaccpList, name='haccp_list'),
    path('delete/<int:id>', views.HaccpDelete, name='haccp_delete'),
    path('<str:name>/', views.haccpHome, name='haccp_home'),
    path('<str:name>/<str:control_point>/', views.storagelocation, name='storage_location'),
    path('admin/<str:name>/<str:status>/', views.storagelocationAdminData, name='storage_data_admin_data'),
]
