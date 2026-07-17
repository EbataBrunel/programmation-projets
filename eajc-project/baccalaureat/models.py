from django.db import models
from django.contrib.auth.models import User
from etablissement.models import*
from annee.models import*

class Baccalaureat(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    annee=models.ForeignKey(Annee, on_delete=models.CASCADE, null=True)
    etablissement=models.ForeignKey(Etablissement, on_delete=models.CASCADE, null=True)
    LEVEL=[
        ('BAC A1','BAC A1'),
        ('BAC A2','BAC A2'),
        ('BAC A3','BAC A3'),
        ('BAC A4','BAC A4'),
        ('BAC A5','BAC A5'),
        ('BAC C','BAC C'),
        ('BAC D','BAC D'),
        ('BAC E','BAC E'),
        ('BAC F1','BAC F1'),
        ('BAC F2','BAC F2'),
        ('BAC F3','BAC F3'),
        ('BAC F4','BAC F4'),
        ("BAC Français ('inscription non-règlementée')","BAC Français ('inscription non-règlementée')"),
        ("BAC Français ('inscription règlementée')","BAC Français ('inscription règlementée')"),
        ("BAC Français ('lycée français')","BAC Français ('lycée français')"),
        ('BAC G1','BAC G1'),
        ('BAC G2','BAC G2'),
        ('BAC G3','BAC G3'),
        ('BAC R1','BAC R1'),
        ('BAC R2','BAC R2'),
        ('BAC R3','BAC R3'),
        ('BAC R4','BAC R4'),
        ('BAC R5','BAC R5'),
        ('BAC R6','BAC R6'),
        ('BAC R7','BAC R7'),
        ('Autre BAC','Autre BAC')

    ]
    diplome=models.CharField(max_length=200, null=True, choices=LEVEL)
