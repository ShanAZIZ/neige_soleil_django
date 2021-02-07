from django.shortcuts import render


def accueil(request):
    context = {}
    return render(request, 'neige_soleil_apps/guest_home.html', context)
