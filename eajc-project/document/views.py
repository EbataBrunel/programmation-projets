
# Importation des modules tiers
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from eab.utils import send_email_with_html_body
from django.db import transaction
from django.template.loader import get_template
from django.contrib.sites.shortcuts import get_current_site
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from django.urls import reverse
from datetime import timedelta
# Importation des modules locaux
from eab.views import nbnew_answer, nbnew_message, new_message, parametre
from eajc.utils.crypto import dechiffrer_param, chiffrer_param
from .models import*
from eab.models import*
from forum.models import*
from document.models import*
from app_auth.decorator import*
# Importation des modules standards
import os
import pdfkit
import datetime
import bleach
import hashlib
import uuid
import stripe
import requests
import base64
import json


# Configure la clé secrète
stripe.api_key = settings.STRIPE_SECRET_KEY

# Acceder au token
def get_access_token():
    # Encodage de la clé primaire en format Base64 pour l'authentification
    primary_key = settings.MTN_PRIMARY_KEY
    encoded_key = base64.b64encode(f"{primary_key}:".encode()).decode()

    url = "https://sandbox.momodeveloper.mtn.com/v1_0/apiuser"
    headers = {
        "Authorization": f"Basic {encoded_key}",
        "Ocp-Apim-Subscription-Key": primary_key,
    }
    response = requests.post(url, headers=headers)

    # Vérifie si la requête est réussie
    if response.status_code == 201:
        return response.json().get("access_token")
    else:
        print("Error:", response.status_code, response.text)  # Ajout pour voir le problème exact
        return None
    
#print(get_access_token())

def userPriority():
    users = User.objects.all()
    #Memebre prioritaire
    tabUserPriority = []
    count = 0
    for user in users:
        try:
            if user.profile and user.profile.priority == 1:
                if count <=2:
                    tabUserPriority.append(user)
                    count += 1
        except:
            pass
    return tabUserPriority

def get_file_hash(file):
    hash_md5 = hashlib.md5() # Cette objet de MD5 servira de stocker et calculer l'empreinte MD5.
    for chunk in file.chunks(): # Parcourir le fichier par morceau pour ne pas surcherger la memoire
        hash_md5.update(chunk) # Ajout de chaque morceau au calcul de hash et en mettant en même à jour le hash
    return hash_md5.hexdigest() # retourner l'empreinte MD5 sous forme de chaîne hexadécimale

# Resumer d'un achat
def purchase_summary(id):
    commande = Commande.objects.get(id=id)
    panier = eval(commande.ucours)
    prix_total = 0
    qte_totale = 0
    achats = []
    for k,v in panier.items():
        dic = {}
        dic["id"] = k
        dic["quantite"] = v[0]
        dic["discipline"] = v[1]
        dic["composant"] = v[2]
        dic["title"] = v[3]
        dic["comment"] = v[4]
        dic["price"] = v[5]
        achats.append(dic)

        qte_totale += v[0]
        prix_total += v[5]
        
    return qte_totale, prix_total, commande, achats

# Résumer de la commande
def order_summary(user):
    try:
        panier = Panier.objects.get(user_id=user.id)
    except Exception as e:
        panier = None
    
    if panier == None:
        return redirect("cours/cours")
    paniers = eval(panier.cquantite)
    #On calcule le prix total d'achat
    prix_total = 0
    qte_total = 0
    documents = []
    for key,value in paniers.items():
        qte_total += value[0] # Quantité totale
        prix_total += value[5] # Somme totale à payer
        
        dic = {}
        dic["id"] = key
        dic["quantite"] = value[0]
        dic["discipline"] = value[1]
        dic["composant"] = value[2]
        dic["title"] = value[3]
        dic["comment"] = value[4]
        dic["price"] = value[5]
        
        documents.append(dic)
        
    return qte_total, prix_total, documents

@login_required(login_url='connection/login')
def mescours(request):
    date = datetime.datetime.now()

    cours = Cours.objects.values("discipline_id").filter(user_id=request.user.id).annotate(effectif=Count("discipline_id"))
    tabCours = []
    for course in cours:
        dic = {}
        discipline = Discipline.objects.get(id=course["discipline_id"])
        dic["discipline"] = discipline
        dic["effectif"] = course["effectif"]
        #On fait une mise à jour de statut
        list_cours = Cours.objects.filter(discipline_id=course["discipline_id"], user_id=request.user.id, st=1)
        for d in list_cours:
            d.st = 2
            d.save()
        #On compte le nombre de nouvelles notifications
        countnotif = Cours.objects.filter(discipline_id=course["discipline_id"],user_id=request.user.id, st=2).count()
        dic["countnotif"] = countnotif
        tabCours.append(dic)

    context = {
        "cours":tabCours,
        "date":date,
        "parametre":parametre(),
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request),
    }
    return render(request, "cours/mescours.html", context)

def ajax_delete_document_discipline(request, id):
    discipline = Discipline.objects.get(id=id)
    context = {
        "discipline": discipline
    }
    return render(request, "ajax_delete_document_discipline.html", context)

#Suppression des documents d'une discipline d'un membre
@login_required(login_url='connection/login')
def delete_document_discipline(request,id):
    discipline_id = dechiffrer_param(str(id))
    cours = Cours.objects.filter(discipline_id=discipline_id, user_id=request.user.id)
    for cour in cours:
        # Vérifier si la lettre de motivation a un fichié associé et que le fichier existe réellement
        if cour.file and hasattr(cour.file, 'path'):
            """
            Suppression de la lettre de motivation et en même temps du fichier  
            """
            # Chemin complet du fichier
            file_path = cour.file.path
            # Verifier l'existence du fichier
            if os.path.exists(file_path):
                os.remove(file_path)
        cour.delete()
    return redirect("cours/mescours")

@login_required(login_url='connection/login')
def d_cours(request, id):
    date = datetime.datetime.now()
    discipline_id = dechiffrer_param(str(id))
    discipline = Discipline.objects.get(id=discipline_id)
    cours = Cours.objects.values("composant_id").filter(discipline_id=discipline_id,user_id=request.user.id).annotate(effectif=Count("composant_id"))
    tabComposants = []
    for course in cours:
        dic = {}
        composant = Composant.objects.get(id=course["composant_id"])
        dic["composant"] = composant
        dic["effectif"] = course["effectif"]
        #On fait une mise à jour de statut
        list_cours = Cours.objects.filter(composant_id=course["composant_id"], user_id=request.user.id, st=2)
        for d in list_cours:
            d.st = 3
            d.save()
        #On compte le nombre de nouvelles notifications
        countnotif = Cours.objects.filter(composant_id=course["composant_id"],user_id=request.user.id, st=3).count()
        dic["countnotif"]=countnotif
        tabComposants.append(dic)

    context = {
        "discipline":discipline,
        "composants":tabComposants,
        "date":date,
        "parametre":parametre(),
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request),
    }
    return render(request, "cours/d-cours.html", context)

def ajax_delete_document_composant(request, id):
    composant = Composant.objects.get(id=id)
    context = {
        "composant": composant
    }
    return render(request, "ajax_delete_document_composant.html", context)

#Suppression des documents de composant d'un membre
@login_required(login_url='connection/login')
def delete_document_composant(request,id):
    composant=Composant.objects.get(id=id)
    cours=Cours.objects.filter(composant_id=id, user_id=request.user.id)
    for cour in cours:
        # Vérifier si la lettre de motivation a un fichié associé et que le fichier existe réellement
        if cour.file and hasattr(cour.file, 'path'):
            # Chemin complet du fichier
            file_path = cour.file.path
            # Verifier l'existence du fichier
            if os.path.exists(file_path):
                os.remove(file_path)
        cour.delete()
    return redirect("d-cours", id=chiffrer_param(str(composant.discipline_id)))


@login_required(login_url='connection/login')
def details_cours(request, id):
    date = datetime.datetime.now()
    composant_id = dechiffrer_param(str(id))
    composant = Composant.objects.get(id=composant_id)
    cours = Cours.objects.filter(composant_id=composant_id, user_id=request.user.id)
    #On fait une mise à jour de statut
    list_cours = Cours.objects.filter(composant_id=composant_id, user_id=request.user.id, st=3)
    for d in list_cours:
        d.st = 4
        d.save()
    
    context = {
        "composant":composant,
        "cours":cours,
        "date":date,
        "parametre":parametre(),
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request),
    }
    return render(request, "cours/details-cours.html", context)

def ajax_detail_document(request, id):
    cours = Cours.objects.get(id=id)
    context = {
        "course": cours
    }
    return render(request, "ajax_detail_document.html", context)

def ajax_delete_document(request, id):
    cours = Cours.objects.get(id=id)
    context = {
        "cours": cours
    }
    return render(request, "ajax_delete_document.html", context)

#=========== Suppression des documents d'un memebre ====================
@login_required(login_url='connection/login')
def delete_document(request, id, code):
    cours_id = dechiffrer_param(str(id))
    cours = Cours.objects.get(id=cours_id)
    # Vérifier si la lettre de motivation a un fichié associé et que le fichier existe réellement
    if cours.file and hasattr(cours.file, 'path'):
        # Chemin complet du fichier
        file_path = cours.file.path
        # Verifier l'existence du fichier
        if os.path.exists(file_path):
            os.remove(file_path)
    cours.delete()
    return redirect("cours/details-cours", id=chiffrer_param(str(code)))

