# Importation des modules standard
import bleach
import re
# Importation des modules tiers
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count
from django.db.models import Sum
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from decimal import Decimal
# Importation des modules locaux
from eajc.views import get_setting 
from eajcprojet.utils.crypto import dechiffrer_param
from .models import*


#========================== Gestion de l'article ============================
@login_required(login_url='connection/login')
def participations(request):
    setting = get_setting()
    if setting is None:
        redirect("settings/maintenance")
    
    user_id = request.user.id  
    # Récupérer les détails de chaque tâche par projet :    
    participation_pojet = (Participation.objects.values("projet_id").annotate(nb_acteurs=Count("projet_id")))
    tabProjets = []
    for cp in participation_pojet:
        projet = Projet.objects.get(id=cp["projet_id"])
        
        if request.user.is_superuser:
            dic = {}
            dic["projet"] = projet
            dic["participations"] = projet.participations.all()
            dic["nb_acteurs"] = cp["nb_acteurs"]
            # Calculer le montant total des participants
            total_montant_participation = Participation.objects.filter(projet_id=cp["projet_id"]).aggregate(Sum('montant_participation'))['montant_participation__sum'] or 0
            dic["total_montant_participation"] = total_montant_participation
            dic["cout_total_enregistre"] = total_montant_participation + projet.montant_responsable
            dic["cout_reste"] = projet.cout_estime - total_montant_participation + projet.montant_responsable
            tabProjets.append(dic)
        else:
            # Verifier si l'utilisateur est un actionnaire du projet
            participation = Participation.objects.filter(projet_id=projet.id, acteur_id=user_id)
            if projet.responsable.id == user_id or participation.exists():
                dic = {}
                dic["projet"] = projet
                dic["participations"] = projet.participations.all()
                dic["nb_acteurs"] = cp["nb_acteurs"]
                # Calculer le montant total des participants
                total_montant_participation = Participation.objects.filter(projet_id=cp["projet_id"]).aggregate(Sum('montant_participation'))['montant_participation__sum'] or 0
                dic["total_montant_participation"] = total_montant_participation
                dic["cout_total_enregistre"] = total_montant_participation + projet.montant_responsable
                dic["cout_reste"] = projet.cout_estime - total_montant_participation + projet.montant_responsable
                tabProjets.append(dic)
            
    paginator = Paginator(tabProjets, 10)
    num_page = request.GET.get('page')
    tabProjets = paginator.get_page(num_page)

    context = {
        "projets": tabProjets,
        "setting": setting
    }
    return render(request, "participations.html", context)



@login_required(login_url='connection/login')
def add_participation(request):
    
    setting = get_setting()
    if setting is None:
        redirect("settings/maintenance")
    
    if request.method == "POST":
        projet_id = request.POST["projet"]
        acteur_id = request.POST["acteur"]
        date_participation = bleach.clean(request.POST["date_participation"].strip())
        montant_participation = bleach.clean(request.POST["montant_participation"].strip())
        
        # Nettoyer la valeur (supprimer les espaces et remplacer la virgule par un point)
        montant_participation = re.sub(r'\xa0', '', montant_participation)  # Supprime les espaces insécables
        montant_participation = montant_participation.replace(" ", "").replace(",", ".")

        try:
            montant_participation = Decimal(montant_participation)  # Convertir en Decimal
        except:
            return JsonResponse({
                "status": "error",
                "message": "Le coût doit être un nombres valide."})

        # Récuperer le projet 
        projet = get_object_or_404(Projet, id=projet_id)
        if montant_participation > projet.cout_estime:
            return JsonResponse({
                    "status": "error",
                    "message": "Le montant de participation ne peut pas être superieur au coût estimé du projet."})
                
        # retourne la somme totale des participations du projet. Si aucune participation n'existe, il retourne 0.
        total_montant_participation = Participation.objects.filter(projet_id=projet_id).aggregate(Sum('montant_participation'))['montant_participation__sum'] or 0
        if (montant_participation + total_montant_participation + projet.montant_responsable) > projet.cout_estime:
            return JsonResponse({
                    "status": "error",
                    "message": "Le montant total de participation ne peut pas être superieur au coût estimé du projet."})
        
        query = Participation.objects.filter(projet_id=projet_id, acteur_id=acteur_id)
        if query.exists():
            return JsonResponse({
                    "status": "error",
                    "message": "Cette participation existe déjà"})
        else:
            participation = Participation(
                projet_id=projet_id,
                acteur_id=acteur_id, 
                date_participation=date_participation,
                montant_participation=montant_participation)
            # Nombre de participations avant l'ajout
            count0 = Participation.objects.all().count()
            participation.save()
            # Nombre de participations après l'ajout
            count1 = Participation.objects.all().count()
            # On verifie si l'insertion a eu lieu ou pas.
            if count0 < count1:
                return JsonResponse({
                    "status": "success",
                    "message": "Participation enregistrée avec succès."})
            else:
                return JsonResponse({
                    "status": "error",
                    "message": "L'opération a échoué."})
        
            
    projets = Projet.objects.filter(type_projet="En groupe")
    context = {
        "setting": setting,
        "projets": projets
    }
    return render(request, "add_participation.html", context)


