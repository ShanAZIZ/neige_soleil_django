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
    queryset = Utilisateur.objects.all()
    serializer_class = UserSerializer


class ContratProprietaireViewSet(AdminViewSet):
    queryset = ContratProprietaire.objects.all()
    serializer_class = ContratProprietaireSerializer


class ReservationViewSet(AdminViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


class LocationViewSet(AdminViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
