# Importation des modules standard
import bleach
# Importation des modules tiers
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.views import View
# Importation des modules locaux
from eajc.views import get_setting 
from eajcprojet.utils.crypto import dechiffrer_param
from .models import*
from contribution.models import Contribution
from participation.models import Participation


#========================== Progrès du projet personnel ============================
@login_required(login_url='connection/login')
def progres_p(request):
    setting = get_setting()
    if setting is None:
        redirect("settings/maintenance")
        
    # Récupérer les détails de chaque tâche par projet :    
    progres_pojet = (Progres.objects.values("projet_id").annotate(nb_taches=Count("projet_id")))
    tabProjets = []
    nb_taches = 0
    for ta in progres_pojet:
        projet = Projet.objects.get(id=ta["projet_id"])
        if projet.type_projet == "Personnel" and projet.responsable.id == request.user.id:
            nb_taches += 1
            dic = {}
            dic["projet"] = projet
            dic["progres"] = projet.progres.all()
            #dic["nb_articles"] = ta["nb_articles"]
            tabProjets.append(dic)
            
    paginator = Paginator(tabProjets, 10)
    num_page = request.GET.get('page')
    tabProjets = paginator.get_page(num_page)

    context = {
        "projets": tabProjets,
        "setting": setting
    }
    return render(request, "progres_p.html", context)


@login_required(login_url='connection/login')
def add_prog_p(request):
    
    user_id = request.user.id
    setting = get_setting()
    if setting is None:
        redirect("settings/maintenance")
    
    if request.method == "POST":
        projet_id = request.POST["projet"]
        date_progres = bleach.clean(request.POST["date_progres"].strip())
        pourcentage = bleach.clean(request.POST["pourcentage"].strip())
        commentaire = bleach.clean(request.POST["commentaire"].strip())

        query = Progres.objects.filter(projet_id=projet_id, date_progres=date_progres)
        if query.exists():
            return JsonResponse({
                "status": "error",
                "message": "Ce progrès existe déjà"})
        else:
            progres = Progres(
                projet_id=projet_id,
                date_progres=date_progres, 
                pourcentage=pourcentage, 
                commentaire=commentaire)
            # Nombre de progrès avant l'ajout
            count0 = Progres.objects.all().count()
            progres.save()
            # Nombre de progres après l'ajout
            count1 = Progres.objects.all().count()
            # On verifie si l'insertion a eu lieu ou pas.
            if count0 < count1:
                return JsonResponse({
                    "status": "success",
                    "message": "Progrès enregistré avec succès."})
            else:
                return JsonResponse({
                    "status": "error",
                    "message": "L'opération a échoué."})

    projets = Projet.objects.filter(responsable_id=user_id, type_projet="Personnel")
    context = {
        "setting": setting,
        "projets": projets
    }
    return render(request, "add_prog_p.html", context)


@login_required(login_url='connection/login')
def edit_prog_p(request, id):
    user_id = request.user.id
    setting = get_setting()
    if setting is None:
        redirect("settings/maintenance")
    
    progres_id = int(dechiffrer_param(str(id)))    
    progres = get_object_or_404(Progres, id=progres_id)
    #On vérifie si ce membre est authorisé à acceder à cette page ou pas.
    projet = Projet.objects.get(id=progres.projet.id)
    if projet.responsable.id == user_id:
        projets = Projet.objects.filter(responsable_id=user_id).exclude(id=progres.projet.id)
        context = {
            "setting": setting,
            "progres": progres,
            "projets": projets
        }
        return render(request, "edit_prog_p.html", context)
    else:
        return redirect("authorization")

@login_required(login_url='connection/login')
def edit_pro_p(request):
    if request.method == "POST":
        id = int(request.POST["id"])
        try:
            progres = get_object_or_404(Progres, id=id)
        except:
            progres = None
        
        if progres is None:
            return JsonResponse({
                    "status": "error",
                    "message": "Identifiant inexistant."})
        else:
            projet_id = request.POST["projet"]
            # Se proteger de l'attaque XSS(Injection du code javascript)
            date_progres = bleach.clean(request.POST["date_progres"].strip())
            pourcentage = bleach.clean(request.POST["pourcentage"].strip())
            commentaire = bleach.clean(request.POST["commentaire"].strip())
            #On exclut le progrès que l'on veut modifier
            liste_progres = Progres.objects.exclude(id=id)
            tabProgres = []
            for prog in liste_progres:
                try:
                    if prog.projet.responsable.id == request.user.id:
                        tabProgres.append(prog)
                except Exception as e:
                    pass
            #On verifie si ce projet existe déjà
            
            x = False
            for p in tabProgres:
                if int(projet_id) == p.projet.id  and date_progres == p.date_progres:
                    x = True
            if x:
                return JsonResponse({
                    "status": "error",
                    "message": "Ce progrès existe déjà."})
            else:
                progres.projet_id = projet_id
                progres.date_progres = date_progres
                progres.pourcentage = pourcentage
                progres.commentaire = commentaire
                progres.save()
                return JsonResponse({
                    "status": "success",
                    "message": "Progrès modifié avec succès."})


@login_required(login_url='connection/login')
def del_prog_p(request, id):
    try:  
        progres_id = int(dechiffrer_param(str(id)))  
        progres = get_object_or_404(Progres, id=progres_id)
    except:
        progres = None
        
    if progres:
        progres.delete()
    return redirect("progres_p")


