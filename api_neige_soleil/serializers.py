from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated

from neige_soleil_app.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class ProfileProprietaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileProprietaire
        fields = '__all__'


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