from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.http import urlencode


def rej_error(error_str, page='index'):
    return HttpResponseRedirect(reverse(page) + '?' + urlencode({'error': error_str}))
