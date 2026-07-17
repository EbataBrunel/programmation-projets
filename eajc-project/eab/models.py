from django.db import models
from django.contrib.auth.models import User
from etablissement.models import*
from formation.models import*
from entreprise.models import*
from ckeditor.fields import RichTextField
from datetime import datetime

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=100)
    address = models.TextField()
    photo = models.ImageField(upload_to="media", null=True, blank=True)
    SEX = [
        ('Masculin','Masculin'),
        ('Feminin','Feminin')
    ]
    gender = models.CharField(max_length=100, null=True, choices=SEX)
    LIST_COUNTRY = [
        ('Afrique du Sud','Afrique du Sud'),
        ('Afghanistan','Afghanistan'),
        ('Albanie','Albanie'),
        ('Algérie','Algérie'),
        ('Allemagne','Allemagne'),
        ('Andorre','Andorre'),
        ('Angola','Angola'),
        ('Antigua-et-Barbuda','Antigua-et-Barbuda'),
        ('Arabie Saoudite','Arabie Saoudite'),
        ('Argentine','Argentine'),
        ('Arménie','Arménie'),
        ('Australie','Australie'),
        ('Autriche','Autriche'),
        ('Azerbaïdjan','Azerbaïdjan'),
        ('Bahamas','Bahamas'),
        ('Bahreïn','Bahreïn'),
        ('Bangladesh','Bangladesh'),
        ('Barbade','Barbade'),
        ('Belgique','Belgique'),
        ('Belize','Belize'),
        ('Bénin','Bénin'),
        ('Bhoutan','Bhoutan'),
        ('Biélorussie','Biélorussie'),
        ('Birmanie','Birmanie'),
        ('Bolivie','Bolivie'),
        ('Bosnie-Herzégovine','Bosnie-Herzégovine'),
        ('Botswana','Botswana'),
        ('Brésil','Brésil'),
        ('Brunei','Brunei'),
        ('Bulgarie','Bulgarie'),
        ('Burkina Faso','Burkina Faso'),
        ('Burundi','Burundi'),
        ('Cambodge','Cambodge'),
        ('Cameroun','Cameroun'),
        ('Canada','Canada'),
        ('Cap-Vert','Cap-Vert'),
        ('Chili','Chili'),
        ('Chine','Chine'),
        ('Chypre','Chypre'),
        ('Colombie','Colmobie'),
        ('Comores','Comores'),
        ('Congo-Brazzaville','Congo-Brazzaville'),
        ('Corée du Nord','Corée du Nord'),
        ('Corée du Sud','Corée du Sud'),
        ('Costa Rica','Costa Rica'),
        ('Côte d’Ivoire','Côte d’Ivoire'),
        ('Croatie','Croatie'),
        ('Cuba','Cuba'),
        ('Danemark','Danemark'),
        ('Djibouti','Djibouti'),
        ('Dominique','Dominique'),
        ('Égypte','Égypte'),
        ('Émirats arabes unis','Émirats arabes unis'),
        ('Équateur','Équateur'),
        ('Érythrée','Érythrée'),
        ('Espagne','Espagne'),
        ('Eswatini','Eswatini'),
        ('Estonie','Estonie'),
        ('États-Unis','États-Unis'),
        ('Éthiopie','Éthiopie'),
        ('Fidji','Fidji'),
        ('Finlande','Finlande'),
        ('France','France'),
        ('Gabon','Gabon'),
        ('Gambie','Gambie'),
        ('Géorgie','Géorgie'),
        ('Ghana','Ghana'),
        ('Grèce','Grèce'),
        ('Grenade','Grenade'),
        ('Guatemala','Guatemala'),
        ('Guinée','Guinée'),
        ('Guinée équatoriale','Guinée équatoriale'),
        ('Guinée-Bissau','Guinée-Bissau'),
        ('Guyana','Guyana'),
        ('Haïti','Haïti'),
        ('Honduras','Honduras'),
        ('Hongrie','Hongrie'),
        ('Îles Cook','Îles Cook'),
        ('Îles Marshall','Îles Marshall'),
        ('Inde','Inde'),
        ('Indonésie','Indonésie'),
        ('Irak','Irak'),
        ('Iran','Iran'),
        ('Irlande','Irlande'),
        ('Islande','Islande'),
        ('Israël','Israël'),
        ('Italie','Italie'),
        ('Jamaïque','Jamaïque'),
        ('Japon','Japon'),
        ('Jordanie','Jordanie'),
        ('Kazakhstan','Kazakhstan'),
        ('Kenya','Kenya'),
        ('Kirghizistan','Kirghizistan'),
        ('Kiribati','Kiribati'),
        ('Koweït','Koweït'),
        ('Laos','Laos'),
        ('Lesotho','Lesotho'),
        ('Lettonie','Lettonie'),
        ('Liban','Liban'),
        ('Liberia','Liberia'),
        ('Libye','Libye'),
        ('Liechtenstein','Liechtenstein'),
        ('Lituanie','Lituanie'),
        ('Luxembourg','Luxembourg'),
        ('Macédoine','Macédoine'),
        ('Madagascar','Madagascar'),
        ('Malaisie','Malaisie'),
        ('Malawi','Malawi'),
        ('Maldives','Maldives'),
        ('Mali','Mali'),
        ('Malte','Malte'),
        ('Maroc','Maroc'),
        ('Maurice','Maurice'),
        ('Mauritanie','Mauritanie'),
        ('Mexique','Mexique'),
        ('Micronésie','Micronésie'),
        ('Moldavie','Moldavie'),
        ('Monaco','Monaco'),
        ('Mongolie','Mongolie'),
        ('Monténégro','Monténégro'),
        ('Mozambique','Mozambique'),
        ('Namibie','Namibie'),
        ('Nauru','Nauru'),
        ('Népal','Katmandou'),
        ('Nicaragua','Nicaragua'),
        ('Niger','Niger'),
        ('Nigeria','Nigeria'),
        ('Niue','Niue'),
        ('Norvège','Norvège'),
        ('Nouvelle-Zélande','Nouvelle-Zélande'),
        ('Oman','Oman'),
        ('Ouganda','Ouganda'),
        ('Ouzbékistan','Ouzbékistan'),
        ('Pakistan','Pakistan'),
        ('Palaos','Palaos'),
        ('Palestine','Palestine'),
        ('Panama','Panama'),
        ('Papouasie-Nouvelle-Guinée','Papouasie-Nouvelle-Guinée'),
        ('Paraguay','Paraguay'),
        ('Pays-Bas','Pays-Bas'),
        ('Pérou','Pérou'),
        ('Philippines','Philippines'),
        ('Pologne','Pologne'),
        ('Portugal','Portugal'),
        ('Qatar','Qatar'),
        ('République centrafricaine','République centrafricaine'),
        ('République démocratique du Congo','République démocratique du Congo'),
        ('République Dominicaine','République Dominicaine'),
        ('République tchèque','République tchèque'),
        ('Roumanie','Roumanie'),
        ('Royaume-Uni','Royaume-Uni'),
        ('Russie','Russie'),
        ('Rwanda','Rwanda'),
        ('Saint-Kitts-et-Nevis','Saint-Kitts-et-Nevis'),
        ('Saint-Vincent-et-les-Grenadines','Saint-Vincent-et-les-Grenadines'),
        ('Sainte-Lucie','Sainte-Lucie'),
        ('Saint-Marin','Saint-Marin'),
        ('Salomon','Salomon'),
        ('Salvador','Salvador'),
        ('Samoa','Samoa'),
        ('São Tomé-et-Principe','São Tomé-et-Principe'),
        ('Sénégal','Sénégal'),
        ('Serbie','Serbie'),
        ('Seychelles','Seychelles'),
        ('Sierra Leone','Sierra Leone'),
        ('Singapour','Singapour'),
        ('Slovaquie','Slovaquie'),
        ('Slovénie','Slovénie'),
        ('Somalie','Somalie'),
        ('Soudan','Soudan'),
        ('Soudan du Sud','Soudan du Sud'),
        ('Sri Lanka','Sri Lanka'),
        ('Suède','Suède'),
        ('Suisse','Suisse'),
        ('Suriname','Suriname'),
        ('Syrie','Syrie'),
        ('Tadjikistan','Tadjikistan'),
        ('Tanzanie','Tanzanie'),
        ('Tchad','Tchad'),
        ('Thaïlande','Thaïlande'),
        ('Timor oriental','Timor oriental'),
        ('Togo','Togo'),
        ('Tonga','Tonga'),
        ('Trinité-et-Tobago','Trinité-et-Tobago'),
        ('Tunisie','Tunisie'),
        ('Turkménistan','Turkménistan'),
        ('Turquie','Turquie'),
        ('Tuvalu','Tuvalu'),
        ('Ukraine','Ukraine'),
        ('Uruguay','Uruguay'),
        ('Vanuatu','Vanuatu'),
        ('Vatican','Vatican'),
        ('Venezuela','Venezuela'),
        ('Viêt Nam','Viêt Nam'),
        ('Yémen','Yémen'),
        ('Zambie','Zambie'),
        ('Zimbabwe','Zimbabwe')
    ]
    country = models.CharField(max_length=100, null=True, choices=LIST_COUNTRY)
    droitmes = models.BooleanField(default=False, null=True)
    status = models.BooleanField(default=False, null=True) #visibilité du profil
    vp = models.BooleanField(default=False, null=True) #Visibilité du parcours
    apropos = models.TextField(null=True)
    nature_recherche = models.TextField(null=True)
    profession = models.CharField(max_length=50, null=True)
    VARIABLE = [
        ('Visible','Visible'),
        ('Invisible','Invisible')
    ]
    vform = models.CharField(max_length=100, null=True, choices=VARIABLE, default="Visible")
    vep = models.CharField(max_length=100, null=True, choices=VARIABLE, default="Visible")
    vcomp = models.CharField(max_length=100, null=True, choices=VARIABLE, default="Visible")
    vaform = models.CharField(max_length=100, null=True, choices=VARIABLE, default="Visible")
    vref = models.CharField(max_length=100, null=True, choices=VARIABLE, default="Visible")
    priority = models.BooleanField(null=True,default=False)
    status_deleteaccount = models.IntegerField(null=True, default=0)
    just_costumer = models.CharField(max_length=100, null=True)
    linkedin = models.CharField(max_length=500, null=True, default="")
    portfolio = models.CharField(max_length=500, null=True, default="")
    github = models.CharField(max_length=500, null=True, default="")
    

    def __str__(self):
        return str(self.user)
    
