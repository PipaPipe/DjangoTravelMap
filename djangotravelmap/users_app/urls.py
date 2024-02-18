from django.urls import path
from . import views

urlpatterns = [
    path('', views.selection),
    # path('registration', views.registration), # Обращение к методу(не вызов)
    # path('authorization', views.authorization)
    # path('logout', views.LogoutView.as_view())
]
