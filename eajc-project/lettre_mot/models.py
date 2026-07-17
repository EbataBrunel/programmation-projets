from django.db import models
from django.contrib.auth.models import User

class Lettre_mot(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    TP=[
        ('Inscription','Inscription'),
        ('Stage','Stage'),
        ('Alternance','Alternance'),
        ('Emploi','Emploi')
    ]
    type=models.CharField(max_length=100, null=True, choices=TP)
    file=models.FileField(upload_to="upload", null=False) 
    statut=models.IntegerField(default=0,null=True)
    date=models.DateField(auto_created=True)
    comment=models.TextField(null=True)
