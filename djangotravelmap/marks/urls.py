from django.urls import path
from . import views

urlpatterns = [
    path('', views.marks_home), # Обращение к методу(не вызов)
]
