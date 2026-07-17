# Importation des modules standards
import bleach
import re
import pdfkit
import base64
# Importation des modules tiers
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required 
from django.core.paginator import Paginator

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views import View
from decimal import Decimal

from django.http.response import HttpResponse
from django.template.loader import get_template
from django.contrib.sites.shortcuts import get_current_site

# Importation des modules locaux
from eajc.views import get_setting 
from eajcprojet.utils.crypto import dechiffrer_param
from .models import*
from .models import Projet
from contribution.models import Contribution
from participation.models import Participation


#=============================  Gestion du projet personnel ============================
@login_required(login_url='connection/login')
def proj_p(request):
    user_id = request.user.id
    setting = get_setting()
    if setting is None:
        redirect("settings/maintenance")
        
    liste_projets = Projet.objects.filter(responsable_id=user_id, type_projet="Personnel")
    projets = []
    for projet in liste_projets:
        dic = {}
        dic["projet"] = projet
        dic["taches"] = projet.taches.all()
        dic["depenses"] = projet.depenses.all()
        dic["progres"] = projet.progres.all()
        
        projets.append(dic)
        
    
    paginator = Paginator(projets, 10)
    num_page = request.GET.get('page')
    projets = paginator.get_page(num_page)
    
    context = {
        "projets": projets,
        "setting": setting
    }
    return render(request, 'proj_p.html', context)

@login_required(login_url='connection/login')
def add_pp(request):
    
    user_id = request.user.id
    setting = get_setting()
    if setting is None:
        redirect("settings/maintenance")
    
    if request.method == "POST":
        devise_id = request.POST["devise"]
        nom = bleach.clean(request.POST["nom"].strip())
        description = bleach.clean(request.POST["description"].strip())
        date_debut = bleach.clean(request.POST["date_debut"].strip())
        date_fin = bleach.clean(request.POST["date_fin"].strip())
        cout_estime = bleach.clean(request.POST["cout_estime"].strip())
        cout_reel = bleach.clean(request.POST["cout_reel"].strip())
        
        if date_debut > date_fin:
            return JsonResponse({
                "status": "error",
                "message": "La date de début doit être inférieure à la date de fin."})
        query = Projet.objects.filter(nom=nom, responsable_id=user_id)
        if query.exists():
            return JsonResponse({
                "status": "error",
                "message": "Ce projet existe déjà"})
        else:
            project = Projet(
                nom=nom, 
                description=description, 
                date_debut=date_debut, 
                date_fin=date_fin,
                cout_estime=cout_estime,
                cout_reel=cout_reel,
                responsable_id=user_id,
                devise_id=devise_id)
            # Nombre de projets avant l'ajout
            count0 = Projet.objects.all().count()
            project.save()
            # Nombre de projets après l'ajout
            count1 = Projet.objects.all().count()
            # On verifie si l'insertion a eu lieu ou pas.
            if count0 < count1:
                return JsonResponse({
                    "status": "success",
                    "message": "Projet enregistré avec succès."})
            else:
                return JsonResponse({
                    "status": "error",
                    "message": "L'opération a échoué."})
                
    devises = Devise.objects.all()
    context = {
        "setting": setting,
        "devises": devises
    }
    return render(request, "add_pp.html", context)


@login_required(login_url='connection/login')
def edit_pp(request, id):
    setting = get_setting()
    if setting is None:
        redirect("settings/maintenance")
    
    projet_id = int(dechiffrer_param(str(id)))   
    projet = get_object_or_404(Projet, id=projet_id)
    #On vérifie si ce membre est authorisé à acceder à cette page ou pas.
    query = Projet.objects.filter(id=projet_id, responsable_id=request.user.id)
    if query.exists():
        devises = Devise.objects.exclude(id=projet.devise.id)
        context = {
            "setting": setting,
            "projet": projet,
            "devises": devises
        }
        return render(request, "edit_pp.html", context)
    else:
        return redirect("authorization")

