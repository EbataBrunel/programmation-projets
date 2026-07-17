# Importation des modules standard
import bleach
import re
# Importation des modules tiers
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count
from django.views import View
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from decimal import Decimal
# Importation des modules locaux
from eajc.views import get_setting 
from eajcprojet.utils.crypto import dechiffrer_param
from .models import*
from contribution.models import Contribution
from participation.models import Participation

@login_required(login_url='connection/login')
def depense_projet_p(request):
    setting = get_setting()
    if setting is None:
        redirect("settings/maintenance")
        
    # Récupérer les détails de chaque tâche par projet :    
    depense_pojet = Depense.objects.values("projet_id").annotate(nb_depenses=Count("projet_id"))
    tabProjets = []
    for dp in depense_pojet:
        projet = Projet.objects.get(id=dp["projet_id"])
        if projet.type_projet == "Personnel" and projet.responsable.id == request.user.id:
            depenses_taches = (Depense.objects.values("tache_id").
                             filter(projet_id=dp["projet_id"]).
                             annotate(nb_taches=Count("tache_id")))
            for dt in depenses_taches:
                dic = {}
                dic["projet"] = projet
                dic["nb_taches"] = dt["nb_taches"]
                tabProjets.append(dic)
                
    paginator = Paginator(tabProjets, 10)
    num_page = request.GET.get('page')
    tabProjets = paginator.get_page(num_page)

    context = {
        "projets": tabProjets,
        "setting": setting
    }
    return render(request, "depense_projet_p.html", context)



@login_required(login_url='connection/login')
def depense_tache_p(request, projet_id):
    setting = get_setting()
    if setting is None:
        redirect("settings/maintenance")
        
    # Récupérer les détails de chaque tâche par projet :   
    id = int(dechiffrer_param(str(projet_id))) 
    depenses_taches = Depense.objects.filter(projet_id=id)
    
    paginator = Paginator(depenses_taches, 10)
    num_page = request.GET.get('page')
    depenses_taches = paginator.get_page(num_page)

    context = {
        "depenses": depenses_taches,
        "setting": setting
    }
    return render(request, "depense_tache_p.html", context)

@login_required(login_url='connection/login')
def add_depense_p(request):
    
    user_id = request.user.id
    setting = get_setting()
    if setting is None:
        redirect("settings/maintenance")
    
    if request.method == "POST":
        projet_id = request.POST["projet"]
        tache_id = request.POST["tache"]
        description = bleach.clean(request.POST["description"].strip())
        montant = bleach.clean(request.POST["montant"].strip())
        date_paiement = bleach.clean(request.POST["date_paiement"].strip())
        type_depense = bleach.clean(request.POST["type_depense"].strip())
        
        if type_depense == "Autre":
                autre_type_depense = bleach.clean(request.POST["autre_type_depense"].strip())
                type_depense = autre_type_depense
                
        query = Depense.objects.filter(projet_id=projet_id, tache_id=tache_id)
        if query.exists():
            return JsonResponse({
                "status": "error",
                "message": "Cette dépense existe déjà"})
        else:
            depense = Depense(
                projet_id=projet_id,
                tache_id=tache_id, 
                description=description, 
                montant=montant, 
                date_paiement=date_paiement,
                type_depense=type_depense)
            # Nombre de dépenses avant l'ajout
            count0 = Depense.objects.all().count()
            depense.save()
            # Nombre de dépenses après l'ajout
            count1 = Depense.objects.all().count()
            # On verifie si l'insertion a eu lieu ou pas.
            if count0 < count1:
                return JsonResponse({
                    "status": "success",
                    "message": "Dépense enregistrée avec succès."})
            else:
                return JsonResponse({
                    "status": "error",
                    "message": "L'opération a échoué."})

    projets = Projet.objects.filter(responsable_id=user_id, type_projet="Personnel")
    type_depenses = ["Main d'oeuvre", "Logiciel", "Matériel", "Infrastructure", "Autre"]
    context = {
        "setting": setting,
        "projets": projets,
        "type_depenses": type_depenses
    }
    return render(request, "add_depense_p.html", context)


