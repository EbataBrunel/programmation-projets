from django.db import models
from projet.models import Projet
from tache.models import Tache

class Depense(models.Model):
    TYPE_DEPENSE = [
        ('Main d\'œuvre', 'Main d\'œuvre'),
        ('Logiciel', 'Logiciel'),
        ('Matériel', 'Matériel'),
        ('Infrastructure', 'Infrastructure'),
        ('Autre', 'Autre'),
    ]

    projet = models.ForeignKey(Projet, on_delete=models.CASCADE, related_name="depenses")
    tache = models.ForeignKey(Tache, null=True, blank=True, on_delete=models.SET_NULL, related_name="depenses")
    description = models.CharField(max_length=255)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_paiement = models.DateField()
    type_depense = models.CharField(max_length=50, choices=TYPE_DEPENSE)

    def __str__(self):
        return f"{self.description} - {self.montant}€"
    