@login_required(login_url='connection/login')
def edit_proj_p(request):
    if request.method=="POST":
        id = int(request.POST["id"])
        try:
            projet = get_object_or_404(Projet, id=id)
        except:
            projet = None
        
        if projet is None:
            return JsonResponse({
                    "status": "error",
                    "message": "Identifiant inexistant."})
        else:
            # Se proteger de l'attaque XSS(Injection du code javascript)
            nom = bleach.clean(request.POST["nom"].strip())
            description = bleach.clean(request.POST["description"].strip())
            date_debut = bleach.clean(request.POST["date_debut"].strip())
            date_fin = bleach.clean(request.POST["date_fin"].strip())
            cout_estime = bleach.clean(request.POST["cout_estime"].strip())
            cout_reel = bleach.clean(request.POST["cout_reel"].strip())
            devise_id = request.POST["devise"]
            
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
            
            if date_debut >= date_fin:
                return JsonResponse({
                    "status": "error",
                    "message": "La date de début doit être inférieure à la date de fin."})
            
            #On exclut le projet que l'on veut modifier
            projects = Projet.objects.exclude(id=id)
            tabProjets = []
            for proj in projects:
                try:
                    if projet.responsable.id == request.user.id:
                        tabProjets.append(proj.nom)
                except Exception as e:
                    pass
            #On verifie si ce projet existe déjà
            if nom in tabProjets:
                return JsonResponse({
                    "status": "error",
                    "message": "Ce projet existe déjà."})
            else:
                projet.nom = nom
                projet.description = description
                projet.date_debut = date_debut
                projet.date_fin = date_fin
                projet.cout_estime = cout_estime
                projet.cout_reel = cout_reel
                projet.devise_id = devise_id
                projet.save()
                return JsonResponse({
                    "status": "success",
                    "message": "Projet modifié avec succès."})


@login_required(login_url='connection/login')
def del_pp(request, id):
    try:  
        projet_id = int(dechiffrer_param(str(id)))  
        projet = get_object_or_404(Projet, id=projet_id)
    except:
        projet = None
        
    if projet:
        projet.delete()
    return redirect("proj_p")

def liste_projets(request):
    projets = Projet.objects.all()
    return render(request, 'projets/liste_projets.html', {'projets': projets})

#=============================  Gestion du projet en commun ============================
@login_required(login_url='connection/login')
def proj_g(request):
    user_id = request.user.id
    setting = get_setting()
    if setting is None:
        redirect("settings/maintenance")
        
    liste_projets = Projet.objects.filter(type_projet="Individuel")
    
    projets = []
    for projet in liste_projets:
        if request.user.is_superuser:
            dic = {}
            dic["projet"] = projet
            dic["taches"] = projet.taches.all()
            dic["depenses"] = projet.depenses.all()
            dic["progres"] = projet.progres.all()
            dic["contributions"] = projet.contributions.all()
                
            projets.append(dic)
        else:
            # Verifier si l'utilisateur est un actionnaire du projet
            contribution = Contribution.objects.filter(projet_id=projet.id, actionnaire_id=user_id)
            if projet.responsable.id == user_id or contribution.exists():
                dic = {}
                dic["projet"] = projet
                dic["taches"] = projet.taches.all()
                dic["depenses"] = projet.depenses.all()
                dic["progres"] = projet.progres.all()
                dic["contributions"] = projet.contributions.all()
                
                projets.append(dic)
                
    paginator = Paginator(projets, 10)
    num_page = request.GET.get('page')
    projets = paginator.get_page(num_page)
    
    context = {
        "projets": projets,
        "setting": setting
    }
    return render(request, 'proj_g.html', context)

