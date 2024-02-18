# Отслеживает url-адреса
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('main.urls')), # Обращаемся к файлу др. приложения(через include)

    path('marks', include('marks.urls')),

    path('entry', include('users_app.urls'))

    # path('authorization.html', include('users_app.urls'))
    # path('registration', include('users_app.urls')),

]
