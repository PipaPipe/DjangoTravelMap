from django.urls import path, include
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name = 'home'), # Обращение к методу(не вызов)
    path('add', views.about, name='about'),
    path('entry/', include('users_app.urls', namespace="users_app")),
]