class Annee(models.Model):
    libelle = models.CharField(max_length=4, unique=True, null=True)

    def __str__(self):
        return self.libelle
    
class Parametre(models.Model):
    appname = models.CharField(max_length=100)
    appeditor = models.CharField(max_length=200)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    version = models.CharField(max_length=10, null=True)
    devise = models.CharField(max_length=10, null=True)
    COLORS = [
        ('primary','primary'),
        ('info','info'),
        ('success','success'),
        ('danger','danger'),
        ('secondary','secondary'),
        ('dark','dark'),
    ]
    theme = models.CharField(max_length=200, null=True, choices=COLORS)
    logo = models.ImageField(upload_to="media", null=True, blank=True)
    width_logo = models.CharField(max_length=3, null=True)
    height_logo = models.TextField(max_length=3, null=True)
    maintenance_mode = models.BooleanField(default=False)

    def __str__(self):
        return self.appname
    
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.TextField()
    message = models.TextField(null=True)
    datecontact = models.DateTimeField(default=datetime.now, null=True, blank=True)
    statut = models.IntegerField(null=True)
    codes = models.CharField(max_length=300, null=True)
    status = models.IntegerField(null=True)
    statutdel = models.IntegerField(null=True, default=0)

    def __str__(self):
        return self.name
    


