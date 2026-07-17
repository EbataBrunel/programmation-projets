from django.db import models
from projet.models import Projet
from django.contrib.auth.models import User

class ContratRemboursement(models.Model):
    STATUT_CHOICES = [
        ('Non commencé', 'Non commencé'),
        ('En cours', 'En cours'),
        ('Terminé', 'Terminé'),
    ]

    projet = models.OneToOneField(Projet, on_delete=models.CASCADE)
    date_debut = models.DateField(null=True, blank=True)
    date_fin = models.DateField(null=True, blank=True)
    montant_remboursement = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    description = models.TextField()
    date_contrat = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='Non commencé')
    def __str__(self):
        return f"{self.projet.nom} -> {self.montant_remboursement}"
    
class Remboursement(models.Model):
    STATUT_CHOICES = [
        ('En attente', 'En attente'),
        ('Approuvé', 'Approuvé'),
        ('Refusé', 'Refusé')
    ]
    
    MODE_PAIEMENT_CHOICES = [
        ('Virement bancaire', 'Virement bancaire'),
        ('PayPal', 'PayPal'),
        ('Espèces', 'Espèces'),
        ('Chèque', 'Chèque')
    ]
    
    contratremboursement = models.ForeignKey(ContratRemboursement, on_delete=models.CASCADE, related_name="remboursements")
    actionnaire = models.ForeignKey(User, on_delete=models.CASCADE)
    montant_remboursement = models.DecimalField(max_digits=10, decimal_places=2)
    date_remboursement = models.DateField(null=True, blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='En attente')
    justification = models.TextField()
    mode_paiement = models.CharField(max_length=20, choices=MODE_PAIEMENT_CHOICES, default='Espèces')

    def __str__(self):
        return f"Remboursement {self.montant_remboursement}€ - {self.actionnaire.first_name} {self.actionnaire.last_name} - {self.statut}"

class SignatureContrat(models.Model):

    contratremboursement = models.ForeignKey(ContratRemboursement, on_delete=models.CASCADE, related_name="signaturecontrats")
    membre = models.ForeignKey(User, on_delete=models.CASCADE)
    date_signature = models.DateField(null=True, blank=True, auto_now_add=True)
    
class SignatureRemboursement(models.Model):

    remboursement = models.ForeignKey(Remboursement, on_delete=models.CASCADE, related_name="signatureremboursements")
    membre = models.ForeignKey(User, on_delete=models.CASCADE)
    date_signature = models.DateField(null=True, blank=True, auto_now_add=True)