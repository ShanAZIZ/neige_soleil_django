from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, ContratProprietaire, Reservation, ProfileProprietaire


class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class UserInfoUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']


class ContratProprietaireFrom(ModelForm):
    class Meta:
        model = ContratProprietaire
        fields = '__all__'
        exclude = ['profileproprietaire']


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user']


class ReservationForm(ModelForm):
    class Meta:
        model = Reservation
        fields = '__all__'

    def is_avail(self, contrat):
        for reservation in contrat.reservation_set.all():
            if reservation.date_debut_sejour <= self.date_debut_sejour <= reservation.date_fin_sejour or reservation.date_debut_sejour <= self.date_fin_sejour <= reservation.date_fin_sejour:
                return False
        return True


class ProfileProprietaireForm(ModelForm):
    class Meta:
        model = ProfileProprietaire
        fields = '__all__'
        exclude = ['profile']
