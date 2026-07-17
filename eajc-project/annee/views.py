# Importation des modeles standards
import datetime
import bleach
# Importation des modeles tiers
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Importation des models locaux
from eab.views import nbnew_answer, nbnew_message, new_message, parametre
from .models import*
from app_auth.decorator import*
from eajc.utils.crypto import dechiffrer_param

#=================== Gestion de l'année ======================
@login_required(login_url='connection/login')
@allowed_users(allowed_roles=['admin'])
def annees(request):
    date = datetime.datetime.now()

    annees = Annee.objects.all()
    context = {
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request),
        "annees":annees,
        "parametre":parametre(),
        "date":date
    }
    return render(request, "annees.html", context)

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=['admin'])
@csrf_exempt
def add_annee(request):
    date = datetime.datetime.now()

    if request.method == "POST":
        # Se proteger de l'attaque XSS(Injection du code javascript)
        libelle = bleach.clean(request.POST["libelle"].strip())
        query = Annee.objects.filter(libelle=libelle)
        # Verifier l'existence de l'année
        if query.exists():
            return JsonResponse({
                "status": "error",
                "message": "Cette année existe déjà."})
        else:
            annee = Annee(libelle=libelle)
            # Nombre d'années avant l'ajout
            count0 = Annee.objects.all().count()
            annee.save()
            # Nombre d'années après l'ajout
            count1 = Annee.objects.all().count()
            # On verifie si l'insertion a eu lieu ou pas.
            if count0 < count1:
                return JsonResponse({
                    "status": "success",
                    "message": "Année enregistrée avec succès."})
            else:
               return JsonResponse({
                    "status": "error",
                    "message": "L'insertion a échouée."})
    context = {
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request),
        "parametre":parametre(),
        "date":date
    }
    return render(request, "add_annee.html", context)

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=['admin'])
@csrf_exempt
def edit_annee(request, id):
    date = datetime.datetime.now()
    
    annee_id = int(dechiffrer_param(str(id)))
    
    annee = Annee.objects.get(id=annee_id)
    context = {
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request),
        "annee":annee,
        "parametre":parametre(),
        "date":date
    }
    return render(request, "edit_annee.html", context)

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=['admin'])
@csrf_exempt
def edit_an(request):
    if request.method == "POST":
        id = int(request.POST["id"])
        try:
            annee = Annee.objects.get(id=id)
        except:
            annee = None

        if annee == None:
            return JsonResponse({
                    "status": "error",
                    "message": "Identifiant inexistant."})
        else: 
            libelle = bleach.clean(request.POST["libelle"].strip())
            #On verifie si cette année a déjà été enregistrée
            annees = Annee.objects.exclude(id=id)
            tabAnnee = []
            for an in annees:          
                tabAnnee.append(an.libelle)
            #On verifie si cette année existe déjà
            if libelle in tabAnnee:
                return JsonResponse({
                    "status": "error",
                    "message": "Cette année existe déjà."})
            else:
                annee.libelle = libelle
                annee.save()
                return JsonResponse({
                    "status": "success",
                    "message": "Année modifiée avec succès."})

def ajax_delete_annee(request, id):
    annee = Annee.objects.get(id=id)
    context = {
        "annee": annee
    }
    return render(request, "ajax_delete_annee.html", context)

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=['admin'])
def del_annee(request, id):
    try:
        annee_id = int(dechiffrer_param(str(id)))
        annee = Annee.objects.get(id=annee_id)
    except:
        annee = None
        
    if annee:
        annee.delete()   
    return redirect("annees")
    