#========================== Progrès du projet en commun ============================
@login_required(login_url='connection/login')
def progres_g(request):
    setting = get_setting()
    if setting is None:
        redirect("settings/maintenance")
    
    user_id = request.user.id   
    # Récupérer les détails de chaque tâche par projet :    
    progres_projet = (Progres.objects.values("projet_id").annotate(nb_taches=Count("projet_id")))
    tabProjets = []
    for ta in progres_projet:
        projet = Projet.objects.get(id=ta["projet_id"])
        if projet.type_projet == "Individuel":
            if request.user.is_superuser:
                dic = {}
                dic["projet"] = projet
                dic["progres"] = projet.progres.all()
                tabProjets.append(dic)
                
            else:
                # Verifier si l'utilisateur est un actionnaire ou un acteur du projet
                contribution = Contribution.objects.filter(projet_id=projet.id, actionnaire_id=user_id)
                participation = Participation.objects.filter(projet_id=projet.id, acteur_id=user_id)
                if projet.responsable.id == user_id or contribution.exists() or participation.exists():
                    dic = {}
                    dic["projet"] = projet
                    dic["progres"] = projet.progres.all()
                    tabProjets.append(dic)
            
    paginator = Paginator(tabProjets, 10)
    num_page = request.GET.get('page')
    tabProjets = paginator.get_page(num_page)

    context = {
        "projets": tabProjets,
        "setting": setting
    }
    return render(request, "progres_g.html", context)


@login_required(login_url='connection/login')
def add_prog_g(request):
    
    setting = get_setting()
    if setting is None:
        redirect("settings/maintenance")
    
    if request.method == "POST":
        projet_id = request.POST["projet"]
        date_progres = bleach.clean(request.POST["date_progres"].strip())
        pourcentage = bleach.clean(request.POST["pourcentage"].strip())
        commentaire = bleach.clean(request.POST["commentaire"].strip())

        query = Progres.objects.filter(projet_id=projet_id, date_progres=date_progres)
        if query.exists():
            return JsonResponse({
                "status": "error",
                "message": "Ce progrès existe déjà"})
        else:
            progres = Progres(
                projet_id=projet_id,
                date_progres=date_progres, 
                pourcentage=pourcentage, 
                commentaire=commentaire)
            # Nombre de progrès avant l'ajout
            count0 = Progres.objects.all().count()
            progres.save()
            # Nombre de progres après l'ajout
            count1 = Progres.objects.all().count()
            # On verifie si l'insertion a eu lieu ou pas.
            if count0 < count1:
                return JsonResponse({
                    "status": "success",
                    "message": "Progrès enregistré avec succès."})
            else:
                return JsonResponse({
                    "status": "error",
                    "message": "L'opération a échoué."})

    projets = Projet.objects.filter(type_projet__in=["Individuel", "En groupe"])
    context = {
        "setting": setting,
        "projets": projets
    }
    return render(request, "add_prog_g.html", context)


@login_required(login_url='connection/login')
def edit_prog_g(request, id):
    setting = get_setting()
    if setting is None:
        redirect("settings/maintenance")
        
    progres_id = int(dechiffrer_param(str(id)))
    progres = get_object_or_404(Progres, id=progres_id)
    projets = Projet.objects.filter(type_projet__in=["Individuel", "En groupe"]).exclude(id=progres.projet.id)
    context = {
            "setting": setting,
            "progres": progres,
            "projets": projets
    }
    return render(request, "edit_prog_g.html", context)
    

@login_required(login_url='connection/login')
def edit_pro_g(request):
    if request.method == "POST":
        id = int(request.POST["id"])
        try:
            progres = get_object_or_404(Progres, id=id)
        except:
            progres = None
        
        if progres is None:
            return JsonResponse({
                    "status": "error",
                    "message": "Identifiant inexistant."})
        else:
            projet_id = request.POST["projet"]
            # Se proteger de l'attaque XSS(Injection du code javascript)
            date_progres = bleach.clean(request.POST["date_progres"].strip())
            pourcentage = bleach.clean(request.POST["pourcentage"].strip())
            commentaire = bleach.clean(request.POST["commentaire"].strip())
            #On exclut le progrès que l'on veut modifier
            liste_progres = Progres.objects.exclude(id=id)
            tabProgres = []
            for prog in liste_progres:
                try:
                    if prog.projet.type_projet == "Individuel" or prog.projet.type_projet == "En groupe":
                        tabProgres.append(prog)
                except Exception as e:
                    pass
            #On verifie si ce projet existe déjà
            
            x = False
            for p in tabProgres:
                if int(projet_id) == p.projet.id  and date_progres == p.date_progres:
                    x = True
            if x:
                return JsonResponse({
                    "status": "error",
                    "message": "Ce progrès existe déjà."})
            else:
                progres.projet_id = projet_id
                progres.date_progres = date_progres
                progres.pourcentage = pourcentage
                progres.commentaire = commentaire
                progres.save()
                return JsonResponse({
                    "status": "success",
                    "message": "Progrès modifié avec succès."})


@login_required(login_url='connection/login')
def del_prog_g(request,id):
    try:  
        progres_id = int(dechiffrer_param(str(id)))  
        progres = get_object_or_404(Progres, id=progres_id)
    except:
        progres = None
        
    if progres:
        progres.delete()
    return redirect("progres_g")

class tri_progres(View):
    def get(self, request, action, *args, **kwargs):
        setting = get_setting()
        progres_pojet = (Progres.objects.values("projet_id").annotate(nb_taches=Count("projet_id")))
        tabProjets = []
        for ta in progres_pojet:
            projet = Projet.objects.get(id=ta["projet_id"])
            if projet.type_projet == action:
                dic = {}
                dic["projet"] = projet
                dic["progres"] = projet.progres.all()
                tabProjets.append(dic)
                
        paginator = Paginator(tabProjets, 10)
        num_page = request.GET.get('page')
        tabProjets = paginator.get_page(num_page)
    
        context = {
            "projets": tabProjets,
            "setting": setting
        }
        return render(request, "content_progres.html", context) 

