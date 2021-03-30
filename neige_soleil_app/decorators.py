from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    """
    Vérifie si un user n'est pas authentifier
    """

    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main_home')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def no_profile(view_func):
    """
    Vérifie si un user n'as pas de profile
    """

    def wrapper_func(request, *args, **kwargs):
        try:
            if request.user.profile:
                return redirect('main_home')
        except ObjectDoesNotExist:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def known_profile(view_func):
    """
    Vérifie si un utilisateur a un profile ou non
    """

    def wrapper_func(request, *args, **kwargs):
        try:
            if request.user.profile:
                return view_func(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return redirect('new_profile')

    return wrapper_func


def known_proprietaire(view_func):
    """
    Vérifie si un utilisateur est un proprietaire
    """
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_proprietaire:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('main_home')
    return wrapper_func
