# Importation des modules standard
import bleach
import re

# Importation des modules tiers
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from datetime import datetime
from django.views import View
from django.db.models import Sum
from decimal import Decimal
# Importation des modules locaux
from eajc.views import get_setting 
from eajcprojet.utils.crypto import dechiffrer_param
from .models import*
from contribution.models import Contribution
from participation.models import Participation


#========================== Tache personnel ============================
@login_required(login_url='connection/login')
def taches_p(request):
    setting = get_setting()
    if setting is None:
        redirect("settings/maintenance")
        
    # Récupérer les détails de chaque tâche par projet :    
    taches_pojet = (Tache.objects.values("projet_id").annotate(nb_taches=Count("projet_id")))
    tabProjets = []
    nb_taches = 0
    for ta in taches_pojet:
        projet = Projet.objects.get(id=ta["projet_id"])
        if projet.type_projet == "Personnel" and projet.responsable.id == request.user.id:
            nb_taches += 1
            dic = {}
            dic["projet"] = projet
            tabTaches = []
            taches = projet.taches.all()
            for tache in taches:
                dic_tache = {}
                dic_tache["tache"] = tache
                dic_tache["depenses"] = tache.depenses.all()
                tabTaches.append(dic_tache)
            dic["taches"] = tabTaches
            tabProjets.append(dic)
            
    paginator = Paginator(tabProjets, 10)
    num_page = request.GET.get('page')
    tabProjets = paginator.get_page(num_page)

    context = {
        "projets": tabProjets,
        "setting": setting
    }
    return render(request, "taches_p.html", context)


@login_required(login_url='connection/login')
def add_tp(request):
    
    user_id = request.user.id
    setting = get_setting()
    if setting is None:
        redirect("settings/maintenance")
    
    if request.method == "POST":
        projet_id = request.POST["projet"]
        nom = bleach.clean(request.POST["nom"].strip())
        description = bleach.clean(request.POST["description"].strip())
        date_debut = bleach.clean(request.POST["date_debut"].strip())
        date_fin = bleach.clean(request.POST["date_fin"].strip())
        cout_estime = bleach.clean(request.POST["cout_estime"].strip())
        cout_reel = bleach.clean(request.POST["cout_reel"].strip())
        
        # Conversion de date string en date pour mieux faire la comparaison
        date_format = "%Y-%m-%d"
        date_d = datetime.strptime(date_debut, date_format).date()
        date_f = datetime.strptime(date_fin, date_format).date()
        # Récuperer le projet
        projet = get_object_or_404(Projet, id=projet_id)
        if date_d >= projet.date_debut and date_f <= projet.date_fin:
            
            if date_debut > date_fin:
                return JsonResponse({
                    "status": "error",
                    "message": "Date de début doit être supérieure à la date de fin"})
            
            query = Tache.objects.filter(nom=nom, projet_id=projet_id)
            if query.exists():
                return JsonResponse({
                    "status": "error",
                    "message": "Ce projet existe déjà"})
            else:
                tache = Tache(
                    projet_id=projet_id,
                    nom=nom, 
                    description=description, 
                    date_debut=date_debut, 
                    date_fin=date_fin,
                    cout_estime=cout_estime,
                    cout_reel=cout_reel)
                # Nombre de projets avant l'ajout
                count0 = Tache.objects.all().count()
                tache.save()
                # Nombre de projets après l'ajout
                count1 = Tache.objects.all().count()
                # On verifie si l'insertion a eu lieu ou pas.
                if count0 < count1:
                    return JsonResponse({
                        "status": "success",
                        "message": "Tache enregistrée avec succès."})
                else:
                    return JsonResponse({
                        "status": "error",
                        "message": "L'opération a échoué."})
        else:
            return JsonResponse({
                "status": "error",
                "message": "La date de début et la date de fin d'une tâche doivent se situer entre la date de début et la date de fin du projet."})
            
    projets = Projet.objects.filter(responsable_id=user_id, type_projet="Personnel")
    context = {
        "setting": setting,
        "projets": projets
    }
    return render(request, "add_tp.html", context)


