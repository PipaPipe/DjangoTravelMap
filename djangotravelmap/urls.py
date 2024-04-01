# Отслеживает url-адреса
from django.contrib import admin
from django.urls import path, include

app_name = 'djangotravelmap'

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('users_app.urls'), name='users_app'),  # Обращаемся к файлу др. приложения(через include)

    # path('marks', include('marks.urls'), name='marks'),

    # path('entry', include('users_app.urls'))

    # path('authorization', include('users_app.urls'), name='auth1'),
    # path('registration', include('users_app.urls'), name='reg1'),

]
