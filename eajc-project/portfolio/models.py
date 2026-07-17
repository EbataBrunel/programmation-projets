from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    #image = models.ImageField(upload_to='projects/')
    link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title
    
class ContactPortfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField(null=True)
    datecontact = models.DateTimeField(default=datetime.now, null=True, blank=True)
    status = models.IntegerField(null=True, default=0)

    def __str__(self):
        return self.name
    
class These(models.Model):
    auteur = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    titre = models.CharField(max_length=255, verbose_name="Titre de la thèse")
    universite = models.CharField(max_length=255, verbose_name="Université", blank=True, null=True)
    date_soutenance = models.DateField(verbose_name="Date de soutenance")
    resume = models.TextField(verbose_name="Résumé", blank=True)

    def __str__(self):
        return self.titre
    
class Article(models.Model):
    auteur = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    titre = models.CharField(max_length=255, verbose_name="Titre de l'article")
    resume = models.TextField(verbose_name="Résumé", blank=True)
    date_publication = models.DateField(verbose_name="Date de publication", null=True, blank=True)
    revue = models.CharField(max_length=255, verbose_name="Revue/Conférence", blank=True)
    volume = models.CharField(max_length=50, verbose_name="Volume", blank=True)
    numero = models.CharField(max_length=50, verbose_name="Numéro", blank=True)
    pages = models.CharField(max_length=50, verbose_name="Pages", blank=True)
    doi = models.CharField(max_length=255, verbose_name="DOI", blank=True)
    file = models.FileField(upload_to="articles/", verbose_name="Fichier PDF", blank=True, null=True)
    url = models.URLField(max_length=255, verbose_name="Lien URL", blank=True)
    keywords = models.TextField(verbose_name="Mots-clés", blank=True)
    categorie = models.CharField(max_length=100, verbose_name="Catégorie", blank=True)
    these = models.ForeignKey(These, on_delete=models.CASCADE, verbose_name="Thèse associée", related_name="articles")

    def __str__(self):
        return self.titre
