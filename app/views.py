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


# Decorator that fetches the problem
def fetch_problem_decorator(view):
    def wrapper(request, **kwargs):
        p = get_object_or_404(Problem, name=kwargs['name'])
        if request.user.is_anonymous or not p.owners.filter(id=request.user.id).exists():
            return rej_error(f'You cannot access problem {p.name}')
        return view(request, p, **kwargs)

    return wrapper


@fetch_problem_decorator
def problem_view(request, p, name):
    return render(request, 'problem_view/main.html', {
        'problem': p
    })


@fetch_problem_decorator
def problem_tests_view(request, p, name):
    return render(request, 'problem_view/tests.html', {
        'problem': p
    })


@fetch_problem_decorator
def problem_invocations_view(request, p, name):
    return render(request, 'problem_view/invocations.html', {
        'problem': p
    })


@fetch_problem_decorator
def problem_package_view(request, p, name):
    return render(request, 'problem_view/package.html', {
        'problem': p
    })


def wip_view(request, **kwargs):
    return render(request, 'wip.html')
