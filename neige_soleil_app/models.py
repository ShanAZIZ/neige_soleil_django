from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    adresse = models.CharField(max_length=200)
    code_postale = models.IntegerField()
    ville = models.CharField(max_length=200)
    telephone = models.IntegerField()


class ContratProprietaire(models.Model):
    DISPONIBLE = 'AVAIL'
    OCCUPER = 'BUSY'
    INACTIF = 'OFF'

    YEAR_IN_SCHOOL_CHOICES = [
        (DISPONIBLE, 'Disponible'),
        (OCCUPER, 'Occuper'),
        (INACTIF, 'Inactif'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nom = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    surface_habitable = models.FloatField()
    surface_balcon = models.FloatField()
    capacite = models.IntegerField()
    distance_pistes = models.FloatField()
    status = models.CharField(max_length=5, choices=YEAR_IN_SCHOOL_CHOICES, default=DISPONIBLE)


class ProprietePrix(models.Model):
    location = models.OneToOneField(ContratProprietaire, on_delete=models.CASCADE)
    prix = models.FloatField()
    # TO DO : Definir les prix par saison, les saisons et les prix afficher


class ProprieteImage(models.Model):
    location = models.ForeignKey(ContratProprietaire, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Reservation(models.Model):

    ENCOURS = 'WAIT'
    CONFIRMER = 'VALID'
    ANNULER = 'CANCEL'

    STATUS_RES = [
        (ENCOURS, 'En cours'),
        (CONFIRMER, 'Confirmer'),
        (ANNULER, 'Annuler'),
    ]

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    location = models.ForeignKey(ContratProprietaire, on_delete=models.CASCADE)
    date_reservation = models.DateField(auto_now_add=True)
    date_debut_sejour = models.DateField()
    date_fin_sejour = models.DateField()
    status_reservation = models.CharField(max_length=6, choices=STATUS_RES, default=ENCOURS)

