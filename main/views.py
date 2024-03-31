import json

from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from django.contrib.auth import get_user
from .models import *


class FetchHandler(View):
    def get(self, request):
        content_list = list(Mark.objects.filter(user_id=request.user.id).values('content_id'))
        content_indexes = [elem['content_id'] for elem in content_list]

        content = list(Content.objects.filter(id__in=content_indexes).values('id', 'title', 'description'))
        photos = list(Photo.objects.filter(content_id__in=content_indexes).values('id', 'photo', 'content_id'))

        marks = list(Mark.objects.filter(user_id=request.user.id).values('latitude', 'longitude', 'content_id',
                                                                              'user_id'))
        context = {
            'marks': marks,
            'content': content,
            'photos': photos
        }

        # if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        #     return JsonResponse({'Uknown': 1})
        # #print(request.user.id)
        return render(request, 'main/index.html', context)

    def post(self, request):
        # Получаем значения из ответа
        values = json.loads(request.body.decode('utf-8'))

        user = get_user(request)
        #
        content = Content.objects.create(title=values['title'], description=values['description'])
        for source in values['sources']:
            Photo.objects.create(photo=source, content_id=content)
        Mark.objects.create(latitude=values['lat'], longitude=values['lng'], user_id=user, content_id=content)


        print('Выполнение POST-запроса')

        return JsonResponse({'val': 'data'}, status=200)
        # print(f)
        # return JsonResponse()


def index(request):
    # №context = {'marks': list(Mark.objects.values('latitude', 'longitude', 'content_id', 'user_id'))}
    # print(context)
    return render(request, 'main/index.html')


def about(request):
    return render(request, 'main/add.html')
