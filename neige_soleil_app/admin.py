from django.contrib import admin

from .models import *

admin.site.register(Utilisateur)
admin.site.register(Profile)
admin.site.register(Reservation)
admin.site.register(ContratProprietaire)
admin.site.register(ProprieteImage)