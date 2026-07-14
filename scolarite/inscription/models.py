from django.db import models
from django.contrib.auth.models import User
from salle.models import Salle
from app_auth.models import Student
from anneeacademique.models import AnneeCademique

class Inscription(models.Model):
    MP = [
        ('Espèce', 'Espèce'),
        ('Virement', 'Virement'),
        ('Mobile', 'Mobile')
    ]
    salle = models.ForeignKey(Salle, on_delete=models.CASCADE, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    anneeacademique = models.ForeignKey(AnneeCademique, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    dateins = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=10.00, null=True)
    mode_paiement = models.CharField(max_length=50, choices=MP, null=True, default="Espèce")
