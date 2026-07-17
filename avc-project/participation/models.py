from django.db import models
from django.contrib.auth.models import User
from projet.models import Projet

class Participation(models.Model):
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE, related_name="participations")
    acteur = models.OneToOneField(User, on_delete=models.CASCADE)
    montant_participation = models.DecimalField(max_digits=10, decimal_places=2)
    date_participation = models.DateField()

    def __str__(self):
        return f"{self.acteur.last_name} - {self.montant_participation}"