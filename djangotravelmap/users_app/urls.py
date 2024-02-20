from django.template.defaulttags import url
from django.urls import path
from . import views

urlpatterns = [
    path('/registration', views.RegisterFormView.as_view(), name='reg'), # Вызываем класс как представление
    path('/authorization', views.LoginFormView.as_view(), name='auth'),
    path('/logout', views.logout_user, name='logout')

    # path(url('reg1') , views.registration, name='auth2'),  # Обращение к методу(не вызов)
    # path(url('auth1'), views.authorization, name='reg2')

    # path('logout', views.LogoutView.as_view())
]
