from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import UserCreationForm, ContratProprietaireFrom, ProfileForm
from django.contrib.auth.decorators import login_required
from .models import *


def accueil(request):
    context = {}
    return render(request, 'neige_soleil_app/home_guest.html', context)


def register(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            #messages.success(request, 'account was created for ' + username)
            return redirect('login')
    context = {
        'form': form,
    }
    return render(request, 'neige_soleil_app/register.html', context)


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home_main')
        else:
            messages.info(request, 'Username or Password is incorrect')
    context = {}
    return render(request, 'neige_soleil_app/login.html', context)


@login_required(login_url='login')
def logoutPage(request):
    logout(request)
    return redirect('/')


@login_required(login_url='login')
def home_main(request):
    contrat_prop = ContratProprietaire.objects.all()
    context = {
        'contrats': contrat_prop,
    }
    return render(request, 'neige_soleil_app/home_main.html', context)


@login_required(login_url='login')
def profile(request):
    if request.method == 'POST':
        profile = ProfileForm(request.POST)
        if profile.is_valid():
            profile.save()
            return redirect('accueil')
    context = {}
    return render(request, 'neige_soleil_app/profile_set_main.html', context)


@login_required(login_url='login')
def proprietaire_main(request):
    contrat = ContratProprietaire.objects.filter(user=request.user)
    context = {
        'contrats': contrat
    }
    return render(request, 'neige_soleil_app/proprietaire_main.html', context)


@login_required(login_url='login')
def new_location(request):
    ContratProp = ContratProprietaireFrom(initial={'user': request.user.id})

    if request.method == 'POST':
        print(request.POST)
        ContratProp = ContratProprietaireFrom(request.POST)
        images = request.FILES.getlist('images')
        if ContratProp.is_valid():
            contrat = ContratProp.save()
            ProprietePrix.objects.create(location=contrat, prix=request.POST['prix'])
            for image in images:
                ProprieteImage.objects.create(location=contrat, image=image)
            return redirect('proprietaire')
    context = {
        'form': ContratProp,
    }
    return render(request, 'neige_soleil_app/ajout_location_main.html', context)


@login_required(login_url='login')
def location_detail(request, pk):
    location = ContratProprietaire.objects.get(id=pk)
    context = {
        'contrat': location
    }
    return render(request, 'neige_soleil_app/location_detail_main.html', context)