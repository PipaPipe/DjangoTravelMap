from django.urls import path
from . import views

urlpatterns = [
    path('', views.index), # Обращение к методу(не вызов)
    path('add', views.about)
]