@login_required(login_url='connection/login')
def add_cours(request):
    date = datetime.datetime.now()

    if request.method == "POST":
        title = bleach.clean(request.POST["title"].strip())
        file = request.FILES["file"]
        comment = bleach.clean(request.POST["comment"].strip())
        type = request.POST["type"]
        price = 0
        if type == "Payant":
            price = request.POST["price"]
        
        discipline = request.POST["discipline"]
        composant = request.POST["composant"]
        niveau = request.POST["niveau"]
        
        if niveau == "Autre niveau":
            autre_niveau = bleach.clean(request.POST["autre_niveau"].strip())
            niveau = autre_niveau 
            
        # Vérifier l'extension du fichier
        if not file.name.endswith('.pdf'):
            return JsonResponse({
                    "status": "error",
                    "message": "Seuls les fichiers PDF sont acceptés."})  
        elif file.size > 10 * 1024 * 1024: # Limiter la taille du fichier à 10 Mo
            return JsonResponse({
                    "status": "error",
                    "message": "La taille du fichier est limitée à 10 Mo."})
        else:
            
            liste_cours = Cours.objects.all()
            liste_empreint_md5 = []
            for l in liste_cours:
                liste_empreint_md5.append(get_file_hash(l.file))
                l.file.close()  # Fermer le fichier après le calcul du hash
                    
            if get_file_hash(file) in liste_empreint_md5:
                return JsonResponse({
                    "status": "error",
                    "message": "Ce document existe déjà."})
            else:
                cours = Cours(
                    date=date,
                    file=file,
                    comment=comment,
                    type=type,
                    price=price,
                    composant_id=composant,
                    discipline_id=discipline,
                    user_id=request.user.id,
                    niveau=niveau,
                    title=title)
                count0 = Cours.objects.all().count()
                cours.save()
                count1 = Cours.objects.all().count()
                # Verifier si l'ajout a été bien effectué ou pas
                if count0 < count1:
                    return JsonResponse({
                        "status": "success",
                        "message": "Document enregistré avec succès."})
                else:
                    return JsonResponse({
                        "status": "error",
                        "message": "L'insertion a échouée."})
        
    disciplines = Discipline.objects.all()
    niveaux = ["Bac + 1", "Bac + 2", "Bac + 3", "Bac + 4", "Bac + 5", "Bac + 6", "Bac + 7", "Autre niveau" ]
    context = {
        "disciplines":disciplines,
        "date":date,
        "niveaux":niveaux,
        "parametre":parametre(),
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request),
    }
    return render(request, "cours/add_cours.html", context)

@login_required(login_url='connection/login')
def edit_cours(request,id):
    date = datetime.datetime.now()
    cours_id = dechiffrer_param(str(id))
    cours = Cours.objects.get(id=cours_id)   
    #Vérifier si ce membre est authorisé à acceder à cette page ou pas.
    query = Cours.objects.filter(id=cours_id,user_id=request.user.id)
    if query.exists():
    
        disciplines = Discipline.objects.all()
        tabDisciplines = []
        for discipline in disciplines:
            if discipline.id != cours.discipline.id:
                tabDisciplines.append(discipline)

        composants = Composant.objects.filter(discipline_id=cours.discipline.id)
        tabComposants = []
        for composant in composants:
            if composant.id != cours.composant.id:
                tabComposants.append(composant)
                
        niveaux=["Bac + 1", "Bac + 2", "Bac + 3", "Bac + 4", "Bac + 5", "Bac + 6", "Bac + 7", "Autre niveau" ]
        new_niveaux = []
        for niveau in niveaux:
            if cours.niveau != niveau:
                new_niveaux.append(niveau)
                
        context = {
            "cours":cours,
            "disciplines":tabDisciplines,
            "composants":tabComposants,
            "niveaux":niveaux,
            "date":date,
            "parametre":parametre(),
            "countanswer":nbnew_answer(request),
            "count":nbnew_message(request),
            "users":new_message(request),
        }
        return render(request, "cours/edit_cours.html", context)
    else:
        return redirect("authorization")

@login_required(login_url='connection/login')
def edit_cour(request):
   
   if request.method == "POST":
       
        id = request.POST["id"]
        try:
            cours = Cours.objects.get(id=id)
        except:
            cours = None
        
        if cours:
            title = bleach.clean(request.POST["title"].strip())
            niveau = request.POST["niveau"]
            
            if niveau == "Autre niveau":
                autre_niveau = bleach.clean(request.POST["autre_niveau"].strip())
                niveau = autre_niveau
                    
            comment = bleach.clean(request.POST["comment"].strip())
            type = request.POST["type"]
            price = request.POST["price"]
            prix = 0
            if price :
                prix = price

            file = None
            if request.POST.get('file', True):
                f = request.FILES["file"]
                # Vérifier l'extension du fichier
                if not f.name.endswith('.pdf'):
                    return JsonResponse({
                        "status": "error",
                        "message": "Seuls les fichiers PDF sont acceptés."})    
                elif f.size > 10 * 1024 * 1024: # Limiter la taille du fichier à 10 Mo
                    return JsonResponse({
                        "status": "error",
                        "message": "La taille du fichier est limitée à 10 Mo."})
                else:
                    file = f
            discipline = request.POST["discipline"]
            composant = request.POST["composant"]

            cours.title = title
            cours.niveau = niveau
            cours.type = type
            cours.price = prix
            if file is not None:
                liste_cours = Cours.objects.all()
                liste_empreint_md5 = []
                for l in liste_cours:
                    liste_empreint_md5.append(get_file_hash(l.file))
                    l.file.close()  # Fermer le fichier après le calcul du hash
                        
                if get_file_hash(file) in liste_empreint_md5:
                    return JsonResponse({
                        "status": "error",
                        "message": "Ce document existe déjà."})
                else:
                    # Vérifier si la lettre de motivation a un fichié associé et que le fichier existe réellement
                    if cours.file and hasattr(cours.file, 'path'):
                        #Suppression de la lettre de motivation et en même temps du fichier
                        # Chemin complet du fichier
                        file_path = cours.file.path
                        # Verifier l'existence du fichier
                        if os.path.exists(file_path):
                            os.remove(file_path)
                        
                cours.file = file
            cours.comment = comment
            cours.composant_id = composant
            cours.discipline_id = discipline

            cours.save()
            return JsonResponse({
                "status": "success",
                "message": "Document modifié avec succès."})

    

class getCompDiscipline(View):
    def get(self, request, id, *args, **kwargs):    
        composants = Composant.objects.filter(discipline_id=id)
        context = {
            "composants":composants
        }
        return render(request, "ajaxCompDisc.html", context)
    
class getPrice(View):
    def get(self, request, id, *args, **kwargs):    
        type = id
        context = {
            "type":type,
            "parametre":parametre(),
        }
        return render(request, "ajaxType.html", context)

def cours(request):
    date = datetime.datetime.now()

    liste_cours = Cours.objects.values("composant_id").filter(status="Cours publié").annotate(effectif=Count("composant_id")).order_by("discipline_id")
    tabComposant = []
    for item in liste_cours:
        dic = {}
        composant = Composant.objects.get(id=item["composant_id"])
        dic["id"] = item["composant_id"]
        dic["libelle"] = composant.libelle
        dic["effectif"] = item["effectif"]
        tabComposant.append(dic)

    cours = Cours.objects.filter(status="Cours publié").order_by("-date")

    paginator = Paginator(cours, 12)
    num_page = request.GET.get('page')
    cours = paginator.get_page(num_page)
    #On affiche la valeur du panier
    try:
        panier = Panier.objects.get(user_id=request.user.id)
    except Exception as e:
        panier = None
    
    count = 0
    if panier == None:
        pass
    else : 
        cpanier = eval(panier.cquantite)
        count = len(cpanier)
    
    context = {
        "count":count,
        "composants":tabComposant,
        "cours":cours,
        "date":date,
        "userpriorities":userPriority(),
        "parametre":parametre(),
    }
    return render(request, "cours/cours.html", context)

def details(request,id):
    date = datetime.datetime.now()
    cours_id = dechiffrer_param(str(id))
    cours = Cours.objects.get(id=cours_id)
    #On affiche la valeur du panier
    try:
        panier = Panier.objects.get(user_id=request.user.id)
    except Exception as e:
        panier = None
    
    count = 0
    if panier == None:
        pass
    else : 
        cpanier = eval(panier.cquantite)
        count = len(cpanier)

    context = {
        "count":count,
        "course":cours,
        "date":date,
        "userpriorities":userPriority(),
        "parametre":parametre(),
    }
    return render(request, "cours/details.html", context)


class getCours(View):
    def get(self, request, id, *args, **kwargs): 

        cours = Cours.objects.filter(status="Cours publié", composant_id=id)

        paginator = Paginator(cours, 12)
        num_page = request.GET.get('page')
        cours = paginator.get_page(num_page)

        composant = Composant.objects.get(id=id)

        context = {
            "composant":composant,
            "cours":cours,
            "parametre":parametre(),
        }
        return render(request, "ajaxCours.html", context)
    