@login_required(login_url='connection/login')
def edit_tp(request, id):
    user_id = request.user.id
    setting = get_setting()
    if setting is None:
        redirect("settings/maintenance")
    
    tache_id = int(dechiffrer_param(str(id)))    
    tache = get_object_or_404(Tache, id=tache_id)
    #On vérifie si ce membre est authorisé à acceder à cette page ou pas.
    projet = Projet.objects.get(id=tache.projet.id)
    if projet.responsable.id == user_id:
        projets = Projet.objects.filter(responsable_id=user_id).exclude(id=tache.projet.id)
        context = {
            "setting": setting,
            "tache": tache,
            "projets": projets
        }
        return render(request, "edit_tp.html", context)
    else:
        return redirect("authorization")

@login_required(login_url='connection/login')
def edit_tache_p(request):
    if request.method == "POST":
        id = int(request.POST["id"])
        try:
            tache = get_object_or_404(Tache, id=id)
        except:
            tache = None
        
        if tache is None:
            return JsonResponse({
                    "status": "error",
                    "message": "Identifiant inexistant."})
        else:
            projet_id = request.POST["projet"]
            # Se proteger de l'attaque XSS(Injection du code javascript)
            nom = bleach.clean(request.POST["nom"].strip())
            description = bleach.clean(request.POST["description"].strip())
            date_debut = bleach.clean(request.POST["date_debut"].strip())
            date_fin = bleach.clean(request.POST["date_fin"].strip())
            cout_estime = bleach.clean(request.POST["cout_estime"].strip())
            cout_reel = bleach.clean(request.POST["cout_reel"].strip())
            
            # Nettoyer la valeur (supprimer les espaces et remplacer la virgule par un point)
            cout_estime = re.sub(r'\xa0', '', cout_estime)  # Supprime les espaces insécables
            cout_estime = cout_estime.replace(" ", "").replace(",", ".")
            
            cout_reel = re.sub(r'\xa0', '', cout_reel)  # Supprime les espaces insécables
            cout_reel = cout_reel.replace(" ", "").replace(",", ".")

            try:
                cout_estime= Decimal(cout_estime)  # Convertir en Decimal
                cout_reel = Decimal(cout_reel)  # Convertir en Decimal
            except:
                return JsonResponse({
                    "status": "error",
                    "message": "Les coûts doivent être des nombres valides."})
            
            # Conversion de date string en date pour mieux faire la comparaison
            date_format = "%Y-%m-%d"
            date_d = datetime.strptime(date_debut, date_format).date()
            date_f = datetime.strptime(date_fin, date_format).date()
            # Récuperer le projet
            projet = get_object_or_404(Projet, id=projet_id)
            if date_d >= projet.date_debut and date_f <= projet.date_fin:
                
                if date_debut > date_fin:
                    return JsonResponse({
                        "status": "error",
                        "message": "Date de début doit être supérieure à la date de fin"})
                
                #On exclut la tâche que l'on veut modifier
                taches = Tache.objects.exclude(id=id)
                tabTaches = []
                for tach in taches:
                    try:
                        if tach.projet.responsable.id == request.user.id:
                            tabTaches.append(tach.nom)
                    except Exception as e:
                        pass
                #On verifie si cette tâche existe déjà
                if nom in tabTaches:
                    return JsonResponse({
                        "status": "error",
                        "message": "Cette tâche existe déjà."})
                else:
                    tache.projet_id = projet_id
                    tache.nom = nom
                    tache.description = description
                    tache.date_debut = date_debut
                    tache.date_fin = date_fin
                    tache.cout_estime = cout_estime
                    tache.cout_reel = cout_reel
                    tache.save()
                    return JsonResponse({
                        "status": "success",
                        "message": "Tâche modifiée avec succès."})
            else:
                return JsonResponse({
                    "status": "error",
                    "message": "La date de début et la date de fin d'une tâche doivent se situer entre la date de début et la date de fin du projet."})


