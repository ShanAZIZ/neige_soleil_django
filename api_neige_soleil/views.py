# from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser

# from .permissions import *
from .serializers import *
from neige_soleil_app.models import *

# TODO: API - Adapter les permissions des vues

############################################################################################
# ADMIN VIEWS
############################################################################################


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'is_superuser': user.is_superuser,
        })


class AdminViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    authentication_classes = [BasicAuthentication, TokenAuthentication]


class UserViewSet(AdminViewSet):
    queryset = Utilisateur.objects.all()
    serializer_class = UserProfileSerializer

    # def get_permissions(self):
    #     if self.action in ['update', 'partial_update', 'list']:
    #         self.permission_classes = [IsAdminOrIsSelf]
    #     elif self.action in ['create', 'destroy']:
    #         self.permission_classes = [IsAdminUser]
    #     return super().get_permissions()


    @action(detail=True, methods=['post'])
    def set_password(self, request, pk=None):
        user = self.get_object()
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'status': 'password set'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class ProfileView(AdminViewSet):
    queryset = Utilisateur.objects.all()
    serializer_class = UserProfileSerializer


class ContratProprietaireViewSet(AdminViewSet):
    queryset = ContratProprietaire.objects.all()
    serializer_class = ContratProprietaireSerializer


class ReservationViewSet(AdminViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


class LocationViewSet(AdminViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


############################################################################################
# USER VIEWS
############################################################################################