@login_required(login_url='connection/login')
def edit_depense_p(request, id):
    user_id = request.user.id
    setting = get_setting()
    if setting is None:
        redirect("settings/maintenance")
    
    depense_id = int(dechiffrer_param(str(id)))   
    depense = get_object_or_404(Depense, id=depense_id)
    #On vérifie si ce membre est authorisé à acceder à cette page ou pas.
    projet = Projet.objects.get(id=depense.projet.id)
    if projet.responsable.id == user_id:
        projets = Projet.objects.filter(responsable_id=user_id).exclude(id=depense.projet.id)
        taches = Tache.objects.filter(projet_id=depense.projet.id).exclude(id=depense.tache.id)
        context = {
            "setting": setting,
            "depense": depense,
            "taches": taches,
            "projets": projets
        }
        return render(request, "edit_depense_p.html", context)
    else:
        return redirect("authorization")

@login_required(login_url='connection/login')
def edit_dep_p(request):
    if request.method == "POST":
        id = int(request.POST["id"])
        try:
            depense = get_object_or_404(Depense, id=id)
        except:
            depense = None
        
        if depense is None:
            return JsonResponse({
                    "status": "error",
                    "message": "Identifiant inexistant."})
        else:
            projet_id = request.POST["projet"]
            tache_id = request.POST["tache"]
            # Se proteger de l'attaque XSS(Injection du code javascript)
            description = bleach.clean(request.POST["description"].strip())
            montant = bleach.clean(request.POST["montant"].strip())
            date_paiement = bleach.clean(request.POST["date_paiement"].strip())
            type_depense = bleach.clean(request.POST["type_depense"].strip())
            if type_depense == "Autres":
                autre_type_depense = bleach.clean(request.POST["autre_type_depense"].strip())
                type_depense = autre_type_depense
                
            montant = re.sub(r'\xa0', '', montant)  # Supprime les espaces insécables
            montant = montant.replace(" ", "").replace(",", ".")

            try:
                montant = Decimal(montant)  # Convertir en Decimal
            except:
                return JsonResponse({
                    "status": "error",
                    "message": "Le montant être un nombre valide."})
                
            #On exclut la dépense que l'on veut modifier
            depenses = Depense.objects.exclude(id=id)
            tabDepenses = []
            for dep in depenses:
                try:
                    if dep.projet.responsable.id == request.user.id:
                        tabDepenses.append(dep)
                except Exception as e:
                    pass
            #On verifie si cette tâche existe déjà
            # Verifier l'existence de ce parcours
            x = False
            for d in tabDepenses:
                if int(projet_id) == d.projet.id and int(tache_id) == d.tache.id:
                    x = True
            if x :
                return JsonResponse({
                    "status": "error",
                    "message": "Cette dépense existe déjà."})
            else:
                depense.projet_id = projet_id
                depense.tache_id = tache_id
                depense.description = description
                depense.montant = montant
                depense.date_paiement = date_paiement
                depense.type_depense = type_depense
                depense.save()
                return JsonResponse({
                    "status": "success",
                    "message": "Dépense modifiée avec succès."})


@login_required(login_url='connection/login')
def del_depense_p(request, id):
    try: 
        depense_id = int(dechiffrer_param(str(id)))   
        depense = get_object_or_404(Depense, id=depense_id)
    except:
        depense = None
        
    if depense:
        depense.delete()
    return redirect("depense_projet_g")


def ajax_depense_projet(request, projet_id):
    taches = Tache.objects.filter(projet_id=projet_id)
    context = {
        "taches": taches
    }
    return render(request, "ajax_depense_projet.html", context)

class autre_type_depense(View):
    def get(self, request, type_depense, *args, **kwargs):
        context = {"type_depense": type_depense}
        return render(request, "content_other_type.html", context)
    