@login_required(login_url='connection/login')
def del_tp(request,id):
    try:  
        tache_id = int(dechiffrer_param(str(id)))  
        tache = get_object_or_404(Tache, id=tache_id)
    except:
        tache = None
        
    if tache:
        tache.delete()
    return redirect("tache_p")

#========================== Tache en commun ============================
@login_required(login_url='connection/login')
def taches_g(request):
    setting = get_setting()
    if setting is None:
        redirect("settings/maintenance")
    
    user_id = request.user.id   
    # Récupérer les détails de chaque tâche par projet :    
    taches_pojet = (Tache.objects.values("projet_id").annotate(nb_taches=Count("projet_id")))
    tabProjets = []
    for ta in taches_pojet:
        projet = Projet.objects.get(id=ta["projet_id"])
        if projet.type_projet == "Individuel":
            if request.user.is_superuser:
                dic = {}
                dic["projet"] = projet
                tabTaches = []
                taches = projet.taches.all()
                for tache in taches:
                    dic_tache = {}
                    dic_tache["tache"] = tache
                    dic_tache["depenses"] = tache.depenses.all()
                    tabTaches.append(dic_tache)
                dic["taches"] = tabTaches
                tabProjets.append(dic)
            else:
                # Verifier si l'utilisateur est un actionnaire du projet
                contribution = Contribution.objects.filter(projet_id=projet.id, actionnaire_id=user_id)
                if projet.responsable.id == user_id or contribution.exists():
                    dic = {}
                    dic["projet"] = projet
                    tabTaches = []
                    taches = projet.taches.all()
                    for tache in taches:
                        dic_tache = {}
                        dic_tache["tache"] = tache
                        dic_tache["depenses"] = tache.depenses.all()
                        tabTaches.append(dic_tache)
                    dic["taches"] = tabTaches
                    tabProjets.append(dic)
            
    paginator = Paginator(tabProjets, 10)
    num_page = request.GET.get('page')
    tabProjets = paginator.get_page(num_page)

    context = {
        "projets": tabProjets,
        "setting": setting
    }
    return render(request, "taches_g.html", context)


@login_required(login_url='connection/login')
def add_tg(request):
    
    setting = get_setting()
    if setting is None:
        redirect("settings/maintenance")
    
    if request.method == "POST":
        projet_id = request.POST["projet"]
        nom = bleach.clean(request.POST["nom"].strip())
        description = bleach.clean(request.POST["description"].strip())
        date_debut = bleach.clean(request.POST["date_debut"].strip())
        date_fin = bleach.clean(request.POST["date_fin"].strip())
        cout_estime = bleach.clean(request.POST["cout_estime"].strip())
        cout_reel = bleach.clean(request.POST["cout_reel"].strip())
        
        # Conversion de date string en date pour mieux faire la comparaison
        date_format = "%Y-%m-%d"
        date_d = datetime.strptime(date_debut, date_format).date()
        date_f = datetime.strptime(date_fin, date_format).date()
        # Récuperer le projet
        projet = get_object_or_404(Projet, id=projet_id)
        if date_d >= projet.date_debut and date_f <= projet.date_fin:
            
            if date_debut > date_fin:
                return JsonResponse({
                    "status": "error",
                    "message": "Date de début doit être supérieure à la date de fin"})
            
            query = Tache.objects.filter(nom=nom, projet_id=projet_id)
            if query.exists():
                return JsonResponse({
                    "status": "error",
                    "message": "Ce projet existe déjà"})
            else:
                tache = Tache(
                    projet_id=projet_id,
                    nom=nom, 
                    description=description, 
                    date_debut=date_debut, 
                    date_fin=date_fin,
                    cout_estime=cout_estime,
                    cout_reel=cout_reel)
                # Nombre de projets avant l'ajout
                count0 = Tache.objects.all().count()
                tache.save()
                # Nombre de projets après l'ajout
                count1 = Tache.objects.all().count()
                # On verifie si l'insertion a eu lieu ou pas.
                if count0 < count1:
                    return JsonResponse({
                        "status": "success",
                        "message": "Tache enregistrée avec succès."})
                else:
                    return JsonResponse({
                        "status": "error",
                        "message": "L'opération a échoué."})
        else:
            return JsonResponse({
                "status": "error",
                "message": "La date de début et la date de fin d'une tâche doivent se situer entre la date de début et la date de fin du projet."})
            
    projets = Projet.objects.filter(type_projet__in=["Individuel", "En groupe"])
    context = {
        "setting": setting,
        "projets": projets
    }
    return render(request, "add_tg.html", context)


