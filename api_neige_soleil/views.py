# from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import status

from .permissions import *
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
    """
    Affiche le profile de l'utilisateur, sinon un 404 ou 403
    """
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


@api_view(['GET'])
@authentication_classes([TokenAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_user_reservation_view(request, pk):
    """
    Affiche les reservations de l'utilisateur, sinon une liste vide ou 403
    """
    if request.user.id == int(pk) or request.user.is_superuser:
        serializer = ReservationSerializer
        reservations = Reservation.objects.filter(user=pk)
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)
    content = ""
    return Response(content, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@authentication_classes([TokenAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_contrat_by_user_view(request, pk):
    """
    Affiche les contrats par proprietaire, sinon une liste vide ou 403
    """
    if request.user.id == int(pk) or request.user.is_superuser:
        serializer = ContratProprietaireSerializer
        contrats = ContratProprietaire.objects.exclude(user=pk)
        contrats.filter(status='AVAIL')
        serializer = ContratProprietaireSerializer(contrats, many=True)
        return Response(serializer.data)
    content = ""
    return Response(content, status=status.HTTP_403_FORBIDDEN)


############################################################################################
# GENERIC VIEWS
############################################################################################


class AdminViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    authentication_classes = [BasicAuthentication, TokenAuthentication]


class UserViewSet(AdminViewSet):
    queryset = Utilisateur.objects.exclude(is_superuser=True)
    serializer_class = UserProfileSerializer

    def get_permissions(self):
        if self.action in ['update', 'retrieve', 'create']:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

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

    def retrieve(self, request, *args, **kwargs):
        print(kwargs['pk'])
        if request.user.id == int(kwargs['pk']) or request.user.is_superuser:
            return super().retrieve(request, *args, **kwargs)
        content = ""
        return Response(content, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        if request.user.id == int(kwargs['pk']) or request.user.is_superuser:
            return super().update(request, *args, **kwargs)
        content = ""
        return Response(content, status=status.HTTP_403_FORBIDDEN)


class ProfileViewSet(AdminViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_permissions(self):
        if self.action in ['update', 'retrieve', 'create']:
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    # TODO : permission sur create ( Profile )

    def retrieve(self, request, *args, **kwargs):

        if request.user.id == int(kwargs['pk']) or request.user.is_superuser:
            return super().retrieve(request, *args, **kwargs)
        content = ""
        return Response(content, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        if request.user.id == int(kwargs['pk']) or request.user.is_superuser:
            return super().update(request, *args, **kwargs)
        content = ""
        return Response(content, status=status.HTTP_403_FORBIDDEN)


class ContratProprietaireViewSet(AdminViewSet):
    queryset = ContratProprietaire.objects.all()
    serializer_class = ContratProprietaireSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']: 
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()


class ReservationViewSet(AdminViewSet):
    
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    # TODO: Permission sur create et list ( Reservation )

    def retrieve(self, request, *args, **kwargs):
        if request.user.id == int(kwargs['pk']) or request.user.is_superuser:
            return super().retrieve(request, *args, **kwargs)
        content = ""
        return Response(content, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        if request.user.id == int(kwargs['pk']) or request.user.is_superuser:
            return super().update(request, *args, **kwargs)
        content = ""
        return Response(content, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        if request.user.id == int(kwargs['pk']) or request.user.is_superuser:
            return super().destroy(request, *args, **kwargs)
        content = ""
        return Response(content, status=status.HTTP_403_FORBIDDEN)




