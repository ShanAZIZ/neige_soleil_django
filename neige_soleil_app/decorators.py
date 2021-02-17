from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home_main')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def known_profile(view_func):
    def wrapper_func(request, *args, **kwargs):
        try:
            val = request.user.profile
            return view_func(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return redirect('home_main')
    return wrapper_func