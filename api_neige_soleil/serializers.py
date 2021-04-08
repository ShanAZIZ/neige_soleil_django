from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated

from neige_soleil_app.models import *



############################################################################################
# USER MODEL SERIALIZERS
############################################################################################


class UserProfileSerializer(serializers.ModelSerializer):
    profile = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all()) 
    class Meta:
        model = Utilisateur
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'is_proprietaire', 'profile_id']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'adresse', 'code_postale', 'ville', 'telephone', 'rib']


class PasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


############################################################################################
# 
############################################################################################


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'is_proprietaire']


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