@login_required(login_url='connection/login')
@allowed_users(allowed_roles=['admin'])
def listcours(request):
    date = datetime.datetime.now()

    cours = Cours.objects.values('discipline_id').annotate(effectif=Count("discipline_id"))
    tabCours = []
    for item in cours:
        discipline = Discipline.objects.get(id=item["discipline_id"])
        dic = {}
        dic["id"] = item["discipline_id"]
        dic["discipline"] = discipline.libelle
        dic["effectif"] = item["effectif"]
        tabCours.append(dic)

    context = {
            "cours":tabCours,
            "date":date,
            "parametre":parametre(),
            "countanswer":nbnew_answer(request),
            "count":nbnew_message(request),
            "users":new_message(request),
    }
    return render(request, "cours/listcours.html", context)

def ajax_delete_cours_discipline(request, id):
    discipline = Discipline.objects.get(id=id)
    context = {
        "discipline": discipline
    }
    return render(request, "ajax_delete_cours_discipline.html", context)

def delete_cours_discipline(request,id):
    discipline_id = dechiffrer_param(str(id))
    cours = Cours.objects.filter(discipline_id=discipline_id)
    for cour in cours:
        # Vérifier si la lettre de motivation a un fichié associé et que le fichier existe réellement
        if cour.file and hasattr(cour.file, 'path'):
            # Chemin complet du fichier
            file_path = cour.file.path
            # Verifier l'existence du fichier
            if os.path.exists(file_path):
                os.remove(file_path)
        cour.delete()
    return redirect("cours/listcours", id=cours.composant.id)

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=['admin'])
def detcours(request,id):
    date = datetime.datetime.now()
    discipline_id = dechiffrer_param(str(id))
    discipline = Discipline.objects.get(id=discipline_id)
    cours = Cours.objects.values('composant_id').filter(discipline_id=discipline_id).annotate(effectif=Count("composant_id"))
    tabCours = []

    for item in cours:
        composant = Composant.objects.get(id=item["composant_id"])
        dic = {}
        dic["id"] = item["composant_id"]
        dic["composant"] = composant.libelle
        dic["effectif"] = item["effectif"]
        tabCours.append(dic)

    context = {
            "discipline":discipline,
            "cours":tabCours,
            "date":date,
            "parametre":parametre(),
            "countanswer":nbnew_answer(request),
            "count":nbnew_message(request),
            "users":new_message(request),
    }
    return render(request, "cours/detcours.html", context)

def ajax_delete_cours_composant(request, id):
    composant = Composant.objects.get(id=id)
    context = {
        "composant": composant
    }
    return render(request, "ajax_delete_cours_composant.html", context)

def delete_cours_composant(request,id):
    composant = Composant.objects.get(id=id)
    cours = Cours.objects.filter(composant_id=id)
    for cour in cours:
        # Vérifier si la lettre de motivation a un fichié associé et que le fichier existe réellement
        if cour.file and hasattr(cour.file, 'path'):
            # Chemin complet du fichier
            file_path = cour.file.path
            # Verifier l'existence du fichier
            if os.path.exists(file_path):
                os.remove(file_path)
        cour.delete()
    return redirect("cours/detcours", id=chiffrer_param(str(composant.discipline_id)))

def ajax_delete_cours(request, id):
    cours = Cours.objects.get(id=id)
    context = {
        "cours": cours
    }
    return render(request, "ajax_delete_cours.html", context)

@login_required(login_url='connection/login')
def delete_cours(request, id):
    cours_id = dechiffrer_param(str(id))
    cours = Cours.objects.get(id=cours_id)
    #Suppression de la lettre de motivation et en même temps du fichier 
    # Vérifier si la lettre de motivation a un fichié associé et que le fichier existe réellement
    if cours.file and hasattr(cours.file, 'path'):
        # Chemin complet du fichier
        file_path = cours.file.path
        # Verifier l'existence du fichier
        if os.path.exists(file_path):
            os.remove(file_path)
    cours.delete()
    return redirect("cours/dcours", id=chiffrer_param(str(cours.composant.id)))

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=['admin'])
def dcours(request,id):
    date = datetime.datetime.now()
    composant_id = dechiffrer_param(str(id))
    composant = Composant.objects.get(id=composant_id)
    cours = Cours.objects.filter(composant_id=composant_id).order_by("-id")

    context = {
            "composant":composant,
            "cours":cours,
            "date":date,
            "parametre":parametre(),
            "countanswer":nbnew_answer(request),
            "count":nbnew_message(request),
            "users":new_message(request),
    }
    return render(request, "cours/dcours.html", context)

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=['admin'])
def viewcours(request,id):
    date = datetime.datetime.now()
    cours_id = dechiffrer_param(str(id))
    cours = Cours.objects.get(id=cours_id)

    if request.method == "POST":
        status = request.POST["status"]
        content = request.POST["content"]

        cours.status = status
        cours.content = content
        cours.st = 1
        cours.save()
        return redirect("cours/v-cours",id=id)

    context = {
            "cours":cours,
            "date":date,
            "parametre":parametre(),
            "countanswer":nbnew_answer(request),
            "count":nbnew_message(request),
            "users":new_message(request),
    }

    return render(request, "cours/v-cours.html", context)

# On determine les cours publiés
@login_required(login_url='connection/login')
@allowed_users(allowed_roles=['admin'])
def courspub(request):
    date = datetime.datetime.now()

    dataDiscipline = []
    disciplines = Cours.objects.values("discipline_id").filter(status="Cours publié").annotate(effectif=Count("discipline_id"))
    for data in disciplines:
        dic = {}
        discipline = Discipline.objects.get(id=data["discipline_id"])
        dic["id"] = data["discipline_id"]
        dic["libelle"] = discipline.libelle
        dic["effectif"] = data["effectif"]
        dataDiscipline.append(dic)

    context = {
            "disciplines":dataDiscipline,
            "date":date,
            "parametre":parametre(),
            "countanswer":nbnew_answer(request),
            "count":nbnew_message(request),
            "users":new_message(request),
    }
    return render(request, "cours/courspub.html", context)

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=['admin'])
def detcourspub(request,id):
    date = datetime.datetime.now()
    composant_id = dechiffrer_param(str(id))
    discipline = Discipline.objects.get(id=composant_id)

    dataComposant = []
    composants = Cours.objects.values("composant_id").filter(discipline_id=composant_id, status="Cours publié").annotate(effectif=Count("composant_id"))
    for data in composants:
        dic = {}
        composant = Composant.objects.get(id=data["composant_id"])
        dic["id"] = data["composant_id"]
        dic["libelle"] = composant.libelle
        dic["effectif"] = data["effectif"]
        dataComposant.append(dic)

    context = {
            "discipline":discipline,
            "composants":dataComposant,
            "date":date,
            "parametre":parametre(),
            "countanswer":nbnew_answer(request),
            "count":nbnew_message(request),
            "users":new_message(request),
    }
    return render(request, "cours/detcourspub.html", context)

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=['admin'])
def dcourspub(request,id):
    date = datetime.datetime.now()
    composant_id = dechiffrer_param(str(id))
    composant = Composant.objects.get(id=composant_id)
    cours = Cours.objects.filter(composant_id=composant_id, status="Cours publié").order_by("-id")
    context = {
            "composant":composant,
            "cours":cours,
            "date":date,
            "parametre":parametre(),
            "countanswer":nbnew_answer(request),
            "count":nbnew_message(request),
            "users":new_message(request),
    }
    return render(request, "cours/dcourspub.html", context)

def ajax_detail_document_publie(request, id):
    cours = Cours.objects.get(id=id)
    context = {
        "course": cours
    }
    return render(request, "ajax_detail_document_publie.html", context)

# On determine les cours publiés
@login_required(login_url='connection/login')
@allowed_users(allowed_roles=['admin'])
def coursencours(request):
    date = datetime.datetime.now()

    dataDiscipline = []
    disciplines = Cours.objects.values("discipline_id").filter(status="Traitement en cours").annotate(effectif=Count("discipline_id"))
    for data in disciplines:
        dic = {}
        discipline = Discipline.objects.get(id=data["discipline_id"])
        dic["id"] = data["discipline_id"]
        dic["libelle"] = discipline.libelle
        dic["effectif"] = data["effectif"]
        dataDiscipline.append(dic)

    context = {
            "disciplines":dataDiscipline,
            "date":date,
            "parametre":parametre(),
            "countanswer":nbnew_answer(request),
            "count":nbnew_message(request),
            "users":new_message(request),
    }
    return render(request, "cours/c-encours.html", context)

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=['admin'])
def detcoursencours(request,id):
    date = datetime.datetime.now()
    discipline_id = dechiffrer_param(str(id))
    discipline = Discipline.objects.get(id=discipline_id)

    dataComposant = []
    composants = Cours.objects.values("composant_id").filter(discipline_id=discipline_id, status="Traitement en cours").annotate(effectif=Count("composant_id"))
    for data in composants:
        dic = {}
        composant = Composant.objects.get(id=data["composant_id"])
        dic["id"] = data["composant_id"]
        dic["libelle"] = composant.libelle
        dic["effectif"] = data["effectif"]
        dataComposant.append(dic)

    context = {
            "discipline":discipline,
            "composants":dataComposant,
            "date":date,
            "parametre":parametre(),
            "countanswer":nbnew_answer(request),
            "count":nbnew_message(request),
            "users":new_message(request),
    }
    return render(request, "cours/detcoursencours.html", context)

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=['admin'])
def dcoursencours(request,id):
    date = datetime.datetime.now()
    composant_id = dechiffrer_param(str(id))
    if request.method == "POST":
        cours_id = request.POST["id"]
        status = request.POST["status"]
        content = bleach.clean(request.POST["content"].strip())
        """
        etat = 0
        if status == "Traitement en cours" and status == "Cours non retenu":
            etat = 0
        else:
            etat += 1
        """
        cours = Cours.objects.get(id=cours_id)        
        #cours.etat = etat
        cours.status = status
        cours.content = content
        cours.st = 1
        cours.save()
        return redirect("cours/dcoursencours",id=id)
    else:
        composant = Composant.objects.get(id=composant_id)
        listcours = Cours.objects.filter(composant_id=composant_id, status="Traitement en cours").order_by("-id")
        context = {
                "composant":composant,
                "cours":listcours,
                "date":date,
                "parametre":parametre(),
                "countanswer":nbnew_answer(request),
                "count":nbnew_message(request),
                "users":new_message(request),
        }
        return render(request, "cours/dcoursencours.html", context)
    
