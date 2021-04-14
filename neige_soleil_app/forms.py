from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Utilisateur, Profile, ContratProprietaire, Reservation


class NewUserForm(UserCreationForm):
    class Meta:
        model = Utilisateur
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user']


class UserInfoUpdateForm(ModelForm):
    class Meta:
        model = Utilisateur
        fields = ['first_name', 'last_name', 'email', 'username']


class ContratProprietaireFrom(ModelForm):
    class Meta:
        model = ContratProprietaire
        fields = '__all__'
        exclude = ['user', 'status']


class ReservationForm(ModelForm):
    class Meta:
        model = Reservation
        fields = '__all__'
        exclude = ['user', 'propriete']

