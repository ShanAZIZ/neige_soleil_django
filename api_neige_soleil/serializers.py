from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated

from neige_soleil_app.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ['id', 'username', 'email']


class ContratProprietaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContratProprietaire
        fields = '__all__'


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'