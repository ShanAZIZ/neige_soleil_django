from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save


class Utilisateur(AbstractUser):
    is_proprietaire = models.BooleanField(null=True, blank=True, default=False)

    def __str__(self):
        return str(self.username)


class Profile(models.Model):
    user = models.OneToOneField(Utilisateur, on_delete=models.CASCADE)
    adresse = models.CharField(max_length=200)
    code_postale = models.CharField(max_length=5)
    ville = models.CharField(max_length=200)
    telephone = models.IntegerField()
    rib = models.CharField(max_length=50)

    def __str__(self):
        return str(self.user.first_name) + " " + str(self.user.last_name)


class ContratProprietaire(models.Model):
    DISPONIBLE = 'AVAIL'
    INACTIF = 'EXPIRED'
    ATTENTE = 'CHECK'

    STATUS_CHOICES = [
        (ATTENTE, 'Attente de Validation'),
        (DISPONIBLE, 'Actif'),
        (INACTIF, 'Expiré')
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
    user = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    date_debut = models.DateField()
    date_fin = models.DateField()
    date_creation = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=7, choices=STATUS_CHOICES, default=ATTENTE)
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
    prix_saison_haute = models.FloatField()
    prix_saison_moyenne = models.FloatField()
    prix_saison_basse = models.FloatField()

    def __str__(self):
        return self.nom

    def get_prix_actuel(self):
        return self.prix_saison_moyenne

    def is_avail(self, date_debut_sejour, date_fin_sejour, pk=None):
        reservations = self.reservation_set.exclude(id=pk)
        for reservation in reservations:
            if (reservation.date_debut_sejour <= date_debut_sejour <= reservation.date_fin_sejour or
                reservation.date_debut_sejour <= date_fin_sejour <= reservation.date_fin_sejour) and \
                    reservation.status_reservation != 'CANCEL':
                return False
        return True


class ProprieteImage(models.Model):
    # TODO: Suppression des images du serveur si suppression de la bdd
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
    # TODO: Gérer les dates de fin antérieures aux dates débuts et les dates de debut avant date actuelle
    ENCOURS = 'WAIT'
    LOCATION = 'LOCATION'
    ANNULER = 'CANCEL'

    STATUS_RES = [
        (ENCOURS, 'En cours'),
        (LOCATION, 'Location'),
        (ANNULER, 'Annuler'),
    ]

    user = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    propriete = models.ForeignKey(ContratProprietaire, on_delete=models.CASCADE)
    date_reservation = models.DateField(auto_now_add=True)
    date_debut_sejour = models.DateField()
    date_fin_sejour = models.DateField()
    status_reservation = models.CharField(max_length=8,
                                          choices=STATUS_RES,
                                          default=ENCOURS)

    def __str__(self):
        return str(self.user.username) + " " + str(self.propriete.nom) + " " + \
               str(self.date_debut_sejour) + " a " + str(self.date_fin_sejour)

    def prix_total(self):
        duree = (self.date_fin_sejour - self.date_debut_sejour).days
        if duree == 0:
            duree = 1
        return duree * self.propriete.get_prix_actuel() / 7

    def annuler_reservation(self):
        """
        modifier le status de la reservation
        """
        self.status_reservation = self.ANNULER
        pass

    # def check_date(self):
    #     if self.date_debut_sejour < self.date_fin_sejour:
    #         if self.propriete.is_avail(self.date_debut_sejour, self.date_fin_sejour):
    #             return True
    #     return False
    #
    # def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    #     if self.check_date() and self.propriete.is_avail(self.date_debut_sejour, self.date_fin_sejour):
    #         super().save(force_insert, force_update, using, update_fields)


def on_new_propriete(sender, instance, created,  **kwargs):
    if created:
        utilisateur = Utilisateur.objects.get(id=instance.user.id)
        utilisateur.is_proprietaire = True
        utilisateur.save()


post_save.connect(on_new_propriete, sender=ContratProprietaire)

