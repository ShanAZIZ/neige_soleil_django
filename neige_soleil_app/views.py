from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import UserCreationForm


def accueil(request):
    context = {}
    return render(request, 'neige_soleil_app/guest_home.html', context)


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

def home_main(request):
    context = {}
    return render(request, 'neige_soleil_app/home_main.html', context)