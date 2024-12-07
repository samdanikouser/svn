from django.urls import path

from . import views

urlpatterns = [
    path('/list', views.personalhygiene_list, name='personalhygiene_list'),
    path('/add', views.add_personalhygiene, name='add_personalhygiene'),
    path('/delete/<int:id>', views.delete_personalhygiene, name='delete_personalhygiene'),
    path('/view/<int:id>', views.view_personalhygiene, name='view_personalhygiene'),
    path('download_filtered_pdf/', views.download_filtered_pdf, name='download_filtered_pdf'),

]