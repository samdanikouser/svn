from django.urls import path

from . import views

urlpatterns = [
    path('/list', views.personalhygiene_list, name='personalhygiene_list'),
    path('/add', views.add_personalhygiene, name='add_personalhygiene'),
    path('/delete/<int:id>', views.delete_personalhygiene, name='delete_personalhygiene'),
    path('/update/<int:id>', views.update_personalhygiene, name='update_personalhygiene'),
]