def ajax_detail_document_encours(request, id):
    cours = Cours.objects.get(id=id)
    context = {
        "course": cours
    }
    return render(request, "ajax_detail_document_encours.html", context)

############################## Cours non publiés ####################################
@login_required(login_url='connection/login')
@allowed_users(allowed_roles=['admin'])
def coursnonpub(request):
    date = datetime.datetime.now()

    dataDiscipline = []
    disciplines = Cours.objects.values("discipline_id").filter(status="Cours non retenu").annotate(effectif=Count("discipline_id"))
    for data in disciplines:
        dic = {}
        discipline = Discipline.objects.get(id=data["discipline_id"])
        dic["id"] = data["discipline_id"]
        dic["libelle"] = discipline.libelle
        dic["effectif"] = data["effectif"]
        dataDiscipline.append(dic)

    context = {
            "disciplines":dataDiscipline,
            "date":date,
            "parametre":parametre(),
            "countanswer":nbnew_answer(request),
            "count":nbnew_message(request),
            "users":new_message(request),
    }
    return render(request, "cours/coursnonpub.html", context)

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=['admin'])
def detcoursnonpub(request,id):
    date = datetime.datetime.now()

    discipline_id = dechiffrer_param(str(id))
    discipline = Discipline.objects.get(id=discipline_id)

    dataComposant = []
    composants = Cours.objects.values("composant_id").filter(discipline_id=discipline_id, status="Cours non retenu").annotate(effectif=Count("composant_id"))
    for data in composants:
        dic = {}
        composant = Composant.objects.get(id=data["composant_id"])
        dic["id"] = data["composant_id"]
        dic["libelle"] = composant.libelle
        dic["effectif"] = data["effectif"]
        dataComposant.append(dic)

    context = {
            "discipline":discipline,
            "composants":dataComposant,
            "date":date,
            "parametre":parametre(),
            "countanswer":nbnew_answer(request),
            "count":nbnew_message(request),
            "users":new_message(request),
    }
    return render(request, "cours/detcoursnonpub.html", context)

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=['admin'])
def dcoursnonpub(request,id):
    date = datetime.datetime.now()
    composant_id = dechiffrer_param(str(id))
    composant = Composant.objects.get(id=composant_id)
    cours = Cours.objects.filter(composant_id=composant_id, status="Cours non retenu").order_by("-id")
    context = {
            "composant":composant,
            "cours":cours,
            "date":date,
            "parametre":parametre(),
            "countanswer":nbnew_answer(request),
            "count":nbnew_message(request),
            "users":new_message(request),
    }
    return render(request, "cours/dcoursnonpub.html", context)

def ajax_detail_document_nonpublie(request, id):
    cours = Cours.objects.get(id=id)
    context = {
        "course": cours
    }
    return render(request, "ajax_detail_document_nonpublie.html", context)

#============================ Panier =======================================
class addPanier(View):
    def get(self, request, id, *args, **kwargs):   
        try:
            panier = Panier.objects.get(user_id=request.user.id)
        except Exception as e:
            panier = None
        
        if panier == None:
            cours = Cours.objects.get(id=id)
            dic = {}
            tabCours = []
            tabCours.append(1)
            tabCours.append(cours.discipline.libelle)
            tabCours.append(cours.composant.libelle)
            tabCours.append(cours.title)
            tabCours.append(cours.comment)
            tabCours.append(cours.price)
            
            dic[id] = tabCours
            
            panier = Panier(user_id=request.user.id, cquantite=dic)
            panier.save()

            p = Panier.objects.get(user_id=request.user.id)
            cpanier = eval(p.cquantite)

            count = len(cpanier)
            
            context={
                "quantite":count
            }
            return render(request, "addPanier.html", context)
        else:
            cpanier = eval(panier.cquantite)
            tabkey = []
            for k in cpanier.items():
                tabkey.append(k)
            
            if id in tabkey:
                count = len(cpanier)
                context = {
                    "quantite":count
                }
                return render(request, "addPanier.html", context)
            else:
                cours = Cours.objects.get(id=id)

                tabCours = []
                tabCours.append(1)
                tabCours.append(cours.discipline.libelle)
                tabCours.append(cours.composant.libelle)
                tabCours.append(cours.title)
                tabCours.append(cours.comment)
                tabCours.append(cours.price)
                
                cpanier[id] = tabCours

                panier.cquantite = cpanier
                panier.save()

                p = Panier.objects.get(user_id=request.user.id)
                cpanier = eval(p.cquantite)

                count = 0
                for k in cpanier.items():
                    count += 1
                    
                context = {
                    "quantite":count
                }
                return render(request, "addPanier.html", context)
        
def panier(request):
    user = request.user
    qte_totale, prix_total, documents = order_summary(user)
    count = len(documents)

    context = {
            "count":count,
            "quantitetotale":qte_totale,
            "prixtotal":prix_total,
            "paniers":documents,
            "userpriorities":userPriority(),
            "parametre":parametre()
    }
    return render(request, "commande/panier.html", context)

def ajax_detail_cart(request, id):
    panier = Panier.objects.get(user_id=request.user.id)
    
    paniers = eval(panier.cquantite)
    
    dic = {}
    for key,value in paniers.items():
        if key == id:
            dic["id"] = key
            dic["quantite"] = value[0]
            dic["discipline"] = value[1]
            dic["composant"] = value[2]
            dic["title"] = value[3]
            dic["comment"] = value[4]
            dic["price"] = value[5]
        
    context = {
        "panier": dic
    }
    return render(request, "ajax_detail_cart.html", context)

def ajax_delete_cart(request, id):

    context = {
        "cartId": id
    }
    return render(request, "ajax_delete_cart.html", context)

@login_required(login_url='connection/login')
def del_panier(request, id):
    cart_id = dechiffrer_param(str(id))
    panier = Panier.objects.get(user_id=request.user.id)
    cquantite = eval(panier.cquantite)
    
    del cquantite[int(cart_id)]

    panier.cquantite = cquantite
    panier.save()
    return redirect("commande/panier")

@login_required(login_url='connection/login')
def md_paiement(request):
    user = request.user
    prix_total = order_summary(user)[1]

    #Mode de paiement
    modes = ModePaiement.objects.values("typepaiement").annotate(effectif=Count("typepaiement"))
    context = {
            "modes":modes,
            "prixtotal":prix_total,
            "userpriorities":userPriority(),
            "parametre":parametre()
    }

    return render(request, "commande/md_paiement.html", context)

# Paiement avec le compte paypal
def paiement_paypal(request):
    
    user = request.user
    qte_totale, prix_total, documents = order_summary(user)
    transaction_id = str(uuid.uuid4())
        
    host = request.get_host()
    
    # Informations de paiement
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': str(prix_total),
        'item_name': 'Nom du produit',
        'invoice': str(uuid.uuid4()),
        'currency_code': 'USD',
        'notify_url': f"http://{host}{reverse('paypal-ipn')}",
        'return_url': f"http://{host}{reverse('commande/payment_successful', kwargs={'transaction_id': transaction_id})}",
        'cancel_url': f"http://{host}{reverse('commande/echec')}",
    }
    
    # Créez le formulaire de paiement
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {
        "form": form,
        "qte_totale": qte_totale,
        "prix_total": prix_total,
        "documents": documents,
        "userpriorities":userPriority(),
        "parametre":parametre()
    }
    return render(request, 'commande/paiement_paypal.html', context)

@login_required(login_url='connection/login')
@transaction.atomic
def payment_successful(request, transaction_id):
    #On affiche la valeur du panier
    try:
        panier = Panier.objects.get(user_id=request.user.id)
    except Exception as e:
        panier = None
    
    if panier == None:
        return redirect("cours/cours")
    else:
        documents = eval(panier.cquantite)

    prixtotal = 0
    for k,v in documents.items():
        prixtotal += v[5]
    # Recupérer le mode du paiement
    mode = ModePaiement.objects.get(typepaiement = 'PayPal')
    # Enregistrer la commande 
    commande = Commande(
        total=prixtotal, 
        user_id=request.user.id, 
        ucours=documents, 
        modepaiement_id=mode.id, 
        transaction_id=transaction_id,
        validation="Commande validée"
    )
    commande.save()
    # Vider le panier
    panier.delete() 
    return redirect("commande/succ")

