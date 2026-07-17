from django.db import models
from django.contrib.auth.models import User
from devise.models import Devise

class Projet(models.Model):
    
    TYPE_CHOICES = [
        ('Personnel', 'Personnel'),
        ('Individuel', 'Individuel'),
        ('En groupe', 'En groupe'),
    ]
     
    STATUT_CHOICES = [
        ('Planifié', 'Planifié'),
        ('En cours', 'En cours'),
        ('Terminé', 'Terminé'),
    ]
    
    nom = models.CharField(max_length=255)
    description = models.TextField()
    date_debut = models.DateField(null=True, blank=True)
    date_fin = models.DateField(null=True, blank=True)
    type_projet = models.CharField(max_length=20, choices=TYPE_CHOICES, default='Personnel')
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='Planifié')
    responsable = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    cout_estime = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    cout_reel = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    montant_responsable = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True)
    devise = models.ForeignKey(Devise, on_delete=models.SET_NULL, null=True)
    visibilite_projet = models.BooleanField(default=False, null=True)
    visibilite_tache = models.BooleanField(default=False, null=True)
    visibilite_depense = models.BooleanField(default=False, null=True)
    visibilite_progres = models.BooleanField(default=False, null=True)
    
    def __str__(self):
        return self.nom