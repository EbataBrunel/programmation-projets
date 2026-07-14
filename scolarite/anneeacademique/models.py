from django.db import models

class AnneeCademique(models.Model):
    annee_debut = models.IntegerField(default=2000, null=True)
    annee_fin =  models.IntegerField(default=2001, null=True)
    separateur = models.CharField(max_length=1, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    status_cloture = models.BooleanField(default=False, null=True)
    
    def __str__(self):
        return str(self.annee_debut)+""+self.separateur+""+str(self.annee_fin)
    
    