@login_required(login_url='connection/login')
@transaction.atomic
def paiement_card_bancaire(request):
    
    user = request.user
    qte_totale, amount, documents = order_summary(user) 
    transaction_id = str(uuid.uuid4())
    
    if request.method == "POST":
        try:
            # Crée une session de paiement
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'eur',
                        'product_data': {
                            'name': 'Produit Exemple',
                        },
                        'unit_amount': 100*amount,  # Montant en centimes
                    },
                    'quantity': qte_totale,
                }],
                mode = 'payment',
                success_url = f"{request.build_absolute_uri(reverse('commande/payment_successful', kwargs={'transaction_id': transaction_id}))}",
                cancel_url = f"{request.build_absolute_uri(reverse('commande/echec'))}"
            )
            return JsonResponse({
                'id': checkout_session.id
            })
        except Exception as e:
            return JsonResponse({'error': str(e)})
        
    context = {
        "qte_total":qte_totale,
        "prix_total": amount,
        "documents":documents,
        "stripe_publishable_key": settings.STRIPE_PUBLISHABLE_KEY,
        "userpriorities":userPriority(),
        "parametre":parametre()
    }
    return render(request, 'commande/paiement_card_bancaire.html', context)

# Num Card test: 4242 4242 4242 4242

# Création de User API
def user_api(unique_ref, subscription_key):
    url = "https://sandbox.momodeveloper.mtn.com/v1_0/apiuser"
    headers = {
        'X-Reference-Id': unique_ref,  # ID unique de la transaction
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Content-Type': 'application/json'
    }
    data = {
        "providerCallbackHost": "string"
    }
    # Elle retourne 201 si l'opération a reussi 
    response = requests.post(url, data=json.dumps(data), headers=headers)

    return response.status_code

def generate_momo_api_key(unique_ref, subscription_key):
    url = f"https://sandbox.momodeveloper.mtn.com/v1_0/apiuser/{unique_ref}/apikey"
    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Content-Type': 'application/json'
    }
    body = {"providerCallbackHost": "string"}

    response = requests.post(url, data=json.dumps(body), headers=headers)

    if response.status_code == 201:
        user_key_tojson = response.json()
        apikey = user_key_tojson['apiKey']
        print("Clé API générée avec succès:", apikey)
        return apikey
    else:
        print("Erreur lors de la génération de la clé API:", response.json())
        return None

@login_required(login_url='connection/login')
@transaction.atomic
def paiement_mobile(request):
    
    unique_ref = str(uuid.uuid4())
    subscription_key = settings.MTN_PRIMARY_KEY
    user = request.user
    qte_totale, prix_total, documents = order_summary(user)
    
    if request.method == "POST":
            phone_number = bleach.clean(request.POST["phone"].strip())
            
            user_api(unique_ref, subscription_key)
            
            apikey = generate_momo_api_key(unique_ref, subscription_key)
                              
            url = "https://sandbox.momodeveloper.mtn.com/collection/token/"
            hdr = {'Ocp-Apim-Subscription-Key': subscription_key}
            r = requests.post(url, headers=hdr, auth=(unique_ref, apikey))
            if r.status_code == 200:
                json_content = r.json()
                access_token = json_content['access_token']
                token_type = json_content['token_type']
                expires_in = json_content['expires_in']
                print('access_token : ', access_token),
                print('token_type :', token_type),
                print('expires_in :', expires_in)
                
                # Transaction
                
                headers = {
                    'Authorization': f"Bearer {access_token}",
                    'X-Reference-Id': unique_ref,  # Utilisez un identifiant unique pour chaque requête
                    'X-Target-Environment': 'sandbox',  # Changez en 'production' si vous passez en production
                    'Ocp-Apim-Subscription-Key': subscription_key,
                    'Content-Type': 'application/json'
                }
                body = {
                    "amount": prix_total,
                    "currency": "EUR",
                    "externalId": "123456789",
                    "payer": {
                        "partyIdType": "MSISDN",
                        "partyId": phone_number
                    },
                    "payerMessage": "Paiement pour votre commande",
                    "payeeNote": "Merci pour votre paiement"
                }

                ul = 'https://sandbox.momodeveloper.mtn.com/collection/v1_0/requesttopay'
                response = requests.post(ul, data=json.dumps(body), headers=headers)
                
                if response.status_code == 202:
                    transaction_id = unique_ref  # Utilisez `unique_ref` pour suivre le statut
                    return redirect("commande/payment_successful", transaction_id=transaction_id)
                else:
                    #print(response.json())  # Affiche le message d'erreur détaillé
                    return redirect("commande/echec")
                    #return JsonResponse({"status": "error", "message": "Transaction échouée"})
            else:
                #print(response.json())  # Affiche le message d'erreur détaillé
                return redirect("commande/echec")
                #return JsonResponse({"status": "error", "message": "Transaction échouée"})

    
    modes=ModePaiement.objects.filter(typepaiement="Mobile")
    context={
            "modes":modes,
            "prix_total":prix_total,
            "qte_total": qte_totale,
            "documents": documents,
            "userpriorities":userPriority(),
            "parametre":parametre()
    }
    return render(request, "commande/paiement_mobile.html", context)

@login_required(login_url='connection/login')
@transaction.atomic
def validate_order(request):
    user_id = request.user.id
    unique_ref = str(uuid.uuid4())
    #On affiche la valeur du panier
    try:
        panier=Panier.objects.get(user_id=user_id)
    except Exception as e:
        panier=None
    
    if panier == None:
        return redirect("cours/cours")
    else:
        cquantite = eval(panier.cquantite)

    prix_total = 0
    for key,value in cquantite.items():
        prix_total += value[5]
    #On recupération du mode
    mode = ModePaiement.objects.get(typepaiement='Mobile')
    commande = Commande(total=prix_total, user_id=user_id, ucours=cquantite, modepaiement_id=mode.id, transaction_id=unique_ref)
    commande.save()
    # Vider le panier
    panier.delete()  
    return redirect("commande/success")

@login_required(login_url='connection/login')
@transaction.atomic
def success(request):
    date = datetime.datetime.now()
    # Ajouter 3 jours à cette date
    date_limit = date + timedelta(days=3)
    #On recupère des documents
    subject = "Documents"
    template = "email/emailcmd.html"
    receivers = [request.user.email]
    #On recupère le membre qui a effectué l'achat
    user = User.objects.get(id=request.user.id)            
    ctxt = {
        "user": user,
        'date': date,
        'date_limit': date_limit,
        'parametre': parametre(),
        "domain":get_current_site(request).domain,
    }

    send_email_with_html_body(
        subjet=subject,
        receivers=receivers,
        template=template,
        context=ctxt
    )
    
    context = {
        "date":date,
        "date_limit": date_limit,
        "userpriorities": userPriority(),
        "parametre": parametre()
    }
    return render(request, "commande/success.html", context)

@login_required(login_url='connection/login')
@transaction.atomic
def succ(request):
    date = datetime.datetime.now()
    
    # Recuperer les documents
    tabCours = []
    commande = Commande.objects.filter(user_id=request.user.id).order_by("-id")[0]
    doc = eval(commande.ucours)
    for k,v in doc.items():
        cours = Cours.objects.get(id=k)
        tabCours.append(cours)
    
    subject = "Documents"
    template = "email/emaildocument.html"
    receivers = [request.user.email]
    # Recuperer le membre qui a effectué l'achat
    user = User.objects.get(id=request.user.id)            
    ctxt = {
        "user":user,
        "count":len(tabCours),
        "cours":tabCours,
        'date': date,
        'parametre': parametre(),
        "domain":get_current_site(request).domain,
    }

    send_email_with_html_body(
        subjet=subject,
        receivers=receivers,
        template=template,
        context=ctxt
    )
    
    context = {
        "commande":commande,
        "cours":tabCours,
        "userpriorities":userPriority(),
        "parametre":parametre()
    }
    return render(request, "commande/succ.html", context)

@login_required(login_url='connection/login')
def echec(request):
    context={
        "parametre":parametre()
    }
    return render(request, "commande/echec.html", context)

@login_required(login_url='connection/login')
def commandes(request):
    date = datetime.datetime.now()
    commandes = []
    cmds = Commande.objects.filter(status=0)
    for commande in cmds:
        if commande.modepaiement.typepaiement == "Mobile":
            commandes.append(commande)

    for commande in commandes:
        commande.status = 1
        commande.save()
    
    commdes = []
    comdes = Commande.objects.filter(status=1, validation__in=['Commande en cours de traitement','Commande validée']).order_by("-id")
    for commande in comdes:
        if commande.modepaiement.typepaiement == "Mobile":
            commdes.append(commande)
    context = {
        "commandes":commdes,
        "date":date,
        "parametre":parametre(),
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request),
    }
    return render(request, "commande/commandes.html", context)

