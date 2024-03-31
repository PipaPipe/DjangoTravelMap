import json

from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from django.contrib.auth import get_user
from .models import *


class FetchHandler(View):
    def get(self, request):
        context = {
            'marks': list(Mark.objects.filter(user_id=request.user.id).values('latitude', 'longitude', 'content_id',
                                                                              'user_id'))}

        # if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        #     return JsonResponse({'Uknown': 1})
        # #print(request.user.id)
        return render(request, 'main/index.html', context)

    def post(self, request):
        values = json.loads(request.body.decode('utf-8'))
        print(type(values))
        user = get_user(request)
        print(values['title'])
        content = Content.objects.create(title=values['title'], description=values['description'])
        for source in values['sources']:
            Photo.objects.create(photo=source, content_id=content)
        Mark.objects.create(latitude=values['lat'], longitude=values['lng'], user_id=user, content_id=content)
        print(request.user.id)

        print(values)

        print('Выполнение POST-запроса')
        # data = json.loads(request.body)
        # print(data['lng'], data['lat'])
        # res = json.loads(data)
        # print(data)
        return JsonResponse({'val': 'data'}, status=200)
        # print(f)
        # return JsonResponse()


def index(request):
    # №context = {'marks': list(Mark.objects.values('latitude', 'longitude', 'content_id', 'user_id'))}
    # print(context)
    return render(request, 'main/index.html')


def about(request):
    return render(request, 'main/add.html')
