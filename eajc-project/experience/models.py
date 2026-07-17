from django.db import models
from django.contrib.auth.models import User
from entreprise.models import*

class Experience(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    TYPE=[
        ('Employé(e)','Employé(e)'),
        ('Stage','Stage'),
        ('Alternance','Alternance'),
    ]
    type_exp=models.CharField(max_length=100, null=False, choices=TYPE)
    entreprise=models.ForeignKey(Entreprise, on_delete=models.CASCADE, null=True)
    posteoccupe=models.CharField(max_length=200, null=True)
    projet=models.CharField(max_length=200, null=True)
    tache=models.CharField(max_length=300)
    date_debut=models.DateField(null=True)
    date_fin=models.DateField(null=True)
    status=models.BooleanField(null=True,default=True)
    lien=models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.type_exp

