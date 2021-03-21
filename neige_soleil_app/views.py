"""
TODO: FEATURE - Vue de Mise a jour des images de proprietes
TODO: PROJET - Vue de modification des locations(A voir)
TODO: DEBUG - Effectuer un refactor des vues(Utiliser les class based View)
TODO: PROJET - Revoir la logique des bases user et de l'authentification
"""

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.utils.dateparse import parse_date

from .forms import *
from .decorators import unauthenticated_user, known_profile, known_proprietaire, no_profile
from .models import *


def accueil(request):
    """
    Page d'accueil publique de l'application
    Aucune restriction appliquer

    TODO: PROJET -Gerer l'affichage des biens reservables

    """
    context = {}
    return render(request, 'neige_soleil_app/guest_home.html', context)


############################################################################################
# AUTHENTIFICATION
############################################################################################
@unauthenticated_user
def register(request):
    """
    Page de creation de compte utilisateur
    Creation d'un utilisateur dans la table user de Django
    Restriction: User non authentifies

    TODO : FEATURE - Rediger le message d'erreur

    """
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            login(request, user)
            return redirect('main_home')
        else:
            messages.error(request, "Entrez des informations correcte et suffisant (longueur de mot de passe 8 caractères")
    context = {
        'form': form,
    }
    return render(request, 'neige_soleil_app/auth_register.html', context)


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
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main_home')
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect')
    context = {}
    return render(request, 'neige_soleil_app/auth_login.html', context)


@login_required(login_url='login')
def logoutPage(request):
    """
    Page de deconnexion, utilise la methode logout de Django
    Restriction: User authentifier
    """
    logout(request)
    return redirect('/')


def edit_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Votre mot de passe a bien été mis a jour")
            return redirect('detail_profile')
    context = {}
    return render(request, 'neige_soleil_app/main_edit_password.html', context)


