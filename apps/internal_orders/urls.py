from django.urls import path

from . import views

urlpatterns = [
    path('/add', views.internal_orders, name='internal_orders'),
]