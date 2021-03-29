# from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAdminUser

from .serializers import *
from neige_soleil_app.models import *

# TODO: API - Adapter les permissions des vues


class AdminViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    authentication_classes = [BasicAuthentication, TokenAuthentication]


class UserViewSet(AdminViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileViewSet(AdminViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileProprietaireViewSet(AdminViewSet):
    queryset = ProfileProprietaire.objects.all()
    serializer_class = ProfileProprietaireSerializer


class ContratProprietaireViewSet(AdminViewSet):
    queryset = ContratProprietaire.objects.all()
    serializer_class = ContratProprietaireSerializer


class ReservationViewSet(AdminViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


class LocationViewSet(AdminViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