@login_required(login_url='connection/login')
def add_pg(request):
    
    user_id = request.user.id
    setting = get_setting()
    if setting is None:
        redirect("settings/maintenance")
    
    if request.method == "POST":
        nom = bleach.clean(request.POST["nom"].strip())
        description = bleach.clean(request.POST["description"].strip())
        date_debut = bleach.clean(request.POST["date_debut"].strip())
        date_fin = bleach.clean(request.POST["date_fin"].strip())
        cout_estime = bleach.clean(request.POST["cout_estime"].strip())
        cout_reel = bleach.clean(request.POST["cout_reel"].strip())
        type_projet = bleach.clean(request.POST["type_projet"].strip())
        responsable_id = bleach.clean(request.POST["responsable"].strip())
        montant_responsable = bleach.clean(request.POST["montant_responsable"].strip()) 
        devise_id = request.POST["devise"]
        
        if cout_estime < montant_responsable:
            return JsonResponse({
                "status": "error",
                "message": "Le montant du responsable ne peut pas être superieur au coût estimé."})
        
        if date_debut > date_fin:
            return JsonResponse({
                "status": "error",
                "message": "La date de début doit être inférieure à la date de fin."})
        query = Projet.objects.filter(nom=nom, responsable_id=user_id)
        if query.exists():
            return JsonResponse({
                "status": "error",
                "message": "Ce projet existe déjà"})
        else:
            project = Projet(
                nom=nom, 
                description=description, 
                date_debut=date_debut, 
                date_fin=date_fin,
                cout_estime=cout_estime,
                cout_reel=cout_reel,
                responsable_id=responsable_id,
                type_projet=type_projet,
                montant_responsable=montant_responsable,
                devise_id=devise_id)
            # Nombre de projets avant l'ajout
            count0 = Projet.objects.all().count()
            project.save()
            # Nombre de projets après l'ajout
            count1 = Projet.objects.all().count()
            # On verifie si l'insertion a eu lieu ou pas.
            if count0 < count1:
                return JsonResponse({
                    "status": "success",
                    "message": "Projet enregistré avec succès."})
            else:
                return JsonResponse({
                    "status": "error",
                    "message": "L'opération a échoué."})

    responsables = User.objects.all()
    devises = Devise.objects.all()
    context = {
        "setting": setting,
        "responsables": responsables,
        "devises": devises
    }
    return render(request, "add_pg.html", context)

@login_required(login_url='connection/login')
def edit_pg(request, id):
    setting = get_setting()
    if setting is None:
        redirect("settings/maintenance")
    
    projet_id = int(dechiffrer_param(str(id)))    
    projet = get_object_or_404(Projet, id=projet_id)
    
    responsables = User.objects.exclude(id=projet.responsable.id)
    devises = Devise.objects.exclude(id=projet.devise.id)
    context = {
            "setting": setting,
            "projet": projet,
            "responsables": responsables,
            "devises": devises
    }
    return render(request, "edit_pg.html", context)
    

@login_required(login_url='connection/login')
def edit_proj_g(request):
    if request.method=="POST":
        id = int(request.POST["id"])
        try:
            projet = get_object_or_404(Projet, id=id)
        except:
            projet = None
        
        if projet is None:
            return JsonResponse({
                    "status": "error",
                    "message": "Identifiant inexistant."})
        else:
            # Se proteger de l'attaque XSS(Injection du code javascript)
            nom = bleach.clean(request.POST["nom"].strip())
            description = bleach.clean(request.POST["description"].strip())
            date_debut = bleach.clean(request.POST["date_debut"].strip())
            date_fin = bleach.clean(request.POST["date_fin"].strip())
            cout_estime = bleach.clean(request.POST["cout_estime"].strip())
            cout_reel = bleach.clean(request.POST["cout_reel"].strip())
            type_projet = bleach.clean(request.POST["type_projet"].strip())
            responsable_id = bleach.clean(request.POST["responsable"].strip())
            montant_responsable = bleach.clean(request.POST.get("montant_responsable", "").strip())
            devise_id = request.POST["devise"]
            
            if cout_estime < montant_responsable:
                return JsonResponse({
                    "status": "error",
                    "message": "Le montant du responsable ne peut pas être superieur au coût estimé."})
            
            # Nettoyer la valeur (supprimer les espaces et remplacer la virgule par un point)
            cout_estime = re.sub(r'\xa0', '', cout_estime)  # Supprime les espaces insécables
            cout_estime = cout_estime.replace(" ", "").replace(",", ".")
            
            cout_reel = re.sub(r'\xa0', '', cout_reel)  # Supprime les espaces insécables
            cout_reel = cout_reel.replace(" ", "").replace(",", ".")
            
            montant_responsable = re.sub(r'\xa0', '', montant_responsable)  # Supprime les espaces insécables
            montant_responsable = montant_responsable.replace(" ", "").replace(",", ".")

            try:
                montant = Decimal(montant_responsable)  # Convertir en Decimal
                cout_estime= Decimal(cout_estime)  # Convertir en Decimal
                cout_reel = Decimal(cout_reel)  # Convertir en Decimal
            except:
                return JsonResponse({
                    "status": "error",
                    "message": "Le montant et les coûts doivent être des nombres valides."})
                
            if date_debut >= date_fin:
                return JsonResponse({
                    "status": "error",
                    "message": "La date de début doit être inférieure à la date de fin."})
            
            #On exclut le projet que l'on veut modifier
            projects = Projet.objects.exclude(id=id)
            tabProjets = []
            for proj in projects:
                try:
                    if projet.responsable.id == request.user.id:
                        tabProjets.append(proj.nom)
                except Exception as e:
                    pass
            #On verifie si ce projet existe déjà
            if nom in tabProjets:
                return JsonResponse({
                    "status": "error",
                    "message": "Ce projet existe déjà."})
            else:
                projet.nom = nom
                projet.description = description
                projet.date_debut = date_debut
                projet.date_fin = date_fin
                projet.cout_estime = cout_estime
                projet.cout_reel = cout_reel
                projet.type_projet = type_projet
                projet.responsable_id = responsable_id
                projet.montant_responsable = montant
                projet.devise_id = devise_id
                projet.save()
                return JsonResponse({
                    "status": "success",
                    "message": "Projet modifié avec succès."})
                
