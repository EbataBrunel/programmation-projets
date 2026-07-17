from django.db import models

from projet.models import Projet

class Progres(models.Model):
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE, related_name="progres")
    date_progres = models.DateField(null=True, blank=True)
    pourcentage = models.IntegerField(default=0, null=True)
    commentaire = models.TextField()

    def __str__(self):
        return f"{self.pourcentage}"
