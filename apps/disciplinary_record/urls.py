from django.urls import path

from . import views

urlpatterns = [
    path('/list/<int:id>', views.list_disciplinary_record, name='list_disciplinary_record'),
    path('/add', views.add_disciplinary_record, name='add_disciplinary_record'),
    path('/view/<int:id>', views.view_disciplinary_record, name='view_disciplinary_record')
]