#============== Depense en commun =========================   
@login_required(login_url='connection/login')
def depense_projet_g(request):
    setting = get_setting()
    if setting is None:
        redirect("settings/maintenance")
    
    user_id = request.user.id    
    # Récupérer les détails de chaque tâche par projet :    
    depense_pojet = Depense.objects.values("projet_id").annotate(nb_depenses=Count("projet_id"))
    tabProjets = []
    for dp in depense_pojet:
        projet = Projet.objects.get(id=dp["projet_id"])
        if projet.type_projet == "Individuel":
            if request.user.is_superuser:
                depenses_taches = (Depense.objects.values("tache_id").
                                filter(projet_id=dp["projet_id"]).
                                annotate(nb_taches=Count("tache_id")))
                for dt in depenses_taches:
                    dic = {}
                    dic["projet"] = projet
                    dic["nb_taches"] = dt["nb_taches"]
                    tabProjets.append(dic)
            else:
                # Verifier si l'utilisateur est un actionnaire ou un acteur du projet
                contribution = Contribution.objects.filter(projet_id=projet.id, actionnaire_id=user_id)
                participation = Participation.objects.filter(projet_id=projet.id, acteur_id=user_id)
                if projet.responsable.id == user_id or contribution.exists() or participation.exists():
                    depenses_taches = (Depense.objects.values("tache_id").
                                filter(projet_id=dp["projet_id"]).
                                annotate(nb_taches=Count("tache_id")))
                    for dt in depenses_taches:
                        dic = {}
                        dic["projet"] = projet
                        dic["nb_taches"] = dt["nb_taches"]
                        tabProjets.append(dic)
                
    paginator = Paginator(tabProjets, 10)
    num_page = request.GET.get('page')
    tabProjets = paginator.get_page(num_page)

    context = {
        "projets": tabProjets,
        "setting": setting
    }
    return render(request, "depense_projet_g.html", context)



@login_required(login_url='connection/login')
def depense_tache_g(request, projet_id):
    setting = get_setting()
    if setting is None:
        redirect("settings/maintenance")
        
    # Récupérer les détails de chaque tâche par projet :  
    id = int(dechiffrer_param(str(projet_id)))  
    depenses_taches = Depense.objects.filter(projet_id=id)
    
    paginator = Paginator(depenses_taches, 10)
    num_page = request.GET.get('page')
    depenses_taches = paginator.get_page(num_page)

    context = {
        "depenses": depenses_taches,
        "setting": setting
    }
    return render(request, "depense_tache_g.html", context)

@login_required(login_url='connection/login')
def add_depense_g(request):
    setting = get_setting()
    if setting is None:
        redirect("settings/maintenance")
    
    if request.method == "POST":
        projet_id = request.POST["projet"]
        tache_id = request.POST["tache"]
        description = bleach.clean(request.POST["description"].strip())
        montant = bleach.clean(request.POST["montant"].strip())
        date_paiement = bleach.clean(request.POST["date_paiement"].strip())
        type_depense = bleach.clean(request.POST["type_depense"].strip())
        
        if type_depense == "Autre":
                autre_type_depense = bleach.clean(request.POST["autre_type_depense"].strip())
                type_depense = autre_type_depense
                
        query = Depense.objects.filter(projet_id=projet_id, tache_id=tache_id)
        if query.exists():
            return JsonResponse({
                "status": "error",
                "message": "Cette dépense existe déjà"})
        else:
            depense = Depense(
                projet_id=projet_id,
                tache_id=tache_id, 
                description=description, 
                montant=montant, 
                date_paiement=date_paiement,
                type_depense=type_depense)
            # Nombre de dépenses avant l'ajout
            count0 = Depense.objects.all().count()
            depense.save()
            # Nombre de dépenses après l'ajout
            count1 = Depense.objects.all().count()
            # On verifie si l'insertion a eu lieu ou pas.
            if count0 < count1:
                return JsonResponse({
                    "status": "success",
                    "message": "Dépense enregistrée avec succès."})
            else:
                return JsonResponse({
                    "status": "error",
                    "message": "L'opération a échoué."})

    projets = Projet.objects.filter(type_projet__in=["Individuel", "En groupe"])
    type_depenses = ["Main d'oeuvre", "Logiciel", "Matériel", "Infrastructure", "Autre"]
    context = {
        "setting": setting,
        "projets": projets,
        "type_depenses": type_depenses
    }
    return render(request, "add_depense_g.html", context)


@login_required(login_url='connection/login')
def edit_depense_g(request, id):
    user_id = request.user.id
    setting = get_setting()
    if setting is None:
        redirect("settings/maintenance")
    
    depense_id = int(dechiffrer_param(str(id)))    
    depense = get_object_or_404(Depense, id=depense_id)
    #On vérifie si ce membre est authorisé à acceder à cette page ou pas.
    projet = Projet.objects.get(id=depense.projet.id)
    if projet.responsable.id == user_id:
        projets = Projet.objects.filter(type_projet__in=["Individuel", "En groupe"]).exclude(id=depense.projet.id)
        taches = Tache.objects.filter(projet_id=depense.projet.id).exclude(id=depense.tache.id)
        context = {
            "setting": setting,
            "depense": depense,
            "taches": taches,
            "projets": projets
        }
        return render(request, "edit_depense_g.html", context)

