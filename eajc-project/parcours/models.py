from django.db import models
from django.contrib.auth.models import User
from etablissement.models import*
from formation.models import*
from annee.models import*

class Parcours(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name="users")
    annee=models.ForeignKey(Annee, on_delete=models.CASCADE, null=True)
    annee1=models.IntegerField(default=0, null=True)
    etablissement=models.ForeignKey(Etablissement, on_delete=models.CASCADE, null=True,related_name="etablissements")
    formation=models.ForeignKey(Formation, on_delete=models.CASCADE, null=True, related_name="formations")
    LEVEL=[
        ('Baccalauréat','Baccalauréat'),
        ('Bac + 1','Bac + 1'),
        ('Bac + 2','Bac + 2'),
        ('Bac + 3','Bac + 3'),
        ('Bac + 4','Bac + 4'),
        ('Bac + 5','Bac + 5'),
        ('Bac + 6','Bac + 6'),
        ('Bac + 7','Bac + 7'),
        ('1ère année Ingénieur','1ère année Ingénieur'),
        ('2ème année Ingénieur','2ème année Ingénieur'),
        ('3ème année Ingénieur','3ème année Ingénieur'),

    ]
    niveau=models.CharField(max_length=200, null=True, choices=LEVEL)
    status=models.BooleanField(null=True,default=True)
    statusan=models.CharField(max_length=50, null=True, default="Non")

