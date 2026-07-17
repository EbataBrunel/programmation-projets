from django.db import models
from django.contrib.auth.models import User

class Etablissement(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name=models.CharField(max_length=200)
    country=models.CharField(max_length=100)
    city=models.CharField(max_length=100)

    def __str__(self):
        return self.name
