# Importation des modules standard
import bleach
import re
import hashlib
import os
# Importation des modules tiers
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count, Sum
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from decimal import Decimal
# Importation des modules locaux
from eajc.views import get_setting 
from eajcprojet.utils.crypto import dechiffrer_param
from .models import*
from tache.models import Tache


#========================== Gestion de l'article ============================
@login_required(login_url='connection/login')
def contributions(request):
    setting = get_setting()
    if setting is None:
        redirect("settings/maintenance")
    
    user_id = request.user.id    
    # Récupérer les détails de chaque tâche par projet :    
    contribution_pojet = (Contribution.objects.values("projet_id").annotate(nb_actionnaires=Count("projet_id"))).order_by("-projet_id")
    tabProjets = []
    for cp in contribution_pojet:
        projet = Projet.objects.get(id=cp["projet_id"])
        if request.user.is_superuser:
            dic = {}
            dic["projet"] = projet
            dic["contributions"] = projet.contributions.all()
            dic["nb_actionnaires"] = cp["nb_actionnaires"]
            
            # Calculer le montant total des contributeurs
            total_montant_actionnaire = Contribution.objects.filter(projet_id=cp["projet_id"]).aggregate(Sum('montant_contribution'))['montant_contribution__sum'] or 0
            dic["total_montant_actionnaire"] = total_montant_actionnaire
            dic["cout_total_enregistre"] = total_montant_actionnaire + projet.montant_responsable
            dic["cout_reste"] = projet.cout_estime - total_montant_actionnaire + projet.montant_responsable
            
            tabProjets.append(dic)
        else:
            # Verifier si l'utilisateur est un actionnaire du projet
            contribution = Contribution.objects.filter(projet_id=projet.id, actionnaire_id=user_id)
            if projet.responsable.id == user_id or contribution.exists():
                dic = {}
                dic["projet"] = projet
                dic["contributions"] = projet.contributions.all()
                dic["nb_actionnaires"] = cp["nb_actionnaires"]
                
                # Calculer le montant total des contributeurs
                total_montant_actionnaire = Contribution.objects.filter(projet_id=cp["projet_id"]).aggregate(Sum('montant_contribution'))['montant_contribution__sum'] or 0
                dic["total_montant_actionnaire"] = total_montant_actionnaire
                dic["cout_total_enregistre"] = total_montant_actionnaire + projet.montant_responsable
                dic["cout_reste"] = projet.cout_estime - total_montant_actionnaire + projet.montant_responsable
                
                tabProjets.append(dic)
            
    paginator = Paginator(tabProjets, 10)
    num_page = request.GET.get('page')
    tabProjets = paginator.get_page(num_page)

    context = {
        "projets": tabProjets,
        "setting": setting
    }
    return render(request, "contributions.html", context)



@login_required(login_url='connection/login')
def add_contribution(request):
    
    setting = get_setting()
    if setting is None:
        redirect("settings/maintenance")
    
    if request.method == "POST":
        projet_id = request.POST["projet"]
        actionnaire_id = request.POST["actionnaire"]
        date_contribution = bleach.clean(request.POST["date_contribution"].strip())
        montant_contribution = bleach.clean(request.POST["montant_contribution"].strip())
        
        # Nettoyer la valeur (supprimer les espaces et remplacer la virgule par un point)
        montant_contribution = re.sub(r'\xa0', '', montant_contribution)  # Supprime les espaces insécables
        montant_contribution = montant_contribution.replace(" ", "").replace(",", ".")

        try:
            montant_contribution = Decimal(montant_contribution)  # Convertir en Decimal
        except:
            return JsonResponse({
                "status": "error",
                "message": "Le coût doit être un nombres valide."})

        # Récuperer le projet 
        projet = get_object_or_404(Projet, id=projet_id)
        if montant_contribution > projet.cout_estime:
            return JsonResponse({
                    "status": "error",
                    "message": "Le montant de contribution ne peut pas être superieur au coût estimé du projet."})
                
        # retourne la somme totale des contributions du projet. Si aucune contribution n'existe, il retourne 0.
        total_montant_contribution = Contribution.objects.filter(projet_id=projet_id).aggregate(Sum('montant_contribution'))['montant_contribution__sum'] or 0
        if (montant_contribution + total_montant_contribution + projet.montant_responsable) > projet.cout_estime:
            return JsonResponse({
                    "status": "error",
                    "message": "Le montant total de contribution ne peut pas être superieur au coût estimé du projet."})
        
        query = Contribution.objects.filter(projet_id=projet_id, actionnaire_id=actionnaire_id)
        if query.exists():
            return JsonResponse({
                    "status": "error",
                    "message": "Cette contribution existe déjà"})
        else:
            contribution = Contribution(
                projet_id=projet_id,
                actionnaire_id=actionnaire_id, 
                date_contribution=date_contribution,
                montant_contribution=montant_contribution)
            # Nombre de contribution avant l'ajout
            count0 = Contribution.objects.all().count()
            contribution.save()
            # Nombre de contributions après l'ajout
            count1 = Contribution.objects.all().count()
            # On verifie si l'insertion a eu lieu ou pas.
            if count0 < count1:
                return JsonResponse({
                    "status": "success",
                    "message": "Contribution enregistrée avec succès."})
            else:
                return JsonResponse({
                    "status": "error",
                    "message": "L'opération a échoué."})
        
            
    projets = Projet.objects.filter(type_projet="Individuel")
    context = {
        "setting": setting,
        "projets": projets
    }
    return render(request, "add_contribution.html", context)