@login_required(login_url='connection/login')
def del_pg(request, id):
    try: 
        projet_id = int(dechiffrer_param(str(id)))   
        projet = get_object_or_404(Projet, id=projet_id)
    except:
        projet = None
        
    if projet:
        projet.delete()
    return redirect("proj_g")


class tri_projet(View):
    def get(self, request, action, *args, **kwargs):
        setting = get_setting()
        liste_projets = Projet.objects.filter(type_projet=action)
        
        user_id = request.user.id
        projets = []
        for projet in liste_projets:
            if request.user.is_superuser:
                dic = {}
                dic["projet"] = projet
                dic["taches"] = projet.taches.all()
                dic["depenses"] = projet.depenses.all()
                dic["progres"] = projet.progres.all()
                dic["contributions"] = projet.contributions.all()
                dic["participations"] = projet.participations.all()
                
                projets.append(dic)
            else:
                # Verifier si l'utilisateur est un actionnaire ou un acteur du projet
                contribution = Contribution.objects.filter(projet_id=projet.id, actionnaire_id=user_id)
                participation = Participation.objects.filter(projet_id=projet.id, acteur_id=user_id)
                if projet.responsable.id == user_id or contribution.exists() or participation.exists():
                    dic = {}
                    dic["projet"] = projet
                    dic["taches"] = projet.taches.all()
                    dic["depenses"] = projet.depenses.all()
                    dic["progres"] = projet.progres.all()
                    dic["contributions"] = projet.contributions.all()
                    
                    projets.append(dic)
        
        paginator = Paginator(projets, 10)
        num_page = request.GET.get('page')
        projets = paginator.get_page(num_page)
    
        context = {
            "projets": projets,
            "setting": setting
        }
        return render(request, "content_projet.html", context) 


@login_required(login_url='connection/login')
def document_projet(request, projet_id):
    setting = get_setting()
    projet = get_object_or_404(Projet, id=projet_id)
    
    contributions = projet.contributions.all()
    participations = projet.participations.all()
    taches = projet.taches.all()
    depenses = projet.depenses.all()
    progres = projet.progres.all()
    
    # Chemin vers notre image
    image_path = setting.logo

    # Lire l'image en mode binaire et encoder en Base64
    base64_string = base64.b64encode(image_path.read()).decode('utf-8')

    context = {
        "base64_image": base64_string,
        "setting": setting,
        "contributions":contributions,
        "participations":participations,
        "projet": projet,
        "taches": taches,
        "depenses": depenses,
        "progres": progres,
        
        'domain':get_current_site(request).domain
    }
    template = get_template("document_projet.html")
    html = template.render(context)
    options = {
        'page-size': 'Letter',
        'encoding': "UTF-8",
    }
    pdf = pdfkit.from_string(html, False, options)
    reponse = HttpResponse(pdf, content_type='application/pdf')
    reponse['Content-Disposition'] = f"attachment; filename=Projet_{projet.responsable.last_name }_{ projet.responsable.first_name }.pdf"
    return reponse

