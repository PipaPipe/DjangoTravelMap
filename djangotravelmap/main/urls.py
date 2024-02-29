from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index), # Обращение к методу(не вызов)
    path('add', views.about),
    path('entry/', include('users_app.urls')),
]