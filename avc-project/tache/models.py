from django.db import models
from projet.models import Projet

class Tache(models.Model):
    STATUT_CHOICES = [
        ('Non commencé', 'Non commencé'),
        ('En cours', 'En cours'),
        ('Terminé', 'Terminé'),
    ]

    projet = models.ForeignKey(Projet, on_delete=models.CASCADE, related_name="taches")
    nom = models.CharField(max_length=255)
    description = models.TextField()
    date_debut = models.DateField(null=True, blank=True)
    date_fin = models.DateField(null=True, blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='Non commencé')
    cout_estime = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    cout_reel = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.nom} ({self.projet.nom})"
