# from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import serializers

# from .permissions import *
from .serializers import *
from neige_soleil_app.models import *


############################################################################################
# GENERAL VIEWS
############################################################################################


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'id': user.id,
            'nom': user.first_name + " " + user.last_name,
            'token': token.key,
            'is_superuser': user.is_superuser,
        })


@api_view(['GET'])
@authentication_classes([TokenAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_user_profile_view(request, pk):
    if request.user.id == int(pk) or request.user.is_superuser:
        serializer = ProfileSerializer
        try:
            profile = Profile.objects.get(user=pk)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        except Profile.DoesNotExist:
            content = ""
            return Response(content, status=status.HTTP_404_NOT_FOUND)
    content = ""
    return Response(content, status=status.HTTP_403_FORBIDDEN)


############################################################################################
# ADMIN VIEWS
############################################################################################


class AdminViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    authentication_classes = [BasicAuthentication, TokenAuthentication]


class UserViewSet(AdminViewSet):
    queryset = Utilisateur.objects.exclude(is_superuser=True)
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
        serializer = AdminPasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'status': 'password set'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class ProfileViewSet(AdminViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_permissions(self):
        if self.request.method == "POST" or self.request.method == "PUT":
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        if request.user.id == int(request.data["user"]) or request.user.is_superuser:
            return super().create(request, *args, **kwargs)
        content = ""
        return Response(content, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        if request.user.id == int(request.data["user"]) or request.user.is_superuser:
            return super().update(request, *args, **kwargs)
        content = ""
        return Response(content, status=status.HTTP_403_FORBIDDEN)


class ContratProprietaireViewSet(AdminViewSet):
    queryset = ContratProprietaire.objects.all()
    serializer_class = ContratProprietaireSerializer


class ReservationViewSet(AdminViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    # TODO: Gérer la conformités des dates avant les put et les post

############################################################################################
# USER VIEWS
############################################################################################

# TODO: Contrat View : Il voit tout les contrats qui ne sont pas les siens
# TODO: Reservations View : Voir, Ajouter et modifier ces reservations