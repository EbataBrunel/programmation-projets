# Importation des modules standards
import bleach
import re
# Importation des modules tiers
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import User 
from django.http import JsonResponse
from django.contrib import messages
from datetime import datetime, date
from django.db.models import Count
from .models import Setting
from projet.models import Projet
from tache.models import Tache

def get_setting():
    try:
        setting = Setting.objects.all().first()
    except Exception as e:
        setting = None

    return setting

@login_required(login_url='connection/login')
def setting(request):
    
    setting = get_setting()
    
    if setting is None:
        return redirect("settings/maintenance")
    else:
    
        if request.method == "POST":
            
            id = request.POST["id"]
            if id:                
                sett = Setting.objects.get(id=id)
                
                appname = bleach.clean(request.POST["appname"].strip())
                appeditor = bleach.clean(request.POST["appeditor"].strip())
                version = bleach.clean(request.POST["version"].strip())
                theme = request.POST["theme"].strip()
                text_color = request.POST["text_color"]
                email = request.POST["email"]
                
                #On verifie si l'adresse e-mail correspond bien
                regexp = r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$"
                if not re.search(regexp, email):
                    messages.error(request, "Le format de l'adresse e-mail ne correspond pas.")
                else:
                    
                    phone = bleach.clean(request.POST["phone"].strip())
                    logo = None
                    if request.POST.get('logo', True):
                        logo = request.FILES["logo"]
                    width = request.POST["width"].strip()
                    height = request.POST["height"].strip()

                    sett.appname = appname
                    sett.appeditor = appeditor
                    sett.version = version
                    sett.theme = theme
                    sett.text_color = text_color
                    sett.email = email
                    sett.phone = phone
                    if logo is not None:
                        sett.logo = logo
                    sett.width_logo = width
                    sett.height_logo = height

                    sett.save()
                    messages.success(request, "Paramètre modifié avec succès.")
                    return redirect("settings/setting")
            else:
                appname = bleach.clean(request.POST["appname"].strip())
                appeditor = bleach.clean(request.POST["appeditor"].strip())
                version = bleach.clean(request.POST["version"].strip())
                theme = request.POST["theme"]
                text_color = request.POST["text_color"]
                email = request.POST["email"]
                #On verifie si l'adresse e-mail correspond bien
                regexp = r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$"
                if not re.search(regexp, email):
                    messages.error(request, "Le format de l'adresse e-mail ne correspond pas.")
                else:
                    phone = bleach.clean(request.POST["phone"].strip())
                    logo = None
                    if request.POST.get('logo', True):
                            logo = request.FILES["logo"]
                    width = bleach.clean(request.POST["width"].strip())
                    height = bleach.clean(request.POST["height"].strip())

                    sett = Setting(
                        appname = appname,
                        appeditor = appeditor,
                        version = version,
                        theme = theme,
                        text_color = text_color,
                        email = email,
                        phone = phone,
                        logo = logo,
                        width_logo = width,
                        height_logo = height)
                    
                    sett.save()
                    messages.success(request, "Paramètre enregistré avec succès.")
                    return redirect("settings/setting")

        themes = ["bg-gradient-primary", "bg-gradient-info", "bg-gradient-success", "bg-gradient-warning", "bg-gradient-danger", "bg-gradient-secondary", "bg-gradient-dark"]
        context = {
            "setting": setting,
            "themes": themes
        }
        return render(request, "settings/setting.html",context)


def maintenance(request):   
    return render(request, "settings/maintenance.html")


