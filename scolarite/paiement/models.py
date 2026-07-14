from django.db import models
from django.contrib.auth.models import User
from anneeacademique.models import AnneeCademique
from app_auth.models import Student, Parent
from salle.models import Salle


class AutorisationPayment(models.Model):
    MS = [
        ('Janvier', 'Janvier'),
        ('Février', 'Février'),
        ('Mars', 'Mars'),
        ('Avril', 'Avril'),
        ('Mai', 'Mai'),
        ('Juin', 'Juin'),
        ('Juillet', 'Juillet'),       
        ('Août', 'Août'),        
        ('Septembre', 'Septembre'),       
        ('Octobre', 'Octobre'),       
        ('Novembre', 'Novembre'),       
        ('Décembre', 'Décembre'),
    ]
    anneeacademique = models.ForeignKey(AnneeCademique, on_delete=models.CASCADE, null=True)
    salle = models.ForeignKey(Salle, on_delete=models.CASCADE, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    month = models.CharField(max_length=20, choices=MS, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    justification = models.TextField()
    date_autorisation = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    
class AutorisationPaymentSalle(models.Model):
    MS = [
        ('Janvier', 'Janvier'),
        ('Février', 'Février'),
        ('Mars', 'Mars'),
        ('Avril', 'Avril'),
        ('Mai', 'Mai'),
        ('Juin', 'Juin'),
        ('Juillet', 'Juillet'),       
        ('Août', 'Août'),        
        ('Septembre', 'Septembre'),       
        ('Octobre', 'Octobre'),       
        ('Novembre', 'Novembre'),       
        ('Décembre', 'Décembre'),
    ]
    anneeacademique = models.ForeignKey(AnneeCademique, on_delete=models.CASCADE, null=True)
    salle = models.ForeignKey(Salle, on_delete=models.CASCADE, null=True)
    month = models.CharField(max_length=20, choices=MS, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    justification = models.TextField()
    date_autorisation = models.DateTimeField(null=True, blank=True, auto_now_add=True)


class Payment(models.Model):
    MS = [
        ('Janvier', 'Janvier'),
        ('Février', 'Février'),
        ('Mars', 'Mars'),
        ('Avril', 'Avril'),
        ('Mai', 'Mai'),
        ('Juin', 'Juin'),
        ('Juillet', 'Juillet'),       
        ('Août', 'Août'),        
        ('Septembre', 'Septembre'),       
        ('Octobre', 'Octobre'),       
        ('Novembre', 'Novembre'),       
        ('Décembre', 'Décembre'),
    ]
    MP = [
        ('Espèce', 'Espèce'),
        ('Virement', 'Virement'),
        ('Mobile', 'Mobile')
    ]
    anneeacademique = models.ForeignKey(AnneeCademique, on_delete=models.CASCADE, null=True)
    salle = models.ForeignKey(Salle, on_delete=models.CASCADE, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    month = models.CharField(max_length=20, choices=MS, null=True)
    mode_paiement = models.CharField(max_length=50, choices=MP, null=True, default="Espèce")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=10.00, null=True)
    datepaye = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    status = models.BooleanField(default=False, null=True)
    status_parent = models.BooleanField(default=False, null=True)
    
    
class Notification(models.Model):
    MS = [
        ('Janvier', 'Janvier'),
        ('Février', 'Février'),
        ('Mars', 'Mars'),
        ('Avril', 'Avril'),
        ('Mai', 'Mai'),
        ('Juin', 'Juin'),
        ('Juillet', 'Juillet'),       
        ('Août', 'Août'),        
        ('Septembre', 'Septembre'),       
        ('Octobre', 'Octobre'),       
        ('Novembre', 'Novembre'),       
        ('Décembre', 'Décembre'),
    ]
    anneeacademique = models.ForeignKey(AnneeCademique, on_delete=models.CASCADE, null=True)
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, null=True)
    month = models.CharField(max_length=20, choices=MS, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=10.00, null=True)
    date_notification = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    status = models.BooleanField(default=False, null=True) # Statut de lecture
    