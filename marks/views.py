from django.http import HttpResponse
from django.shortcuts import render

def marks_home(request):
    # return HttpResponse('aa')
    return render(request, 'marks/marks_home.html')
    # return render(request, 'marks/index.html')
