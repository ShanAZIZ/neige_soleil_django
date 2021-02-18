from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, ContratProprietaire, ProprietePrix, Reservation


class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class ContratProprietaireFrom(ModelForm):
    class Meta:
        model = ContratProprietaire
        fields = '__all__'


class LocationSetPrix(ModelForm):
    class Meta:
        model = ProprietePrix
        fields = '__all__'


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'


class ReservationForm(ModelForm):
    class Meta:
        model = Reservation
        fields = '__all__'