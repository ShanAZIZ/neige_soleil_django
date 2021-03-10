from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    """
    Le profile de l'utilisateur :
    il contient des informations propre à un utilisateur
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    adresse = models.CharField(max_length=200)
    code_postale = models.IntegerField()
    ville = models.CharField(max_length=200)
    telephone = models.IntegerField()

    def __str__(self):
        return self.user.first_name


class ProfileProprietaire(models.Model):
    """
    Défini si les utilisateurs deviennent proprietaire (seuls les proprietaire peuvent
    creer des contrats)
    """
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)


class ContratProprietaire(models.Model):
    """
    Cette classe generera la table des proprietés,
    et contients les informations des proprietés.

    TODO: Ajouter les dates du contrat selon la demande du Projet
    """
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

    def __str__(self):
        return self.nom


class ProprietePrix(models.Model):
    """
    Permet de definir les differents prix de la propriete
    TODO: Ajouter plusieurs types de prix et la fonction d'affichage selon la période
    """
    propriete = models.OneToOneField(ContratProprietaire, on_delete=models.CASCADE)
    prix = models.FloatField()

    # TO DO : Definir les prix par saison, les saisons et les prix afficher

    def __str__(self):
        return self.propriete.nom


class ProprieteImage(models.Model):
    """
    Classe qui regroupe les images des proprietés
    """
    propriete = models.ForeignKey(ContratProprietaire, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.propriete.nom + " " + str(self.id)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Reservation(models.Model):
    """
    Classe des reservations
    """
    ENCOURS = 'WAIT'
    ANNULER = 'CANCEL'

    STATUS_RES = [
        (ENCOURS, 'En cours'),
        (ANNULER, 'Annuler'),
    ]

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    propriete = models.ForeignKey(ContratProprietaire, on_delete=models.CASCADE)
    date_reservation = models.DateField(auto_now_add=True)
    date_debut_sejour = models.DateField()
    date_fin_sejour = models.DateField()
    status_reservation = models.CharField(max_length=6, choices=STATUS_RES, default=ENCOURS)

    def prixTotal(self):
        duree = (self.date_fin_sejour - self.date_debut_sejour).days
        return duree * self.propriete.proprieteprix.prix / 7


class Location(models.Model):
    """
    Classe des locations
    """
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE)
    date_confirmation = models.DateField(auto_now_add=True)
