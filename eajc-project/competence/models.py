from django.db import models
from django.contrib.auth.models import User

class TypeCompetence(models.Model):   
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class Competence(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    type_competence = models.ForeignKey(TypeCompetence, on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=200, null=True)
    comment = models.TextField(null=True)
    status = models.BooleanField(null=True,default=True)

    def __str__(self):
        return self.name

