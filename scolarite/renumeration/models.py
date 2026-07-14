from django.db import models
from django.contrib.auth.models import User
from anneeacademique.models import AnneeCademique


class Renumeration(models.Model):
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
    
    anneeacademique = models.ForeignKey(AnneeCademique, on_delete=models.CASCADE, null=False)
    month = models.CharField(max_length=20, choices=MS, null=True)
    personnel = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        null=False, 
        related_name='personnel_à_renumerer')
       
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    indeminte = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_amount = models.CharField(max_length=1000, null=True)
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        null=False,
        related_name='renumeration_enregistrées_par')
    date = models.DateField(blank=True, auto_now_add=True)
    status = models.BooleanField(default=False, null=True)
    

class Contrat(models.Model):
    anneeacademique = models.ForeignKey(AnneeCademique, on_delete=models.CASCADE, null=False)
    TC = [
        ('Admin', 'Admin'),
        ('Enseignant', 'Enseignant'),
    ]  
    type_contrat = models.CharField(max_length=20, choices=TC, null=True)
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        null=False, 
        related_name='contrats')
    
    poste = models.CharField(max_length=100, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    description = models.TextField()
    date_debut = models.DateField(null=True, blank=True)
    date_fin = models.DateField(null=True, blank=True)
    date_contrat = models.DateTimeField(auto_now_add=True)
    admin = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        null=True, 
        related_name='responsable_enregistre_contrat')
    status_signature = models.BooleanField(default=False, null=True) # Statut de la signature de l'utilisateur (False s'il n'a pas signé)
    date_signature = models.DateField(null=True, blank=True, auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name}"
    
class RenumerationAdmin(models.Model):
    anneeacademique = models.ForeignKey(AnneeCademique, on_delete=models.CASCADE, null=True)
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
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        null=False, 
        related_name='renumerationadmins')   
    month = models.CharField(max_length=20, choices=MS, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True)
    indemnite = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    responsable = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        null=False,
        related_name='responsables')
    date_renumeration = models.DateField(blank=True, auto_now_add=True, null=True)
    status = models.BooleanField(default=False, null=True)
  
    

    
