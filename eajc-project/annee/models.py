from django.db import models

class Annee(models.Model):
    libelle=models.CharField(max_length=4, unique=True, null=True)

    def __str__(self):
        return self.libelle
    

