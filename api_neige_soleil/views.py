from django.shortcuts import render

from rest_framework import viewsets
from .serializers import *
from neige_soleil_app.models import *


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