@login_required(login_url='connection/login')
def edit_dep_g(request):
    if request.method == "POST":
        id = int(request.POST["id"])
        try:
            depense = get_object_or_404(Depense, id=id)
        except:
            depense = None
        
        if depense is None:
            return JsonResponse({
                    "status": "error",
                    "message": "Identifiant inexistant."})
        else:
            projet_id = request.POST["projet"]
            tache_id = request.POST["tache"]
            # Se proteger de l'attaque XSS(Injection du code javascript)
            description = bleach.clean(request.POST["description"].strip())
            montant = bleach.clean(request.POST["montant"].strip())
            date_paiement = bleach.clean(request.POST["date_paiement"].strip())
            type_depense = bleach.clean(request.POST["type_depense"].strip())
            if type_depense == "Autres":
                autre_type_depense = bleach.clean(request.POST["autre_type_depense"].strip())
                type_depense = autre_type_depense
                
            montant = re.sub(r'\xa0', '', montant)  # Supprime les espaces insécables
            montant = montant.replace(" ", "").replace(",", ".")

            try:
                montant = Decimal(montant)  # Convertir en Decimal
            except:
                return JsonResponse({
                    "status": "error",
                    "message": "Le montant être un nombre valide."})
                
            #On exclut la dépense que l'on veut modifier
            depenses = Depense.objects.exclude(id=id)
            tabDepenses = []
            for dep in depenses:
                try:
                    if dep.projet.type_projet == "Individuel" or dep.projet.type_projet == "En groupe":
                        tabDepenses.append(dep)
                except Exception as e:
                    pass
            #On verifie si cette tâche existe déjà
            # Verifier l'existence de ce parcours
            x = False
            for d in tabDepenses:
                if int(projet_id) == d.projet.id and int(tache_id) == d.tache.id:
                    x = True
            if x :
                return JsonResponse({
                    "status": "error",
                    "message": "Cette dépense existe déjà."})
            else:
                depense.projet_id = projet_id
                depense.tache_id = tache_id
                depense.description = description
                depense.montant = montant
                depense.date_paiement = date_paiement
                depense.type_depense = type_depense
                depense.save()
                return JsonResponse({
                    "status": "success",
                    "message": "Dépense modifiée avec succès."})


@login_required(login_url='connection/login')
def del_depense_g(request, id):
    try:   
        depense_id = int(dechiffrer_param(str(id))) 
        depense = get_object_or_404(Depense, id=depense_id)
    except:
        depense = None
        
    if depense:
        depense.delete()
    return redirect("depense_projet_g")


class tri_depense(View):
    def get(self, request, action, *args, **kwargs):
        setting = get_setting()
        if setting is None:
            redirect("settings/maintenance")
            
        # Récupérer les détails de chaque tâche par projet :    
        depense_pojet = Depense.objects.values("projet_id").annotate(nb_depenses=Count("projet_id"))
        tabProjets = []
        for dp in depense_pojet:
            projet = Projet.objects.get(id=dp["projet_id"])
            if projet.type_projet == action:
                depenses_taches = (Depense.objects.values("tache_id").
                                filter(projet_id=dp["projet_id"]).
                                annotate(nb_taches=Count("tache_id")))
                for dt in depenses_taches:
                    dic = {}
                    dic["projet"] = projet
                    dic["nb_taches"] = dt["nb_taches"]
                    tabProjets.append(dic)
                    
        paginator = Paginator(tabProjets, 10)
        num_page = request.GET.get('page')
        tabProjets = paginator.get_page(num_page)
    
        context = {
            "projets": tabProjets,
            "setting": setting
        }
        return render(request, "content_depense.html", context) 
    
def ajax_devise(request, projet_id):
    projet = get_object_or_404(Projet, id=projet_id)
    context = {
        "symbole": projet.devise.symbole
    }
    return render(request, "ajax_devise.html", context)