@login_required(login_url='connection/login')
def achats(request):
    date = datetime.datetime.now()
    commandes = []
    cmds = Commande.objects.filter(status=0)
    for commande in cmds:
        if commande.modepaiement.typepaiement in ["PayPal", "Carte bancaire"]:
            commandes.append(commande)

    for commande in commandes:
        commande.status = 1
        commande.save()
    
    commdes = []
    comdes = Commande.objects.filter(status=1).order_by("-id")
    for commande in comdes:
        if commande.modepaiement.typepaiement in ["PayPal", "Carte bancaire"]:
            commdes.append(commande)
        else:
            if commande.validation == "Commande validée":
               commdes.append(commande)

    context = {
        "commandes":commdes,
        "date":date,
        "parametre":parametre(),
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request),
    }
    return render(request, "commande/achats.html", context)

@login_required(login_url='connection/login')
def delachat(request, id):
    try:
        achat = Commande.objects.get(id=id)
    except:
        achat = None
        
    if achat:
        achat.delete()
    return redirect("commande/achats")

@login_required(login_url='connection/login')
def detachat(request, id):
    date = datetime.datetime.now()
    # Résumer d'un achat
    qte_totale, prix_total, commande, achats = purchase_summary(id)

    context = {
        "commande":commande,
        "achats":achats,
        "total":prix_total,
        "qtetotal":qte_totale,
        "date":date,
        "parametre":parametre(),
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request),
    }
    return render(request, "commande/detachat.html", context)

@login_required(login_url='connection/login')
def det_cmd(request, id):
    date = datetime.datetime.now()
    # Résumer d'un achat
    qte_totale, prix_total, commande, achats = purchase_summary(id)

    validation_status = ["Commande en cours de traitement", "Commande validée", "Commande non validée"]
    validations = []
    for validation in validation_status:
        if validation != commande.validation:
            validations.append(validation)
    context = {
        "validations": validations,
        "commande": commande,
        "achats": achats,
        "total": prix_total,
        "qtetotal": qte_totale,
        "date": date,
        "parametre": parametre(),
        "countanswer": nbnew_answer(request),
        "count": nbnew_message(request),
        "users": new_message(request),
    }
    return render(request, "commande/det-cmd.html", context)

@login_required(login_url='connection/login')
def doc_purchased(request):
    date=datetime.datetime.now()
    modes=ModePaiement.objects.all()
    tabAchats=[]
    for mode in modes:
        if mode.typepaiement == "Mobile":
            commandes = Commande.objects.filter(user_id=request.user.id,  modepaiement_id=mode.id, validation="Commande validée")
            for commande in commandes:
                doc = eval(commande.ucours)
                dic = {}
                dic["id"] = commande.id
                dic["total"] = commande.total
                dic["datecommande"] = commande.datecommande
                tabcours = []
                for k,c in doc.items():
                    cours = Cours.objects.get(id=k)
                    dict = {}
                    dict["qte"] = c[0]
                    dict["discipline"] = c[1]
                    dict["composant"] = c[2]
                    dict["title"] = c[3]
                    dict["comment"] = c[4]
                    dict["price"] = c[5]
                    dict["file"] = cours.file

                    tabcours.append(dict)
                dic["cours"] = tabcours
                tabAchats.append(dic)
        else:
            commandes = Commande.objects.filter(user_id=request.user.id, modepaiement_id=mode.id,)
            for commande in commandes:
                doc = eval(commande.ucours)
                dic = {}
                dic["id"] = commande.id
                dic["total"] = commande.total
                dic["datecommande"] = commande.datecommande
                tabcours=[]
                for k,c in doc.items():
                    cours = Cours.objects.get(id=k)
                    dict = {}
                    dict["qte"] = c[0]
                    dict["discipline"] = c[1]
                    dict["composant"] = c[2]
                    dict["title"] = c[3]
                    dict["comment"] = c[4]
                    dict["price"] = c[5]
                    dict["file"] = cours.file

                    tabcours.append(dict)
                dic["cours"] = tabcours
                tabAchats.append(dic)
    context = {
        "date":date,
        "parametre":parametre(),
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request),
        "achats":tabAchats
    }
    return render(request, "commande/doc-pur.html", context)

@login_required(login_url='connection/login')
def doc_cmd(request):
    date = datetime.datetime.now()
    modes = ModePaiement.objects.all()
    tabAchats = []
    for mode in modes:
        if mode.typepaiement == "Mobile":
            commandes = Commande.objects.filter(user_id=request.user.id, modepaiement_id=mode.id, validation__in=['Commande en cours de traitement','Commande non validée'])
            for commande in commandes:
                doc = eval(commande.ucours)
                dic = {}
                dic["id"] = commande.id
                dic["total"] = commande.total
                dic["datecommande"] = commande.datecommande
                dic["validation"] = commande.validation
                dic["commentaire"] = commande.comment
                tabcours = []
                for k,c in doc.items():
                    cours = Cours.objects.get(id=k)
                    dict = {}
                    dict["qte"] = c[0]
                    dict["discipline"] = c[1]
                    dict["composant"] = c[2]
                    dict["title"] = c[3]
                    dict["comment"] = c[4]
                    dict["price"] = c[5]
                    dict["file"] = cours.file
                    tabcours.append(dict)
                dic["cours"] = tabcours
                tabAchats.append(dic)
    context = {
        "date":date,
        "parametre":parametre(),
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request),
        "achats":tabAchats
    }
    return render(request, "commande/doc-cmd.html", context)

# Supprimer la dupplication de date
def delete_duplicated_date_user(cours):
    orders = []
    for cour in cours:
        commandes = Commande.objects.filter(validation="Commande validée")
        # Selectionner uniquement les commandes des documents de l'utilisateur
        for commande in commandes:
            documents = eval(commande.ucours)
            for key, value in documents.items():
                if key == cour.id:
                    orders.append(commande)
                
    liste_dates = []
    listes = []
    for c in orders:
        date = str(c.datecommande.month)+"-"+str(c.datecommande.year)
        if date  not in liste_dates:
            liste_dates.append(date)
            listes.append(c.datecommande)
            
    return listes

@login_required(login_url='connection/login')
def my_doc_purchased(request):
    date = datetime.datetime.now()
    
    tabAchats = []
    #On recupère tous les documents du mmenbre
    cours = Cours.objects.filter(user_id=request.user.id)

    for c in cours:
        #On recupère tous les achats
        commandes = Commande.objects.filter(statusachat=0)
        for commande in commandes:
            doc = eval(commande.ucours)
            for k,v in doc.items():
                #On selectionne uniquement les documents du membre qui ont été acheté 
                if k == c.id:
                    #Changement de status
                    commande.statusachat = 1
                    commande.save()

    for c in cours:
        #On recupère uniquement les documents achetés
        tabCommandes = []
        modes = ModePaiement.objects.all()
        for mode in modes:
            if mode.typepaiement == "Mobile":
                comdes = Commande.objects.filter(modepaiement_id=mode.id, validation="Commande validée")
                for cmd in comdes:
                    tabCommandes.append(cmd)
            else:
                comdes = Commande.objects.filter(modepaiement_id=mode.id)
                for cmd in comdes:
                    tabCommandes.append(cmd)

        dic = {}
        tab = []
        count = 0
        for commande in tabCommandes:
            doc = eval(commande.ucours)
            for k,v in doc.items():
                #On selectionne uniquement les documents du membre qui ont été acheté 
                if k == c.id:
                    count += 1
                    dict = {}
                    dict["id"] = commande.id
                    dict["date"] = commande.datecommande
                    dict["user"] = commande.user
                    dict["qte"] = v[0]
                    dict["discipline"] = v[1]
                    dict["composant"] = v[2]
                    dict["title"] = v[3]
                    dict["comment"] = v[4]
                    dict["price"] = v[5]
                    dict["file"] = c.file
                    tab.append(dict)
            
            if len(tab) > 0:
                dic[c.id] = tab
        if len(dic) > 0:
            tabAchats.append(dic)
    # Suppression des dates duppliquées       
    list_date = delete_duplicated_date_user(cours)
    
    context = {
        "liste_dates" :list_date,
        "date":date,
        "parametre":parametre(),
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request),
        "achats":tabAchats
    }
    return render(request, "commande/my-docpur.html", context)

# Supprimer la dupplication de date
def delete_duplicated_date():
    commandes = Commande.objects.filter(validation="Commande validée")
    liste_dates = []
    listes = []
    for c in commandes:
        date = str(c.datecommande.month)+"-"+str(c.datecommande.year)
        if date  not in liste_dates:
            liste_dates.append(date)
            listes.append(c.datecommande)
            
    return listes


