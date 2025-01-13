from django.urls import path
from . import views

urlpatterns = [
    path('recognize_face/', views.recognize_face, name='recognize_face'),
]