############################################################################################
# VUES GENERALES
############################################################################################
@login_required(login_url='login')
def main_home(request):
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
    TODO: FEATURE Optimiser les visuels et ajouter des options
    """
    reservations = Reservation.objects.filter(profile=request.user.profile.id, location__isnull=True)
    locations = Location.objects.filter(reservation__profile=request.user.profile.id)

    context = {
        'reservations': reservations,
        'locations': locations
    }
    return render(request, 'neige_soleil_app/main_dashboard.html', context)


############################################################################################
# PROFILES
############################################################################################
@login_required(login_url='login')
@no_profile
def new_profile(request):
    """
    Page de creation du profile utilisateur
    Utilise la table Profile
    Permet de completer les informations d'un utilisateur
    Restriction: User authentifier

    TODO : FEATURE - Gerer les messages d'erreurs du formulaire
    TODO : FEATURE - Ajouter une photo de profile (Optionnel)

    """
    if request.method == 'POST':
        profile = ProfileForm(request.POST)
        if profile.is_valid():
            form = profile.save(commit=False)
            form.user = request.user
            form.save()
            return redirect('main_home')
    context = {}
    return render(request, 'neige_soleil_app/main_new_profile.html', context)


@login_required(login_url='login')
@known_profile
def edit_profile(request):
    edit = True
    if request.method == 'POST':
        formProfile = ProfileForm(request.POST, instance=request.user.profile)
        formUser = UserInfoUpdateForm(request.POST, instance=request.user)
        if formProfile.is_valid() and formUser.is_valid():
            formProfile.save()
            formUser.save()
            return redirect('detail_profile')
    context = {
        'edit': edit
    }
    return render(request, 'neige_soleil_app/main_edit_profile.html', context)


@login_required(login_url='login')
@known_profile
def detail_profile(request):
    context = {}
    return render(request, 'neige_soleil_app/main_detail_profile.html', context)


############################################################################################
# LES PROPRIETAIRES/HOTES
############################################################################################
@login_required(login_url='login')
@known_profile
def new_proprietaire(request):
    if request.method == 'POST':
        form = ProfileProprietaireForm(request.POST)
        if form.is_valid():
            prop = form.save(commit=False)
            prop.profile = request.user.profile
            prop.save()
            return redirect('main_proprietaire')
    context = {}
    return render(request, 'neige_soleil_app/main_new_proprietaire.html', context)


@login_required(login_url='login')
@known_profile
@known_proprietaire
def edit_proprietaire(request):
    if request.method == 'POST':
        form = ProfileProprietaireForm(request.POST, instance=request.user.profile.profileproprietaire)
        if form.is_valid():
            form.save()
            return redirect('main_proprietaire')
    context = {}
    return render(request, 'neige_soleil_app/main_new_proprietaire.html', context)


@login_required(login_url='login')
@known_profile
@known_proprietaire
def main_proprietaire(request):
    """
    Vue espace proprietaire, elle affiche les contrats du proprietaire et
    lui permet de se rediriger vers l'ajout de nouveaux contrats
    Restriction: User authentifier, avec Profile
    TODO: PROJET - Terminer le front end de la vue main_proprietaire

    """
    contrat = ContratProprietaire.objects.filter(profileproprietaire=request.user.profile.profileproprietaire)
    context = {
        'contrats': contrat
    }
    return render(request, 'neige_soleil_app/main_proprietaire.html', context)


############################################################################################
# LES PROPRIETES
############################################################################################
@login_required(login_url='login')
@known_profile
@known_proprietaire
def new_propriete(request):
    """
    Vue qui permet de créer un contrat d'un proprietaire
    Restriction: User authentifier, avec Profile
    """
    if request.method == 'POST':
        ContratPropForm = ContratProprietaireFrom(request.POST)
        images = request.FILES.getlist('images')
        if ContratPropForm.is_valid():
            contrat = ContratPropForm.save(commit=False)
            contrat.profileproprietaire = request.user.profile.profileproprietaire
            contrat.save()
            for image in images:
                ProprieteImage.objects.create(propriete=contrat, image=image)
            return redirect('main_proprietaire')
    context = {}
    return render(request, 'neige_soleil_app/main_new_propriete.html', context)


@login_required(login_url='login')
@known_profile
def edit_propriete(request, pk):
    contrat = ContratProprietaire.objects.get(id=pk)
    if contrat.profileproprietaire == request.user.profile.profileproprietaire:
        if request.method == 'POST':
            contratEditForm = ContratProprietaireFrom(request.POST, instance=contrat)
            if contratEditForm.is_valid():
                contratEditForm.save()
                return redirect('main_proprietaire')
        context = {
            'contrat': contrat
        }
        return render(request, 'neige_soleil_app/main_edit_propriete.html', context)
    else:
        return redirect('dashboard')


@login_required(login_url='login')
def detail_propriete(request, pk):
    """
    Vue qui affiche les détails d'un contrat proprietaire et permet de reservation un bien
    Restriction: User authentifier

    TODO: PROJET - Affichage sans authentification necessaire, mais avec contrainte

    """
    contrat = ContratProprietaire.objects.get(id=pk)
    reservations = contrat.reservation_set.all()
    context = {
        'contrat': contrat,
        'reservations': reservations
    }
    return render(request, 'neige_soleil_app/main_detail_propriete.html', context)


############################################################################################
# LES RESERVATIONS
############################################################################################
@login_required(login_url='login')
@known_profile
def new_reservation(request, pk):
    """
    Vue de reservation
    Restriction: User authentifier,  avec Profile
    TODO: DEBUG - Empecher le propriete d'acceder a cette vue par l'url
    """
    contrat = ContratProprietaire.objects.get(id=pk)
    reservations = contrat.reservation_set.all()
    if request.method == "POST":
        resForm = ReservationForm(request.POST)
        date_debut_sejour = parse_date(request.POST['date_debut_sejour'])
        date_fin_sejour = parse_date(request.POST['date_fin_sejour'])
        if contrat.is_avail(date_debut_sejour, date_fin_sejour):
            if resForm.is_valid():
                res = resForm.save(commit=False)
                res.profile = request.user.profile
                res.propriete = contrat
                res.save()
                return redirect('dashboard')
        else:
            messages.error(request, 'Cette propriete est deja reservée a cette date')
    context = {
        'reservations': reservations
    }
    return render(request, 'neige_soleil_app/main_new_reservation.html', context)


def edit_reservation(request, pk):
    reservation = Reservation.objects.get(id=pk)
    contrat = ContratProprietaire.objects.get(id=reservation.propriete.id)
    reservations = contrat.reservation_set.exclude(id=pk)
    if request.method == 'POST':
        resForm = ReservationForm(request.POST, instance=reservation)
        date_debut_sejour = parse_date(request.POST['date_debut_sejour'])
        date_fin_sejour = parse_date(request.POST['date_fin_sejour'])
        if contrat.is_avail(date_debut_sejour, date_fin_sejour, pk):
            if resForm.is_valid():
                res = resForm.save(commit=False)
                res.profile = request.user.profile
                res.propriete = contrat
                res.save()
                return redirect('dashboard')
        else:
            messages.error(request, 'Cette propriete est deja reservée a cette date')
    context = {
        'reservation': reservation,
        'reservations': reservations,
    }
    return render(request, 'neige_soleil_app/main_edit_reservation.html', context)


def cancel_reservation(request, pk):
    context = {}
    return render(request, 'neige_soleil_app/main_cancel_reservation.html', context)


############################################################################################
# LES LOCATIONS
############################################################################################
@login_required(login_url='login')
@known_profile
def new_location(request, pk):
    """
    Vue qui permet de generer une location (Page de confirmation de location)
    Restriction: User authentifier, avec Profile
    """
    reservation = Reservation.objects.get(id=pk)
    if request.method == 'POST':
        Location.objects.create(reservation=reservation)
        reservation.status_reservation = 'LOCATION'
        reservation.save()
        return redirect('dashboard')
    context = {
        'reservation': reservation,
    }
    return render(request, 'neige_soleil_app/main_confirm_reservation.html', context)






