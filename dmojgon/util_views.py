from django.contrib.auth import logout, login, authenticate
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import redirect, render

from response_utils import rej_error


def logout_view(request):
    logout(request)
    return redirect('index')


def login_request_view(request: WSGIRequest):
    if not request.user.is_anonymous:
        return rej_error('User already logged in!')

    new_user = authenticate(username=request.POST.get('username', ''), password=request.POST.get('password', ''))
    if new_user is None:
        return rej_error('Incorrect credentials!', page='login')
    else:
        login(request, new_user)
        return redirect('index')


def login_view(request: WSGIRequest):
    return render(request, 'login.html', {
        'error': request.GET.get('error', '')
    })
