from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout


def index_view(request):

    return render(request, 'view_all_problems.html', {
        'user': request.user
    })


