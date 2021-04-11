from abc import ABC

from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated

from neige_soleil_app.models import *


############################################################################################
# USER MODEL SERIALIZERS
############################################################################################


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'is_proprietaire']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'adresse', 'code_postale', 'ville', 'telephone', 'rib', 'user']


class AdminPasswordSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    # old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


############################################################################################
# CONTRAT MODEL SERIALIZERS
############################################################################################


class ContratProprietaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContratProprietaire
        fields = '__all__'


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'
