from django.db import models

class Devise(models.Model):
    
    nom = models.CharField(max_length=100)
    symbole = models.CharField(max_length=100)

    def __str__(self):
        return self.symbole