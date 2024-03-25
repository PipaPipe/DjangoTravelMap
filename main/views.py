from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse


class FetchHandler(View):
    def get(self, request):
            # return JsonResponse({'Uknown': 1})
        print(request.user.id)
        return render(request, 'main/index.html')


def index(request):
    return render(request, 'main/index.html')

def about(request):
    return render(request, 'main/add.html')