@login_required(login_url='connection/login')
def index(request):   
    setting = get_setting()
    
    if setting is None:
        return redirect("settings/maintenance")
    
    tous_projets = Projet.objects.all()
    nb_total_projet = tous_projets.count()
    
    types_projets = (Projet.objects.values("type_projet").annotate(nb_projets=Count("type_projet")))
    tabTypeProjets = []
    n = 0
    for tp in types_projets:
        n += 1
        dic = {}
        dic["num_type"] = n
        dic["type_projet"] = tp["type_projet"]
        projets = Projet.objects.filter(type_projet=tp["type_projet"])
        dic["projets"] = projets
        dic["nb_projets"] = tp["nb_projets"]
        tabTypeProjets.append(dic)

    
    #Projet planifié
    nb_total_projet_planifie = Projet.objects.filter(statut="Planifié").count()
    projets_planifies = (Projet.objects.values("type_projet").filter(statut="Planifié").annotate(nb_projets=Count("type_projet")))
    tabProjetsPlanifies = []
    n = 0
    for tp in projets_planifies:
        n += 1
        dic = {}
        dic["num_type"] = n
        dic["type_projet"] = tp["type_projet"]
        projets = Projet.objects.filter(type_projet=tp["type_projet"], statut="Planifié")
        dic["projets"] = projets
        dic["nb_projets"] = tp["nb_projets"]
        tabProjetsPlanifies.append(dic)
    
    
    #Projet en cours
    nb_total_projet_encours = Projet.objects.filter(statut="En cours").count()
    projets_encours = (Projet.objects.values("type_projet").filter(statut="En cours").annotate(nb_projets=Count("type_projet")))
    tabProjetsEncours = []
    n = 0
    for tp in projets_encours:
        n += 1
        dic = {}
        dic["num_type"] = n
        dic["type_projet"] = tp["type_projet"]
        projets = Projet.objects.filter(type_projet=tp["type_projet"], statut="En cours")
        dic["projets"] = projets
        dic["nb_projets"] = tp["nb_projets"]
        tabProjetsEncours.append(dic)
    
    #Projet terminé
    nb_total_projet_termine = Projet.objects.filter(statut="Terminé").count()
    
    projets_termines = (Projet.objects.values("type_projet").filter(statut="Terminé").annotate(nb_projets=Count("type_projet")))
    tabProjetsTermines = []
    n = 0
    for tp in projets_termines:
        n += 1
        dic = {}
        dic["num_type"] = n
        dic["type_projet"] = tp["type_projet"]
        projets = Projet.objects.filter(type_projet=tp["type_projet"], statut="Terminé")
        dic["projets"] = projets
        dic["nb_projets"] = tp["nb_projets"]
        tabProjetsTermines.append(dic)
        
    context = {
        "tous_projets": tous_projets,
        "nb_total_projet": nb_total_projet,
        
        "types_projets": tabTypeProjets,
        
        "nb_total_projet_planifie": nb_total_projet_planifie,
        "projets_planifies": tabProjetsPlanifies,
        
        "nb_total_projet_encours": nb_total_projet_encours,
        "projets_encours": tabProjetsEncours,
        
        "nb_total_projet_termine": nb_total_projet_termine,
        "projets_termines": tabProjetsTermines,
        
        "pourcntage_planifie": int((nb_total_projet_planifie*100)/nb_total_projet),
        "pourcntage_encours": int((nb_total_projet_encours*100)/nb_total_projet),      
        "pourcntage_termine": int((nb_total_projet_termine*100)/nb_total_projet),
        
        "setting": setting,
        "fresh_dashbord": True
    }
    return render(request, "index.html", context)
    
    
# Mise à jour des status du projet et des taches
def update_satus_project_and_task(request):
    date_actuelle = date.today()
    projets = Projet.objects.all()
       
    for projet in projets:
            taches = Tache.objects.filter(projet_id=projet.id)
            nb_taches = taches.count()
            nb_tache_termine = 0
            nb_tache_encours = 0
            for tache in taches:
                if tache.date_debut < date_actuelle and  date_actuelle <= tache.date_fin:
                    tache.statut = "En cours"
                    tache.save()
                    nb_tache_encours += 1
                    
                if tache.date_fin < date_actuelle:
                    tache.statut = "Terminé"
                    tache.save()
                    nb_tache_termine += 1
                    
            if nb_taches > 0 and  nb_taches == nb_tache_termine:
                projet.statut = "Terminé"
                projet.save()
            else:
                projet.statut = "En cours"
                projet.save()
                 
        
    
    return JsonResponse({
        'status': 0
    })

            
        