@login_required(login_url='connection/login')
def document_projet_partage(request, projet_id):
    setting = get_setting()
    projet = get_object_or_404(Projet, id=projet_id)
    
    contributions = projet.contributions.all()
    participations = projet.participations.all()
    taches = projet.taches.all()
    depenses = projet.depenses.all()
    progres = projet.progres.all()
    
    # Chemin vers notre image
    image_path = setting.logo

    # Lire l'image en mode binaire et encoder en Base64
    base64_string = base64.b64encode(image_path.read()).decode('utf-8')

    context = {
        "base64_image": base64_string,
        "setting": setting,
        "contributions":contributions,
        "participations":participations,
        "projet": projet,
        "taches": taches,
        "depenses": depenses,
        "progres": progres,
        
        'domain':get_current_site(request).domain
    }
    template = get_template("document_projet_partage.html")
    html = template.render(context)
    options = {
        'page-size': 'Letter',
        'encoding': "UTF-8",
    }
    pdf = pdfkit.from_string(html, False, options)
    reponse = HttpResponse(pdf, content_type='application/pdf')
    reponse['Content-Disposition'] = f"attachment; filename=Projet_{projet.responsable.last_name }_{ projet.responsable.first_name }.pdf"
    return reponse

def configuration(request): 
    setting = get_setting()
    
    if setting is None:
        return redirect("settings/maintenance")
    
    liste_projets = Projet.objects.filter(type_projet="Personnel", statut="Terminé", responsable_id=request.user.id)
    projets = []
    for projet in liste_projets:
        dic = {}
        dic["projet"] = projet
        dic["taches"] = projet.taches.all()
        dic["depenses"] = projet.depenses.all()
        dic["progres"] = projet.progres.all()
        projets.append(dic)
        
    context = {
        "setting": setting,
        "projets": projets
    } 
    return render(request, "configuration.html", context)

def  visibilite_projet(request, id): 
    projet = get_object_or_404(Projet, id=id)
    
    if projet.visibilite_projet:
        projet.visibilite_projet = False
    else:
        projet.visibilite_projet = True
        
    projet.visibilite_tache = False
    projet.visibilite_depense = False
    projet.visibilite_progres = False
    
    projet.save()
        
    return redirect("configuration")

def  visibilite_tache(request, id): 
    projet = get_object_or_404(Projet, id=id)
    
    if projet.visibilite_projet:
        if projet.visibilite_tache:
            projet.visibilite_tache = False
        else:
            projet.visibilite_tache = True
        
        projet.save()
    context = {"projet": projet}
        
    return render(request, "visibilite_tache.html", context)

def  visibilite_depense(request, id): 
    projet = get_object_or_404(Projet, id=id)
    
    if projet.visibilite_projet:
        
        if projet.visibilite_depense:
            projet.visibilite_depense = False
        else:
            projet.visibilite_depense = True
        
        projet.save()
    
    context = {"projet": projet}
        
    return render(request, "visibilite_depense.html", context)

def  visibilite_progres(request, id): 
    projet = get_object_or_404(Projet, id=id)
    
    if projet.visibilite_projet:
        
        if projet.visibilite_progres:
            projet.visibilite_progres = False
        else:
            projet.visibilite_progres = True
          
        projet.save()
    
    context = {"projet": projet}
        
    return render(request, "visibilite_progres.html", context)


@login_required(login_url='connection/login')
def proj_perso_partage(request):
    user_id = request.user.id
    setting = get_setting()
    if setting is None:
        redirect("settings/maintenance")
        
    liste_projets = Projet.objects.filter(type_projet="Personnel", statut="Terminé", visibilite_projet=True)
    projets = []
    for projet in liste_projets:
        if projet.responsable.id != user_id:
            dic = {}
            dic["projet"] = projet
            dic["taches"] = projet.taches.all()
            dic["depenses"] = projet.depenses.all()
            dic["progres"] = projet.progres.all()
            
            projets.append(dic)
        
    
    paginator = Paginator(projets, 10)
    num_page = request.GET.get('page')
    projets = paginator.get_page(num_page)
    
    context = {
        "projets": projets,
        "setting": setting
    }
    return render(request, 'proj_perso_partage.html', context)