@login_required(login_url='connection/login')
def edit_tg(request, id):
    setting = get_setting()
    if setting is None:
        redirect("settings/maintenance")
    
    tache_id = int(dechiffrer_param(str(id)))     
    tache = get_object_or_404(Tache, id=tache_id)
    
    projets = Projet.objects.filter(type_projet__in=["Individuel", "En groupe"]).exclude(id=tache.projet.id)
    context = {
        "setting": setting,
        "tache": tache,
        "projets": projets
    }
    return render(request, "edit_tg.html", context)
   

@login_required(login_url='connection/login')
def edit_tache_g(request):
    if request.method == "POST":
        id = int(request.POST["id"])
        try:
            tache = get_object_or_404(Tache, id=id)
        except:
            tache = None
        
        if tache is None:
            return JsonResponse({
                    "status": "error",
                    "message": "Identifiant inexistant."})
        else:
            projet_id = request.POST["projet"]
            
            # Récuperer le projet
            projet = get_object_or_404(Projet, id=projet_id)
            if projet.type_projet == "Individuel":
                # Calculer le montant total des contributeurs
                total_montant_actionnaire = Contribution.objects.filter(projet_id=projet_id).aggregate(Sum('montant_contribution'))['montant_contribution__sum'] or 0
                cout_estime_enregistrer = total_montant_actionnaire + projet.montant_responsable
                if cout_estime_enregistrer < projet.cout_estime:
                    return JsonResponse({
                        "status": "error",
                        "message": "La contribution des actionnaires et du responsable du projet est inférieur au coût estimé du projet."})
            
            if projet.type_projet == "En groupe":
                # Calculer le montant total des acteurs
                total_montant_acteurs = Participation.objects.filter(projet_id=projet_id).aggregate(Sum('montant_participation'))['montant_participation__sum'] or 0
                cout_estime_enregistrer = total_montant_acteurs + projet.montant_responsable
                if cout_estime_enregistrer < projet.cout_estime:
                    return JsonResponse({
                        "status": "error",
                        "message": "La participation des acteurs et du responsable du projet est inférieur au coût estimé du projet."})
                
            
            # Se proteger de l'attaque XSS(Injection du code javascript)
            nom = bleach.clean(request.POST["nom"].strip())
            description = bleach.clean(request.POST["description"].strip())
            date_debut = bleach.clean(request.POST["date_debut"].strip())
            date_fin = bleach.clean(request.POST["date_fin"].strip())
            cout_estime = bleach.clean(request.POST["cout_estime"].strip())
            cout_reel = bleach.clean(request.POST["cout_reel"].strip())
            
            # Nettoyer la valeur (supprimer les espaces et remplacer la virgule par un point)
            cout_estime = re.sub(r'\xa0', '', cout_estime)  # Supprime les espaces insécables
            cout_estime = cout_estime.replace(" ", "").replace(",", ".")
            
            cout_reel = re.sub(r'\xa0', '', cout_reel)  # Supprime les espaces insécables
            cout_reel = cout_reel.replace(" ", "").replace(",", ".")

            try:
                cout_estime = Decimal(cout_estime)  # Convertir en Decimal
                cout_reel = Decimal(cout_reel)  # Convertir en Decimal
            except:
                return JsonResponse({
                    "status": "error",
                    "message": "Les coûts doivent être des nombres valides."})
            
            # Conversion de date string en date pour mieux faire la comparaison
            date_format = "%Y-%m-%d"
            date_d = datetime.strptime(date_debut, date_format).date()
            date_f = datetime.strptime(date_fin, date_format).date()
            
            # Verifier si la date de début et la date de fin de la tâche sont situées entre la date de début et la date de fin du projet
            if date_d >= projet.date_debut and date_f <= projet.date_fin:
                
                if date_debut > date_fin:
                    return JsonResponse({
                        "status": "error",
                        "message": "Date de début doit être supérieure à la date de fin"})
                
                #On exclut la tâche que l'on veut modifier
                taches = Tache.objects.exclude(id=id)
                tabTaches = []
                for tach in taches:
                    try:
                        if tach.projet.type_projet == "Individuel" or tach.projet.type_projet == "En groupe":
                            tabTaches.append(tach.nom)
                    except Exception as e:
                        pass
                #On verifie si cette tâche existe déjà
                if nom in tabTaches:
                    return JsonResponse({
                        "status": "error",
                        "message": "Cette tâche existe déjà."})
                else:
                    tache.projet_id = projet_id
                    tache.nom = nom
                    tache.description = description
                    tache.date_debut = date_debut
                    tache.date_fin = date_fin
                    tache.cout_estime = cout_estime
                    tache.cout_reel = cout_reel
                    tache.save()
                    return JsonResponse({
                        "status": "success",
                        "message": "Tâche modifiée avec succès."})
            else:
                return JsonResponse({
                    "status": "error",
                    "message": "La date de début et la date de fin d'une tâche doivent se situer entre la date de début et la date de fin du projet."})


