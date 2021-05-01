from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.utils.dateparse import parse_date

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
        # exclude = ['user', 'propriete']

    def check_date(self):
        date_debut_sejour = parse_date(self.data['date_debut_sejour'])
        date_fin_sejour = parse_date(self.data['date_fin_sejour'])
        contrat = ContratProprietaire.objects.get(id=self.data['propriete'])
        if date_debut_sejour < date_fin_sejour:
            if contrat.is_avail(date_debut_sejour, date_fin_sejour):
                return True
        return False

    def is_valid(self):
        if self.check_date():
            return super().is_valid()



