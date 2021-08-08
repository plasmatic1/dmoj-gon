from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import reverse


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
