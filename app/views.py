from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'view_all_problems.html')
