from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    adresse = models.CharField(max_length=200)
    code_postale = models.IntegerField()
    ville = models.CharField(max_length=200)
    telephone = models.IntegerField()
    rib = models.CharField(max_length=200)


class Location(models.Model):
    DISPONIBLE = 'AVAIL'
    OCCUPER = 'BUSY'
    INACTIF = 'OFF'

    YEAR_IN_SCHOOL_CHOICES = [
        (DISPONIBLE, 'Disponible'),
        (OCCUPER, 'Occuper'),
        (INACTIF, 'Inactif'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description_breve = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    surface_habitable = models.FloatField()
    surface_balcon = models.FloatField()
    capacite = models.IntegerField()
    distance_pistes = models.FloatField()
    status = models.CharField(max_length=5, choices=YEAR_IN_SCHOOL_CHOICES, default=DISPONIBLE)


class PrixLocation(models.Model):
    location = models.OneToOneField(Location, on_delete=models.CASCADE)
    prix = models.FloatField()
    # TO DO : Definir les prix par saison, les saisons et les prix afficher


class LocationImage(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
