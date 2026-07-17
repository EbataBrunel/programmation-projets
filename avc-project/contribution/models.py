from django.db import models
from projet.models import Projet
from django.contrib.auth.models import User

class Contribution(models.Model):
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE, related_name="contributions")
    actionnaire = models.OneToOneField(User, on_delete=models.CASCADE)
    montant_contribution = models.DecimalField(max_digits=10, decimal_places=2)
    date_contribution = models.DateField()

    def __str__(self):
        return f"{self.user.last_name} - {self.montant_contribution}€"