@login_required(login_url='connection/login')
def all_doc_purchased(request):
    date = datetime.datetime.now()
    
    tabAchats = []
    #On recupère tous les documents du mmenbre
    cours = Cours.objects.all()

    for c in cours:
        #On recupère tous les achats
        commandes = Commande.objects.filter(statusachat=0)
        for commande in commandes:
            doc = eval(commande.ucours)
            for k,v in doc.items():
                #On selectionne uniquement les documents du membre qui ont été acheté 
                if k == c.id:
                    #Changement de status
                    commande.statusachat = 1
                    commande.save()
                    

    for c in cours:
        #On recupère uniquement les documents achetés
        tabCommandes = []
        modes = ModePaiement.objects.all()
        for mode in modes:
            if mode.typepaiement == "Mobile":
                comdes = Commande.objects.filter(modepaiement_id=mode.id, validation="Commande validée")
                for cmd in comdes:
                    tabCommandes.append(cmd)
            else:
                comdes = Commande.objects.filter(modepaiement_id=mode.id)
                for cmd in comdes:
                    tabCommandes.append(cmd)
        
        dic = {}
        tab = []
        count = 0
        for commande in tabCommandes:
            doc = eval(commande.ucours)
            for k,v in doc.items():
                #On selectionne uniquement les documents du membre qui ont été acheté 
                if k == c.id:
                    count += 1
                    dict = {}
                    dict["id"] = commande.id
                    dict["date"] = commande.datecommande
                    dict["user"] = commande.user
                    dict["qte"] = v[0]
                    dict["discipline"] = v[1]
                    dict["composant"] = v[2]
                    dict["title"] = v[3]
                    dict["comment"] = v[4]
                    dict["price"] = v[5]
                    dict["file"] = c.file
                    tab.append(dict)
            
            if len(tab) > 0:
                dic[c.id] = tab
        if len(dic) > 0:
            tabAchats.append(dic)
            
    # Suppression des dates duppliquées       
    list_date = delete_duplicated_date()
    
    context = {
        "liste_dates" :list_date,
        "date" :date,
        "parametre" :parametre(),
        "countanswer" :nbnew_answer(request),
        "count" :nbnew_message(request),
        "users" :new_message(request),
        "achats" :tabAchats
    }
    return render(request, "commande/all-docpur.html", context)

class purchase_month_year(View):
    def get(self, request, month_year, *args, **kwargs):
        
        m_y = month_year.split("-")
        tabAchats = []
        #On recupère tous les documents du mmenbre
        cours = Cours.objects.all()

        for c in cours:
            #On recupère tous les achats
            commandes = Commande.objects.filter(statusachat=0)
            for commande in commandes:
                doc = eval(commande.ucours)
                for k,v in doc.items():
                    #On selectionne uniquement les documents du membre qui ont été acheté 
                    if k == c.id:
                        #Changement de status
                        commande.statusachat = 1
                        commande.save()

        for c in cours:
            #On recupère uniquement les documents achetés
            tabCommandes = []
            modes = ModePaiement.objects.all()
            for mode in modes:
                if month_year !="022024":
                    if mode.typepaiement == "Mobile":
                        comdes = Commande.objects.filter(modepaiement_id=mode.id, validation="Commande validée", datecommande__month=m_y[0], datecommande__year=m_y[1])
                        for cmd in comdes:
                            tabCommandes.append(cmd)
                    else:
                        comdes = Commande.objects.filter(modepaiement_id=mode.id, datecommande__month=m_y[0], datecommande__year=m_y[1])
                        for cmd in comdes:
                            tabCommandes.append(cmd)
                else:
                    if mode.typepaiement == "Mobile":
                        comdes = Commande.objects.filter(modepaiement_id=mode.id, validation="Commande validée")
                        for cmd in comdes:
                            tabCommandes.append(cmd)
                    else:
                        comdes = Commande.objects.filter(modepaiement_id=mode.id)
                        for cmd in comdes:
                            tabCommandes.append(cmd)

            dic = {}
            tab = []
            count = 0
            for commande in tabCommandes:
                doc = eval(commande.ucours)
                for k,v in doc.items():
                    #On selectionne uniquement les documents du membre qui ont été acheté 
                    if k == c.id:
                        count += 1
                        dict = {}
                        dict["id"] = commande.id
                        dict["date"] = commande.datecommande
                        dict["qte"] = v[0]
                        dict["discipline"] = v[1]
                        dict["composant"] = v[2]
                        dict["title"] = v[3]
                        dict["comment"] = v[4]
                        dict["price"] = v[5]
                        dict["file"] = c.file
                        tab.append(dict)
                
                if len(tab) > 0:
                    dic[c.id] = tab
            if len(dic.keys()) > 0:
                tabAchats.append(dic)
        
        context = {
            "achats":tabAchats
        }
        return render(request, "purchase_month_year.html", context)
    
class purchase_month_year_user(View):
    def get(self, request, month_year_user, *args, **kwargs):
        
        m_y = month_year_user.split("-")
        tabAchats = []
        #On recupère tous les documents du mmenbre
        cours = Cours.objects.filter(user_id=request.user.id)

        for c in cours:
            #On recupère tous les achats
            commandes = Commande.objects.filter(statusachat=0)
            for commande in commandes:
                doc = eval(commande.ucours)
                for k,v in doc.items():
                    #On selectionne uniquement les documents du membre qui ont été acheté 
                    if k == c.id:
                        #Changement de status
                        commande.statusachat = 1
                        commande.save()

        for c in cours:
            #On recupère uniquement les documents achetés
            tabCommandes = []
            modes = ModePaiement.objects.all()
            for mode in modes:
                if month_year_user !="022024":
                    if mode.typepaiement == "Mobile":
                        comdes = Commande.objects.filter(modepaiement_id=mode.id, validation="Commande validée", datecommande__month=m_y[0], datecommande__year=m_y[1])
                        for cmd in comdes:
                            tabCommandes.append(cmd)
                    else:
                        comdes = Commande.objects.filter(modepaiement_id=mode.id, datecommande__month=m_y[0], datecommande__year=m_y[1])
                        for cmd in comdes:
                            tabCommandes.append(cmd)
                else:
                    if mode.typepaiement == "Mobile":
                        comdes = Commande.objects.filter(modepaiement_id=mode.id, validation="Commande validée")
                        for cmd in comdes:
                            tabCommandes.append(cmd)
                    else:
                        comdes = Commande.objects.filter(modepaiement_id=mode.id)
                        for cmd in comdes:
                            tabCommandes.append(cmd)

            dic = {}
            tab = []
            count = 0
            for commande in tabCommandes:
                doc = eval(commande.ucours)
                for k,v in doc.items():
                    #On selectionne uniquement les documents du membre qui ont été acheté 
                    if k == c.id:
                        count += 1
                        dict = {}
                        dict["id"] = commande.id
                        dict["date"] = commande.datecommande
                        dict["qte"] = v[0]
                        dict["discipline"] = v[1]
                        dict["composant"] = v[2]
                        dict["title"] = v[3]
                        dict["comment"] = v[4]
                        dict["price"] = v[5]
                        dict["file"] = c.file
                        tab.append(dict)
                
                if len(tab) > 0:
                    dic[c.id] = tab
            if len(dic.keys()) > 0:
                tabAchats.append(dic)
        
        context = {
            "achats":tabAchats
        }
        return render(request, "purchase_month_year_user.html", context)

class fetchdoc(View):
    def get(self, request, id, *args, **kwargs):
        #On compte le nombre de cours
        countcoursencours = Cours.objects.filter(discipline_id=id,status="Traitement en cours").count()
        countcourspublie = Cours.objects.filter(discipline_id=id,status="Cours publié").count()
        countcoursnonpublie = Cours.objects.filter(discipline_id=id,status="Cours non retenu").count()
        total = Cours.objects.filter(discipline_id=id).count()
        discipline = Discipline.objects.get(id=id)
        context = {
            "discipline":discipline,
            "total":total,
            "countcoursencours":countcoursencours,
            "countcourspublie":countcourspublie,
            "countcoursnonpublie":countcoursnonpublie
        }
        return render(request, "fetchdoc.html", context)
    
class fetchdoccmp(View):
    def get(self, request, id, *args, **kwargs):

        #On compte le nombre de cours
        countcoursencours = Cours.objects.filter(composant_id=id,status="Traitement en cours").count()
        countcourspublie = Cours.objects.filter(composant_id=id,status="Cours publié").count()
        countcoursnonpublie = Cours.objects.filter(composant_id=id,status="Cours non retenu").count()
        total = Cours.objects.filter(composant_id=id).count()
        composant = Composant.objects.get(id=id)
        context = {
            "composant":composant,
            "total":total,
            "countcoursencours":countcoursencours,
            "countcourspublie":countcourspublie,
            "countcoursnonpublie":countcoursnonpublie
        }
        return render(request, "fetchdoccmp.html", context)

@login_required(login_url='connection/login')
def facture(request,id):
    commande = Commande.objects.get(id=id)
    panier = eval(commande.ucours)
    prixtotal = 0
    quantitetotal = 0
    tabAchat = []
    for k,v in panier.items():
        dic = {}
        dic["id"] = k
        dic["quantite"] = v[0]
        dic["discipline"] = v[1]
        dic["composant"] = v[2]
        dic["title"] = v[3]
        dic["comment"] = v[4]
        dic["price"] = v[5]
        tabAchat.append(dic)

        quantitetotal += v[0]
        prixtotal += v[5]
        
    # Chemin vers votre image
    image_path = parametre().logo
    base64_string = ""
    if image_path:
        # Lire l'image en mode binaire et encoder en Base64
        base64_string = base64.b64encode(image_path.read()).decode('utf-8')

    context = {
        "base64_image": base64_string,
        "commande": commande,
        "achats": tabAchat,
        "total": prixtotal,
        "qtetotal": quantitetotal,
        "parametre": parametre(),
        "domain": get_current_site(request).domain,
    }
    template = get_template("commande/facture.html")
    html = template.render(context)
    options = {
        'page-size': 'Letter',
        'encoding': "UTF-8",
    }

    pdf = pdfkit.from_string(html, False, options)
    reponse = HttpResponse(pdf, content_type='application/pdf')
    reponse['Content-Disposition'] = f"attachment; filename=facture_{ parametre().appname }_{commande.id}.pdf"
    return reponse


