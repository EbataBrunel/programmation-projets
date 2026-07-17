from django.db import models
from entreprise.models import *
from django.contrib.auth.models import User

class Reference(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    entreprise=models.ForeignKey(Entreprise, on_delete=models.CASCADE, null=False)
    name=models.CharField(max_length=200)
    phone=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    SEX=[
        ('Masculin','Masculin'),
        ('Feminin','Feminin')
    ]
    gender=models.CharField(max_length=100, null=True, choices=SEX)
    status=models.BooleanField(null=True,default=True)

    def __str__(self):
        return self.nom
