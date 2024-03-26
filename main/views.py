import json

from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse


class FetchHandler(View):
    def get(self, request):
        # if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        #     return JsonResponse({'Uknown': 1})
        # #print(request.user.id)
        return render(request, 'main/index.html')

    def post(self, request):
        print(request.POST)
        #data = json.loads(request.body)
        # print(data['lng'], data['lat'])
        # res = json.loads(data)
        #print(data)
        return JsonResponse({'val': 'data'}, status=200)
        #print(f)
        # return JsonResponse()


def index(request):
    return render(request, 'main/index.html')


def about(request):
    return render(request, 'main/add.html')

