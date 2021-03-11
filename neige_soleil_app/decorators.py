from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    """
    Verifie si un user n'est pas authentifiers
    """
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main_home')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def known_profile(view_func):
    """
    Verifie si un utilisateur a un profile ou non
    """
    def wrapper_func(request, *args, **kwargs):
        try:
            val = request.user.profile
            return view_func(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return redirect('new_profile')

    return wrapper_func


def known_proprietaire(view_func):
    """
    Verifie si un utilisateur a un profile ou non
    """
    def wrapper_func(request, *args, **kwargs):
        try:
            val = request.user.profile.profileproprietaire
            return view_func(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return redirect('new_proprietaire')
    return wrapper_func