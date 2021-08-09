from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now

from .models import Problem
from response_utils import rej_error


def new_problem_view(request):
    name = request.GET.get('name')
    user = request.user

    # Errors:
    if len(name) < 1:
        return rej_error('No name specified!')
    if user.is_anonymous:
        return rej_error('Not logged in!')
    if Problem.objects.filter(name=name).exists():
        return rej_error(f'Problem named {name} already exists!')

    print(user.username)
    p = Problem.objects.create(name=name, last_modified=now())
    p.save()
    p.owners.add(user)

    return redirect('index')


def index_view(request):
    search = request.GET.get('search', '')
    error = request.GET.get('error')

    return render(request, 'view_all_problems.html', {
        'user': request.user,
        'search': search,
        'error': error,
        'problems': Problem.objects.filter(owners__in=[request.user], name__contains=search) if not request.user.is_anonymous else []
    })


def problem_view(request, pname):
    p = get_object_or_404(Problem, name=pname)
    if request.user not in p.owners:
        return rej_error(f'You cannot access problem {p.name}')


def wip_view(request, **kwargs):
    return render(request, 'wip.html')
