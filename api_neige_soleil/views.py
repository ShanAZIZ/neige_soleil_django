from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import *
from neige_soleil_app.models import *

# TODO: API - Adapter les permissions des vues


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication, TokenAuthentication]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileProprietaireViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ProfileProprietaire.objects.all()
    serializer_class = ProfileProprietaireSerializer


class ContratProprietaireViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ContratProprietaire.objects.all()
    serializer_class = ContratProprietaireSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    authentication_classes = [BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


class LocationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