#=================== Gestion du mode de paiement ======================
@login_required(login_url='connection/login')
@allowed_users(allowed_roles=['admin'])
def mode_paiement(request):
    date = datetime.datetime.now()

    modes = ModePaiement.objects.all()
    context = {
        "modes":modes,
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request),
        "parametre":parametre(),
        "date":date
    }
    return render(request, "mode-paiement/mode-paye.html", context)

@login_required(login_url='connection/login')
@csrf_exempt
@allowed_users(allowed_roles=['admin'])
def add_mode(request):
    date = datetime.datetime.now()

    if request.method == "POST":
        typepaiement=request.POST["typepaiement"]
        if typepaiement == "Mobile":
            numero = bleach.clean(request.POST["numero"].strip())
            libelle = bleach.clean(request.POST["libelle"].strip())
            # Verifier l'existence du numéro et du libellé
            query = ModePaiement.objects.filter(typepaiement=typepaiement)
            if query.exists():
                return JsonResponse({
                    "status": "error",
                    "message": "Ce mode de paiement existe déjà."})
            else:
                mode = ModePaiement(typepaiement=typepaiement,libelle=libelle,numero=numero)
                count0 = ModePaiement.objects.all().count()
                mode.save()
                count1 = ModePaiement.objects.all().count()
                if count0 < count1:
                    return JsonResponse({
                        "status": "success",
                        "message": "Mode de paiement enregistré avec succès."})
                else:
                    return JsonResponse({
                        "status": "error",
                        "message": "L'insertion a échouée."})
        else:
            query = ModePaiement.objects.filter(typepaiement=typepaiement)
            # Verifier l'existence du type de paiement
            if query.exists():
                return JsonResponse({
                    "status": "error",
                    "message": "Ce mode de paiement existe déjà."})
            else:
                count0 = ModePaiement.objects.all().count()
                mode = ModePaiement(typepaiement=typepaiement)
                mode.save()
                count1 = ModePaiement.objects.all().count()
                if count0 < count1:
                    return JsonResponse({
                        "status": "success",
                        "message": "Mode de paiement enregistré avec succès."})
                else:
                    return JsonResponse({'status':1})
    context={
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request),
        "parametre":parametre(),
        "date":date
    }
    return render(request, "mode-paiement/add-mode.html", context)

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=['admin'])
def edit_mode(request,id):
    date = datetime.datetime.now()
    mode_id = dechiffrer_param(str(id))
    mode = ModePaiement.objects.get(id=mode_id)
    context = {
            "mode":mode,
            "countanswer":nbnew_answer(request),
            "count":nbnew_message(request),
            "users":new_message(request),
            "parametre":parametre(),
            "date":date
    }
    return render(request, "mode-paiement/edit-mode.html", context)

@login_required(login_url='connection/login')
@csrf_exempt
def edit_mod(request):
    if request.method=="POST":
        id = int(request.POST["id"])
        try:
            mode = ModePaiement.objects.get(id=id)
        except:
            mode = None

        if mode == None:
            return JsonResponse({
                    "status": "error",
                    "message": "Identifiant inexistant."})
        else:
            typepaiement = request.POST["typepaiement"]
            if typepaiement == "Mobile":
                libelle = bleach.clean(request.POST["libelle"].strip())
                numero = bleach.clean(request.POST["numero"].strip())
                #On exclut le mode de paiement que l'on veut modifier et on recupère les autres
                modes = ModePaiement.objects.exclude(id=id)
                tabTypePaiement = []
                for mod in modes:
                    tabTypePaiement.append(mod.typepaiement)
                    
                if typepaiement in tabTypePaiement:
                    return JsonResponse({
                        "status": "error",
                        "message": "Ce mode de paiement existe déjà."})
                else:
                    mode.typepaiement=typepaiement
                    mode.libelle = libelle
                    mode.numero = numero
                    mode.save()
                    return JsonResponse({
                        "status": "success",
                        "message": "Mode de paiement modifié avec succès."})
            else:
                #On exclut le mode de paiement que l'on veut modifier et on recupère les autres
                modes = ModePaiement.objects.exclude(id=id)
                tabTypePaiement = []
                for mod in modes:
                    tabTypePaiement.append(mod.typepaiement)

                if typepaiement in tabTypePaiement:
                    return JsonResponse({
                        "status": "error",
                        "message": "Ce mode de paiement existe déjà."})
                else:
                    mode.typepaiement=typepaiement
                    mode.libelle = ""
                    mode.numero = ""
                    mode.save()
                    return JsonResponse({
                        "status": "success",
                        "message": "Mode de paiement modifié avec succès."})
                
def ajax_delete_mode_payment(request, id):
    mode = ModePaiement.objects.get(id=id)
    context = {
        "mode": mode
    }
    return render(request, "ajax_delete_mode_payment.html", context)

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=['admin'])
def del_mode(request,id):
    try:
        mode_id  = dechiffrer_param(str(id))
        mode = ModePaiement.objects.get(id=mode_id)
    except:
        mode = None
        
    if mode:
        mode.delete()
    return redirect("mode-paiement/mode-paye")

class ajaxmode(View):
    def get(self, request, id, *args, **kwargs):

        typepaiement=id
        context = {
            "typepaiement":typepaiement
        }
        return render(request, "ajaxMode.html", context)

def generate_email(commande):
    date = datetime.datetime.now()
    tabCours = []
    doc = eval(commande.ucours)
    for k,v in doc.items():
        # Recuperer le cours
        cours = Cours.objects.get(id=k)
        tabCours.append(cours)
    
    subject = "Documents"
    template = "email/emaildocument.html"
    receivers = [commande.user.email]
    #On recupère le membre qui a effectué l'achat
    usr = User.objects.get(id=id)            
    ctxt = {
        "user":commande.user,
        "count":len(tabCours),
        "cours":tabCours,
        'date': date,
        'parametre': parametre()
    }

    send_email_with_html_body(
        subjet=subject,
        receivers=receivers,
        template=template,
        context=ctxt
    )

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=['admin'])
@transaction.atomic
def validate(request):
    date = datetime.datetime.now()
    if request.method == "POST":
        id = int(request.POST["id"])
        try:
            commande = Commande.objects.get(id=id)
        except:
            commande = None

        if commande:
            validation = request.POST["validation"]
            comment = bleach.clean(request.POST["comment"].strip())
            if validation == "Commande en cours de traitement":
                commande.validation = validation
                com=""
                if comment == "":
                    com = com + "Nous examinons votre commande et reviendrons vers vous dans les plus brefs délais."
                else:
                    com = comment
                commande.comment = com
                commande.save()
                return redirect("commande/det-cmd", id=id)
            elif validation == "Commande validée":
                commande.validation = validation
                com = ""
                if comment == "":
                    com = com + "Votre commande a été validée, vous pouvez désormais télécharger les documents."
                else:
                    com = comment
                commande.comment = com
                commande.save()
                # Envoyer l'e-mail au client
                tabCours = []
                doc = eval(commande.ucours)
                for k,v in doc.items():
                    # Recuperer le cours
                    cours = Cours.objects.get(id=k)
                    tabCours.append(cours)
                
                subject = "Documents"
                template = "email/emaildocument.html"
                receivers = [commande.user.email]
                #On recupère le membre qui a effectué l'achat
                ctxt = {
                    "user":commande.user,
                    "count":len(tabCours),
                    "cours":tabCours,
                    'date': date,
                    'parametre': parametre()
                }

                send_email_with_html_body(
                    subjet=subject,
                    receivers=receivers,
                    template=template,
                    context=ctxt
                )
                return redirect("commande/det-cmd", id=id)
            else:
                commande.validation = validation
                com = ""
                if comment == "":
                    com = com + "Après examen de votre commande, nous regrettons de vous informer qu'elle n'a pas pu être validée."
                else:
                    com = comment
                commande.comment = com
                commande.save()
                return redirect("commande/det-cmd", id=id)
                   
#Configurer une vue pour vérifier l'état du paiement MTN fournit une API pour vérifier l'état d'un paiement. Crée une vue pour interroger l'API et mettre à jour l'état du paiement.
def check_payment_status(transaction_id, access_token):
    url = f"https://sandbox.momodeveloper.mtn.com/collection/v2_0/payment/{transaction_id}/"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data.get("status")
    return "unknown"

def update_payment_status(request, transaction_id):
    status = check_payment_status(transaction_id)

    payment = Commande.objects.get(transaction_id=transaction_id)
    payment.status = status
    payment.save()

    return JsonResponse({"transaction_id": transaction_id, "status": status})
        
class level(View):
    def get(self, request, id, *args, **kwargs):
        context={"niveau":id}
        return render(request, "niveau.html", context)