@login_required(login_url='connection/login')
def edit_participation(request, id):
    setting = get_setting()
    if setting is None:
        redirect("settings/maintenance")
    
    participation_id = int(dechiffrer_param(str(id)))    
    participation = get_object_or_404(Participation, id=participation_id)
    
    projets = Projet.objects.filter(type_projet="En groupe").exclude(id=participation.projet.id)
    acteurs = User.objects.exclude(id__in=[participation.acteur.id, participation.projet.responsable.id])
    context = {
            "setting": setting,
            "participation": participation,
            "acteurs": acteurs,
            "projets": projets
    }
    return render(request, "edit_participation.html", context)
    

@login_required(login_url='connection/login')
def edit_part(request):
    if request.method == "POST":
        id = int(request.POST["id"])
        try:
            participation = get_object_or_404(Participation, id=id)
        except:
            participation = None
        
        if participation is None:
            return JsonResponse({
                    "status": "error",
                    "message": "Identifiant inexistant."})
        else:
            projet_id = request.POST["projet"]
            acteur_id = request.POST["acteur"]
            date_participation = bleach.clean(request.POST["date_participation"].strip())
            montant_participation = bleach.clean(request.POST["montant_participation"].strip())

            # Nettoyer la valeur (supprimer les espaces et remplacer la virgule par un point)
            montant_participation = re.sub(r'\xa0', '', montant_participation)  # Supprime les espaces insécables
            montant_participation = montant_participation.replace(" ", "").replace(",", ".")

            try:
                montant_participation = Decimal(montant_participation)  # Convertir en Decimal
            except:
                return JsonResponse({
                    "status": "error",
                    "message": "Le coût doit être un nombres valide."})

            # Récuperer le projet 
            projet = get_object_or_404(Projet, id=projet_id)
            if montant_participation > projet.cout_estime:
                return JsonResponse({
                        "status": "error",
                        "message": "Le montant de participation ne peut pas être superieur au coût estimé du projet."})
                
            # retourne la somme totale des participations du projet. Si aucune participation n'existe, il retourne 0.
            total_montant_participation = Participation.objects.filter(projet_id=projet_id).aggregate(Sum('montant_participation'))['montant_participation__sum'] or 0
            if (montant_participation + total_montant_participation + projet.montant_responsable - participation.montant_participation) > projet.cout_estime:
                return JsonResponse({
                        "status": "error",
                        "message": "Le montant total de participation ne peut pas être superieur au coût estimé du projet."})
            
            #On exclut la participation que l'on veut modifier
            participations = Participation.objects.exclude(id=id)
            tabParticipations = []
            for part in participations:
                dic = {}  
                dic["projet_id"] = part.projet.id
                dic["acteur_id"] = part.acteur.id      
                
                tabParticipations.append(dic)

            new_dic = {}
            new_dic["projet_id"] = int(projet_id)
            new_dic["acteur_id"] = int(acteur_id) 
            #On verifie si cette participation existe déjà
            if new_dic in tabParticipations:
                return JsonResponse({
                    "status": "error",
                    "message": "Cette participation existe déjà."})
            else:
                participation.projet_id = projet_id
                participation.acteur_id = acteur_id
                participation.montant_participation = montant_participation
                participation.date_participation = date_participation
                    
                participation.save()
                return JsonResponse({
                    "status": "success",
                    "message": "Participation modifiée avec succès."})
            


@login_required(login_url='connection/login')
def del_participation(request, id):
    try: 
        participation_id = int(dechiffrer_param(str(id)))   
        participation = get_object_or_404(Participation, id=participation_id)
    except:
        participation = None
        
    if participation:
        participation.delete()
    return redirect("participations")

def ajax_acteur_participation(request, projet_id):
    projet = get_object_or_404(Projet, id=projet_id)
    acteurs = User.objects.exclude(id=projet.responsable.id)
    context = {
        "acteurs": acteurs
    }
    return render(request, "ajax_acteur_participation.html", context)

def ajax_devise(request, projet_id):
    projet = get_object_or_404(Projet, id=projet_id)
    context = {
        "symbole": projet.devise.symbole
    }
    return render(request, "ajax_devise.html", context)

