from django.urls import path, include
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.FetchHandler.as_view(), name='map'), # Обращение к методу(не вызов)
    # path('entry/', include('users_app.urls', namespace="users_app")),

]