@login_required(login_url='connection/login')
def edit_contribution(request, id):
    setting = get_setting()
    if setting is None:
        redirect("settings/maintenance")
    
    contribution_id = int(dechiffrer_param(str(id)))   
    contribution = get_object_or_404(Contribution, id=contribution_id)
    
    projets = Projet.objects.filter(type_projet="Individuel").exclude(id=contribution.projet.id)
    actionnaires = User.objects.exclude(id__in=[contribution.actionnaire.id, contribution.projet.responsable.id])
    context = {
            "setting": setting,
            "contribution": contribution,
            "actionnaires": actionnaires,
            "projets": projets
    }
    return render(request, "edit_contribution.html", context)
    

@login_required(login_url='connection/login')
def edit_cont(request):
    if request.method == "POST":
        id = int(request.POST["id"])
        try:
            contribution = get_object_or_404(Contribution, id=id)
        except:
            contribution = None
        
        if contribution is None:
            return JsonResponse({
                    "status": "error",
                    "message": "Identifiant inexistant."})
        else:
            projet_id = request.POST["projet"]
            actionnaire_id = request.POST["actionnaire"]
            date_contribution = bleach.clean(request.POST["date_contribution"].strip())
            montant_contribution = bleach.clean(request.POST["montant_contribution"].strip())
            
            # Nettoyer la valeur (supprimer les espaces et remplacer la virgule par un point)
            montant_contribution = re.sub(r'\xa0', '', montant_contribution)  # Supprime les espaces insécables
            montant_contribution = montant_contribution.replace(" ", "").replace(",", ".")

            try:
                montant_contribution = Decimal(montant_contribution)  # Convertir en Decimal
            except:
                return JsonResponse({
                    "status": "error",
                    "message": "Le coût doit être un nombre valide."})

            # Récuperer le projet 
            projet = get_object_or_404(Projet, id=projet_id)
            if montant_contribution > projet.cout_estime:
                return JsonResponse({
                        "status": "error",
                        "message": "Le montant de contribution ne peut pas être superieur au coût estimé du projet."})
                
            # retourne la somme totale des contributions du projet. Si aucune contribution n'existe, il retourne 0.
            total_montant_contribution = Contribution.objects.filter(projet_id=projet_id).aggregate(Sum('montant_contribution'))['montant_contribution__sum'] or 0
            if (montant_contribution + total_montant_contribution + projet.montant_responsable - contribution.montant_contribution) > projet.cout_estime:
                return JsonResponse({
                        "status": "error",
                        "message": "Le montant total de contribution ne peut pas être superieur au coût estimé du projet."})
            
            #On exclut la contribution que l'on veut modifier
            contributions = Contribution.objects.exclude(id=id)
            tabContributions = []
            for cont in contributions:
                dic = {}  
                dic["projet_id"] = cont.projet.id
                dic["actionnaire_id"] = cont.actionnaire.id      
                
                tabContributions.append(dic)

            new_dic = {}
            new_dic["projet_id"] = int(projet_id)
            new_dic["actionnaire_id"] = int(actionnaire_id) 
            #On verifie si cette contribution existe déjà
            if new_dic in tabContributions:
                return JsonResponse({
                    "status": "error",
                    "message": "Cette contribution existe déjà."})
            else:
                contribution.projet_id = projet_id
                contribution.actionnaire_id = actionnaire_id
                contribution.montant_contribution = montant_contribution
                contribution.date_contribution = date_contribution
                    
                contribution.save()
                return JsonResponse({
                    "status": "success",
                    "message": "Contribution modifiée avec succès."})
            


@login_required(login_url='connection/login')
def del_contribution(request, id):
    try:  
        contribution_id = int(dechiffrer_param(str(id)))  
        contribution = get_object_or_404(Contribution, id=contribution_id)
    except:
        contribution = None
        
    if contribution:
        contribution.delete()
    return redirect("contributions")

def ajax_actionnaire_contribution(request, projet_id):
    projet = get_object_or_404(Projet, id=projet_id)
    actionnaires = User.objects.exclude(id=projet.responsable.id)
    context = {
        "actionnaires": actionnaires
    }
    return render(request, "ajax_actionnaire_contribution.html", context)

def ajax_devise(request, projet_id):
    projet = get_object_or_404(Projet, id=projet_id)
    context = {
        "symbole": projet.devise.symbole
    }
    return render(request, "ajax_devise.html", context)

