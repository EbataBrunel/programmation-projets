from django.db import models
from django.contrib.auth.models import User
from anneeacademique.models import AnneeCademique

class ResumeJournanlier(models.Model):
    content = models.CharField(max_length=300, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    anneeacademique = models.ForeignKey(AnneeCademique, on_delete=models.CASCADE, null=False)
    date_resume = models.DateTimeField(null=True, blank=True)
    status = models.IntegerField(default=0, null=False) # Statut de lecture
    
    def __str__(self):
        return self.content
    
