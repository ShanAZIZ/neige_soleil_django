from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.utils.dateparse import parse_date

from .forms import *
from .decorators import unauthenticated_user, known_profile, no_profile
from .models import *

# TODO: Suppression des images si suppression

@unauthenticated_user
def accueil(request):
    """
    Page d'accueil publique de l'application
    Aucune restriction appliquer
    """
    context = {}
    return render(request, 'neige_soleil_app/guest_home.html', context)


############################################################################################
# AUTHENTIFICATION
############################################################################################
@unauthenticated_user
def register(request):
    form = NewUserForm()
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            login(request, user)
            messages.success(request, " Votre compte à bien été créer "+username)
            return redirect('main_home')
        else:
            messages.error(request, "Entrez des informations correcte et suffisant (longueur de mot de passe 8 "
                                    "caractères minimum)")
    context = {
        'form': form,
    }
    return render(request, 'neige_soleil_app/auth_register.html', context)


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return redirect('neige_soleil_admin')
            return redirect('main_home')
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect')
    context = {}
    return render(request, 'neige_soleil_app/auth_login.html', context)


@login_required(login_url='login')
def logoutPage(request):
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
# VUES GÉNÉRALES
############################################################################################
@login_required(login_url='login')
def main_home(request):
    try:
        contrat_prop = ContratProprietaire.objects.exclude(user=request.user.id).filter(status='AVAIL')
    except ObjectDoesNotExist:
        contrat_prop = ContratProprietaire.objects.all()
    context = {
        'contrats': contrat_prop,
    }
    return render(request, 'neige_soleil_app/main_home.html', context)


@login_required(login_url='login')
@known_profile
def dashboard(request):
    reservations = Reservation.objects.filter(user=request.user.id, status_reservation='WAIT')
    reservations_annules = Reservation.objects.filter(user=request.user.id, status_reservation='CANCEL')
    locations = Reservation.objects.filter(user=request.user.id, status_reservation='LOCATION')

    context = {
        'reservations': reservations,
        'reservations_annules': reservations_annules,
        'locations': locations
    }
    return render(request, 'neige_soleil_app/main_dashboard.html', context)


############################################################################################
# PROFILES
############################################################################################
@login_required(login_url='login')
@no_profile
def new_profile(request):
    if request.method == 'POST':
        profile = ProfileForm(request.POST)
        if profile.is_valid():
            form = profile.save(commit=False)
            form.user = request.user
            form.save()
            return redirect('main_home')
        else :
            messages.error(request, 'Entrez correctement les données')
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
# LES PROPRIÉTAIRES/HÔTES
############################################################################################


@login_required(login_url='login')
@known_profile
def main_proprietaire(request):
    # TODO: Voir des infos tels que le nombre de locations et reservations
    contrat = ContratProprietaire.objects.filter(user=request.user)
    context = {
        'contrats': contrat
    }
    return render(request, 'neige_soleil_app/main_proprietaire.html', context)


############################################################################################
# LES PROPRIÉTÉS
############################################################################################
@login_required(login_url='login')
@known_profile
def new_propriete(request):
    if request.method == 'POST':
        ContratPropForm = ContratProprietaireFrom(request.POST)
        images = request.FILES.getlist('images')
        if ContratPropForm.is_valid():
            contrat = ContratPropForm.save(commit=False)
            contrat.user = request.user
            contrat.save()
            for image in images:
                ProprieteImage.objects.create(propriete=contrat, image=image)
            return redirect('main_proprietaire')
    context = {}
    return render(request, 'neige_soleil_app/main_new_propriete.html', context)


@login_required(login_url='login')
@known_profile
def edit_propriete(request, pk):
    # TODO: Mise a jour des images de propriétés
    contrat = ContratProprietaire.objects.get(id=pk)
    if contrat.user == request.user:
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
    contrat = ContratProprietaire.objects.get(id=pk)
    if contrat.user != request.user:
        reservations = contrat.reservation_set.all().exclude(status_reservation='CANCEL')
        if request.method == "POST":
            post_value = request.POST.copy()
            post_value['user'] = request.user.id
            post_value['propriete'] = contrat.id
            resForm = ReservationForm(post_value)
            if resForm.is_valid():
                resForm.save()
                return redirect('dashboard')
            else:
                messages.error(request, 'Cette propriete est deja réservée a cette date')
        context = {
            'reservations': reservations
        }
        return render(request, 'neige_soleil_app/main_new_reservation.html', context)
    return redirect('dashboard')


def edit_reservation(request, pk):
    reservation = Reservation.objects.get(id=pk)
    contrat = ContratProprietaire.objects.get(id=reservation.propriete.id)
    reservations = contrat.reservation_set.exclude(id=pk)
    if request.method == 'POST':
        post_value = request.POST.copy()
        post_value['user'] = request.user.id
        post_value['propriete'] = contrat.id
        resForm = ReservationForm(post_value, instance=reservation)
        if resForm.is_valid(reservation.id):
            res = resForm.save()
            return redirect('dashboard')
        else:
            messages.error(request, 'Cette propriete est deja réservée a cette date')
    context = {
        'reservation': reservation,
        'reservations': reservations,
    }
    return render(request, 'neige_soleil_app/main_edit_reservation.html', context)


def cancel_reservation(request, pk):
    reservation = Reservation.objects.get(id=pk)
    if request.method == 'POST':
        reservation.annuler_reservation()
        reservation.save()
        return redirect('dashboard')
    context = {
        'reservation': reservation,
    }
    return render(request, 'neige_soleil_app/main_cancel_reservation.html', context)


@login_required(login_url='login')
@known_profile
def confirm_reservation(request, pk):
    reservation = Reservation.objects.get(id=pk)
    if request.method == 'POST':
        reservation.status_reservation = 'LOCATION'
        reservation.save()
        return redirect('dashboard')
    context = {
        'reservation': reservation,
    }
    return render(request, 'neige_soleil_app/main_confirm_reservation.html', context)


############################################################################################
# LES RESERVATIONS
############################################################################################

@login_required(login_url='login')
@permission_required('is_superuser')
def admin_home(request):
    reservations = Reservation.objects.all()
    propriete = ContratProprietaire.objects.all()
    # TODO: Completer la vue admin
    return render(request, 'neige_soleil_app/main_admin_home.html')


