from django.db import models
from django.contrib.auth.models import User
from forum.models import*

class Cours(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, null=False)
    composant = models.ForeignKey(Composant, on_delete=models.CASCADE, null=False)
    file = models.FileField(upload_to="upload", null=False)
    title = models.CharField(max_length=100, null=True)
    LEVEL=[
        ('Baccalauréat','Baccalauréat'),
        ('Bac + 1','Bac + 1'),
        ('Bac + 2','Bac + 2'),
        ('Bac + 3','Bac + 3'),
        ('Bac + 4','Bac + 4'),
        ('Bac + 5','Bac + 5'),
        ('Bac + 6','Bac + 6'),
        ('Bac + 7','Bac + 7'),
    ]
    niveau = models.CharField(max_length=200, null=True, choices=LEVEL)
    comment = models.CharField(max_length=500, null=True)
    TP=[
        ('Gratuit','Gratuit'),
        ('Payant','Payant')
    ]
    type = models.CharField(max_length=100, null=True, choices=TP)
    price = models.IntegerField(default=0, null=True)
    date = models.DateField(auto_created=True)
    ST = [
        ('Traitement en cours','Traitement en cours'),
        ('Cours publié','Cours publié'),
        ('Cours non retenu','Cours non retenu')
    ]
    status = models.CharField(max_length=100, null=True, choices=ST, default="Traitement en cours")
    st = models.IntegerField(default=0,null=True)
    content = models.TextField(null=True)

class Panier(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    cquantite = models.TextField(max_length=100, null=True)

class ModePaiement(models.Model):
    typepaiement = models.TextField(max_length=100, null=False)
    libelle = models.TextField(max_length=100, default="", null=True)
    numero = models.TextField(max_length=100, default="", null=True)

class Commande(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    ucours = models.TextField(max_length=500,null=True)
    total = models.IntegerField(null=False)
    datecommande = models.DateTimeField(auto_now_add=True, null=True)
    status = models.BooleanField(default=False)
    statusachat = models.BooleanField(default=False)
    modepaiement = models.ForeignKey(ModePaiement, on_delete=models.CASCADE, null=True)
    phone = models.TextField(max_length=100, default="")
    st = [
        ('Commande en cours de traitement','Commande en cours de traitement'),
        ('Commande validée','Commande validée'),
        ('Commande non validée','Commande non validée')
    ]
    validation = models.CharField(max_length=50 , choices=st, default="Commande en cours de traitement", null=True)
    comment = models.TextField(max_length=200, default="")
    transaction_id = models.CharField(max_length=100)
    status_payment = models.CharField(max_length=50, default='pending')
    
    def __str__(self):
        return self.transaction_id

class Payment(models.Model):
    transaction_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    phone_number = models.CharField(max_length=15)
    status = models.CharField(max_length=50, default='pending')
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.transaction_id