from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    """
    Le profile de l'utilisateur :
    il contient des informations propre à un utilisateur
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nom = models.CharField(max_length=200)
    prenom = models.CharField(max_length=200)
    adresse = models.CharField(max_length=200)
    code_postale = models.CharField(max_length=5)
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
    rib = models.CharField(max_length=50)


class ContratProprietaire(models.Model):
    """
    Cette class generera la table des proprietés,
    et contients les informations des proprietés.
    """
    DISPONIBLE = 'AVAIL'
    OCCUPER = 'BUSY'
    INACTIF = 'OFF'

    STATUS_CHOICES = [
        (DISPONIBLE, 'Actif'),
        (INACTIF, 'Inactif')
    ]

    TYPES_CHOICES = [
        ('F1', 'F1'),
        ('F2', 'F2'),
        ('F3', 'F3'),
        ('F4', 'F4'),
        ('F5', 'F5'),
    ]

    EXPOSITION_CHOICES = [
        ('Sud', 'Sud'),
        ('Nord', 'Nord'),
        ('Nord-est', 'Nord-est'),
        ('Nord-ouest', 'Nord-ouest'),
        ('Sud-est', 'Sud-est'),
        ('Sud-ouest', 'Sud-ouest'),
        ('Est', 'Est'),
        ('Ouest', 'Ouest'),
    ]

    profileproprietaire = models.ForeignKey(ProfileProprietaire, on_delete=models.CASCADE)
    nom = models.CharField(max_length=200)
    adresse = models.CharField(max_length=200)
    code_postale = models.CharField(max_length=5)
    ville = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    type = models.CharField(max_length=2, choices=TYPES_CHOICES)
    exposition = models.CharField(max_length=10, choices=EXPOSITION_CHOICES)
    surface_habitable = models.FloatField()
    surface_balcon = models.FloatField()
    capacite = models.IntegerField()
    distance_pistes = models.FloatField()
    status = models.CharField(max_length=5, choices=STATUS_CHOICES, default=DISPONIBLE)
    prix_saison_haute = models.FloatField()
    prix_saison_moyenne = models.FloatField()
    prix_saison_basse = models.FloatField()

    def __str__(self):
        return self.nom

    def get_prix_actuel(self):
        return self.prix_saison_moyenne


class ProprieteImage(models.Model):
    """
    Class qui regroupe les images des proprietés
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
    Class des reservations
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

    def prix_total(self):
        duree = (self.date_fin_sejour - self.date_debut_sejour).days
        if duree == 0:
            duree = 1
        return duree * self.propriete.get_prix_actuel() / 7

    def annuler_reservation(self):
        """
        modifier le status de la reservation
        """
        pass


class Location(models.Model):
    """
    Class des locations
    """
    reservation = models.OneToOneField(Reservation, on_delete=models.SET_NULL, null=True)
    date_confirmation = models.DateField(auto_now_add=True)