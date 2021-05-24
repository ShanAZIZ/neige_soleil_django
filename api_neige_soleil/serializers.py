from abc import ABC

from django.utils.dateparse import parse_date
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

    def check_date(self, data):
        date_debut_sejour = data['date_debut_sejour']
        date_fin_sejour = data['date_fin_sejour']
        contrat = ContratProprietaire.objects.get(id=data['propriete'].id)
        if date_debut_sejour < date_fin_sejour:
            if contrat.is_avail(date_debut_sejour, date_fin_sejour):
                return True
        return False

    def validate(self, data):
        if self.check_date(data):
            return data
        raise serializers.ValidationError("Dates not correct")