@login_required(login_url='connection/login')
def del_tg(request, id):
    try:  
        tache_id = int(dechiffrer_param(str(id)))  
        tache = get_object_or_404(Tache, id=tache_id)
    except:
        tache = None
        
    if tache:
        tache.delete()
    return redirect("tache_p")


class tri_tache(View):
    def get(self, request, action, *args, **kwargs):
        setting = get_setting()
        user_id = request.user.id 
        
        taches_pojet = (Tache.objects.values("projet_id").annotate(nb_taches=Count("projet_id")))
        tabProjets = []
        for ta in taches_pojet:
            projet = Projet.objects.get(id=ta["projet_id"])
            if projet.type_projet == action:
                if request.user.is_superuser:
                    dic = {}
                    dic["projet"] = projet
                    tabTaches = []
                    taches = projet.taches.all()
                    for tache in taches:
                        dic_tache = {}
                        dic_tache["tache"] = tache
                        dic_tache["depenses"] = tache.depenses.all()
                        tabTaches.append(dic_tache)
                    dic["taches"] = tabTaches
                    tabProjets.append(dic)
                else:
                    # Verifier si l'utilisateur est un actionnaire ou un acteur du projet
                    contribution = Contribution.objects.filter(projet_id=projet.id, actionnaire_id=user_id)
                    participation = Participation.objects.filter(projet_id=projet.id, acteur_id=user_id)
                    if projet.responsable.id == user_id or contribution.exists() or participation.exists():
                        dic = {}
                        dic["projet"] = projet
                        tabTaches = []
                        taches = projet.taches.all()
                        for tache in taches:
                            dic_tache = {}
                            dic_tache["tache"] = tache
                            dic_tache["depenses"] = tache.depenses.all()
                            tabTaches.append(dic_tache)
                        dic["taches"] = tabTaches
                        tabProjets.append(dic)
                        
        paginator = Paginator(tabProjets, 10)
        num_page = request.GET.get('page')
        tabProjets = paginator.get_page(num_page)
    
        context = {
            "projets": tabProjets,
            "setting": setting
        }
        return render(request, "content_tache.html", context) 
    
def ajax_devise(request, projet_id):
    projet = get_object_or_404(Projet, id=projet_id)
    context = {
        "symbole": projet.devise.symbole
    }
    return render(request, "ajax_devise.html", context)

