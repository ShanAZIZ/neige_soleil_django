from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.utils.dateparse import parse_date

from .forms import UserCreationForm, ContratProprietaireFrom, ProfileForm, ReservationForm
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, known_profile
from .models import *


def accueil(request):
    context = {}
    return render(request, 'neige_soleil_app/guest_home.html', context)


@unauthenticated_user
def register(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            # messages.success(request, 'account was created for ' + username)
            return redirect('login')
    context = {
        'form': form,
    }
    return render(request, 'neige_soleil_app/register.html', context)


@unauthenticated_user
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
    contrat_prop = ContratProprietaire.objects.exclude(user=request.user.id)
    context = {
        'contrats': contrat_prop,
    }
    return render(request, 'neige_soleil_app/main_home.html', context)


@login_required(login_url='login')
def profile_set(request):
    if request.method == 'POST':
        profile = ProfileForm(request.POST)
        if profile.is_valid():
            profile.save()
            return redirect('home_main')
    context = {}
    return render(request, 'neige_soleil_app/main_profile_set.html', context)


@login_required(login_url='login')
@known_profile
def proprietaire_main(request):
    contrat = ContratProprietaire.objects.filter(user=request.user)
    context = {
        'contrats': contrat
    }
    return render(request, 'neige_soleil_app/main_proprietaire.html', context)


@login_required(login_url='login')
@known_profile
def new_propriete(request):
    ContratProp = ContratProprietaireFrom(initial={'user': request.user.id})

    if request.method == 'POST':
        ContratProp = ContratProprietaireFrom(request.POST)
        images = request.FILES.getlist('images')
        if ContratProp.is_valid():
            contrat = ContratProp.save()
            ProprietePrix.objects.create(propriete=contrat, prix=request.POST['prix'])
            for image in images:
                ProprieteImage.objects.create(propriete=contrat, image=image)
            return redirect('proprietaire')
    context = {
        'form': ContratProp,
    }
    return render(request, 'neige_soleil_app/main_ajout_location.html', context)


@login_required(login_url='login')
def propriete_detail(request, pk):
    if request.method == "POST":
        resForm = ReservationForm(request.POST)
        # Ajouter une verification des dates ici
        if resForm.is_valid():
            resForm.save()
    contrat = ContratProprietaire.objects.get(id=pk)
    reservations = contrat.reservation_set.all()
    context = {
        'contrat': contrat,
        'reservations': reservations
    }
    return render(request, 'neige_soleil_app/main_propriete_detail.html', context)


@login_required(login_url='login')
@known_profile
def dashboard(request):
    # Definir l'affichage du status des reservations et la mise en place des contrats de locations
    reservations = Reservation.objects.filter(profile=request.user.profile.id)
    context = {
        'reservations': reservations
    }
    return render(request, 'neige_soleil_app/dashboard.html', context)
