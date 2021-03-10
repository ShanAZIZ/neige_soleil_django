"""
TODO: Vue de modification du profile des info user et des info proprietaire si il y en a
TODO: Vue de Modification des proprietes
TODO: Vue de modification des reservations
TODO: Vue de modification des locations(A voir)
"""

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.utils.dateparse import parse_date

from .forms import UserCreationForm, ContratProprietaireFrom, ProfileForm, ReservationForm, ProfileProprietaireForm
from .decorators import unauthenticated_user, known_profile, known_proprietaire
from .models import *


def accueil(request):
    """
    Page d'accueil publique de l'application
    Aucune restriction appliquer
    """
    context = {}
    return render(request, 'neige_soleil_app/guest_home.html', context)


@unauthenticated_user
def register(request):
    """
    Page de creation de compte utilisateur
    Creation d'un utilisateur dans la table user de Django
    Restriction: User non authentifies

    TODO : Gerer les messages d'erreurs sur la creation de compte selon les Rules Django

    """
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            login(request, user)
            return redirect('home_main')
    context = {
        'form': form,
    }
    return render(request, 'neige_soleil_app/register.html', context)


@unauthenticated_user
def loginPage(request):
    """
    Page de connexion
    Recuperer les infos de connexion et authentifier l'utilisateur avec le systeme d'auth de
    Django
    Restriction: User non authentifies
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home_main')
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect')
    context = {}
    return render(request, 'neige_soleil_app/login.html', context)


@login_required(login_url='login')
def logoutPage(request):
    """
    Page de deconnexion, utilise la methode logout de Django
    Restriction: User authentifier
    """
    logout(request)
    return redirect('/')


@login_required(login_url='login')
def profile_set(request):
    """
    Page de creation du profile utilisateur
    Utilise la table Profile
    Permet de completer les informations d'un utilisateur
    Restriction: User authentifier

    TODO : Gerer les messages d'erreurs du formulaire
    TODO : Ajouter une photo de profile (Optionnel)

    """
    if request.method == 'POST':
        profile = ProfileForm(request.POST)
        if profile.is_valid():
            profile.save()
            return redirect('home_main')
    context = {}
    return render(request, 'neige_soleil_app/main_profile_set.html', context)


@login_required(login_url='login')
def home_main(request):
    """
    Page d'accueil pour les utilisateurs Authentifies
    Recupere les proprietés et les affiches
    Restriction: User authentifier
    """
    try:
        contrat_prop = ContratProprietaire.objects.exclude(profileproprietaire=request.user.profile.profileproprietaire.id)
    except ObjectDoesNotExist:
        contrat_prop = ContratProprietaire.objects.all()
    context = {
        'contrats': contrat_prop,
    }
    return render(request, 'neige_soleil_app/main_home.html', context)


@login_required(login_url='login')
@known_profile
def dashboard(request):
    """
    Vue dashboard
    Restriction: User authentifier, avec Profile
    TODO: Optimiser les visuels et ajouter des options
    """
    reservations = Reservation.objects.filter(profile=request.user.profile.id, location__isnull=True)
    locations = Location.objects.filter(reservation__profile=request.user.profile.id)

    context = {
        'reservations': reservations,
        'locations': locations
    }
    return render(request, 'neige_soleil_app/main_dashboard.html', context)


@login_required(login_url='login')
@known_profile
def new_proprietaire(request):
    if request.method == 'POST':
        aproprietaireForm = ProfileProprietaireForm(request.POST)
        if aproprietaireForm.is_valid():
            aproprietaireForm.save()
            return redirect('proprietaire')
    context = {}
    return render(request, 'neige_soleil_app/main_new_proprietaire.html', context)


@login_required(login_url='login')
@known_profile
@known_proprietaire
def proprietaire_main(request):
    """
    Vue espace proprietaire, elle affiche les contrats du proprietaire et
    lui permet de se rediriger vers l'ajout de nouveaux contrats
    Restriction: User authentifier, avec Profile
    TODO: Ajouter des visuels de données interressant pour les Propriétaires

    """
    contrat = ContratProprietaire.objects.filter(profileproprietaire=request.user.profile.profileproprietaire)
    context = {
        'contrats': contrat
    }
    return render(request, 'neige_soleil_app/main_proprietaire.html', context)


@login_required(login_url='login')
@known_profile
@known_proprietaire
def new_propriete(request):
    """
    Vue qui permet de créer un contrat d'un proprietaire
    Restriction: User authentifier, avec Profile
    """
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
    return render(request, 'neige_soleil_app/main_new_propriete.html', context)


@login_required(login_url='login')
def propriete_detail(request, pk):
    """
    Vue qui affiche les détails d'un contrat proprietaire et permet de reservation un bien
    Restriction: User authentifier
    """
    contrat = ContratProprietaire.objects.get(id=pk)
    reservations = contrat.reservation_set.all()
    context = {
        'contrat': contrat,
        'reservations': reservations
    }
    return render(request, 'neige_soleil_app/main_propriete_detail.html', context)


@login_required(login_url='login')
@known_profile
def new_reservation(request, pk):
    """
    Vue de reservation
    Restriction: User authentifier,  avec Profile
    TODO: Verification des dates avant reservations et gestion du message d'erreur
    TODO: Empecher le proprietaire d'arriver a cet url manuellement
    """
    contrat = ContratProprietaire.objects.get(id=pk)
    reservations = contrat.reservation_set.all()
    if request.method == "POST":
        resForm = ReservationForm(request.POST)
        print(resForm)
        date_debut_sejour = resForm.cleaned_data.get('date_debut_sejour')
        date_fin_sejour = resForm.cleaned_data.get('date_fin_sejour')
        for reservation in contrat.reservation_set.all():
            if reservation.date_debut_sejour < date_debut_sejour < reservation.date_fin_sejour or reservation.date_debut_sejour < date_fin_sejour < reservation.date_fin_sejour:
                messages.error(request, 'Cette propriete est deja reservée a cette date')
                context = {
                    'contrat': contrat,
                    'reservations': reservations
                }
                return render(request, 'neige_soleil_app/main_new_reservation.html', context)
        if resForm.is_valid():
            resForm.save()
            return redirect('dashboard')
    context = {
        'contrat': contrat,
        'reservations': reservations
    }
    return render(request, 'neige_soleil_app/main_new_reservation.html', context)


@login_required(login_url='login')
@known_profile
def louer_propriete(request, pk):
    """
    Vue qui permet de generer une location (Page de confirmation de location)
    Restriction: User authentifier, avec Profile
    """
    reservation = Reservation.objects.get(id=pk)
    if request.method == 'POST':
        Location.objects.create(reservation=reservation)
        return redirect('dashboard')
    context = {
        'reservation': reservation,
    }
    return render(request, 'neige_soleil_app/main_confirm_reservation.html', context)