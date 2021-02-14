from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Location, PrixLocation


class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class LocationCreationFrom(ModelForm):
    class Meta:
        model = Location
        fields = '__all__'


class LocationSetPrix(ModelForm):
    class Meta:
        model = PrixLocation
        fields = '__all__'