from django.contrib import admin

from .models import *

admin.site.register(Profile)
admin.site.register(Reservation)
admin.site.register(ContratProprietaire)
admin.site.register(ProprietePrix)
admin.site.register(ProprieteImage)