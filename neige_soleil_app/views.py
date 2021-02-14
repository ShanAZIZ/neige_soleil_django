from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import UserCreationForm, LocationCreationFrom
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
    context = {
        'row' : [1,2,3,4,5,6]
    }
    return render(request, 'neige_soleil_app/home_main.html', context)


@login_required(login_url='login')
def proprietaire_main(request):
    context = {}
    return render(request, 'neige_soleil_app/proprietaire_main.html', context)


@login_required(login_url='login')
def new_location(request):
    Locationform = LocationCreationFrom(initial={'user': request.user.id})

    if request.method == 'POST':
        print(request.POST)
        Locationform = LocationCreationFrom(request.POST)
        images = request.FILES.getlist('images')
        if Locationform.is_valid():
            location = Locationform.save()
            PrixLocation.objects.create(location=location, prix=request.POST['prix'])
            for image in images:
                LocationImage.objects.create(location=location, image=image)
            return redirect('proprietaire')
    context = {
        'form': Locationform,
    }
    return render(request, 'neige_soleil_app/ajout_location_main.html', context)

