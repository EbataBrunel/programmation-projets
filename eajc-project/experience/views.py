# Importation des modules standards
import datetime
import bleach
# Importation des modules tiers
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
# Importation des modules locaux
from eab.views import nbnew_answer, nbnew_message, new_message, parametre
from .models import*

from eajc.utils.crypto import dechiffrer_param


#=================== Gestion de l'experience ======================
@login_required(login_url='connection/login')
def experiences(request):
    date = datetime.datetime.now()

    all_experiences = Experience.objects.filter(user_id=request.user.id).select_related('entreprise')
    experiences = []
    for experience in all_experiences:
        dic = {}
        dic["experience"] = experience
        dic["taches"] = eval(experience.tache)
        experiences.append(dic)

    context = {
        "experiences":experiences,
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request),
        "parametre":parametre(),
        "date":date
    }
    return render(request, "experiences.html", context)

def ajax_detail_experience(request, id):
    experience = Experience.objects.get(id=id)
    
    experiences = []
    dic = {}
    dic["experience"] = experience
    dic["taches"] = eval(experience.tache)
    experiences.append(dic)
    
    context = {
        "experience": experience,
        "experiences":  experiences,
        "taches": eval(experience.tache)
    }
    return render(request, "ajax_detail_experience.html", context)

@login_required(login_url='connection/login')
@csrf_exempt
def add_exp(request):
    date = datetime.datetime.now()

    if request.method == "POST":
        type_exp = request.POST["type_exp"]        
        projet = bleach.clean(request.POST["projet"].strip())
        lien = bleach.clean(request.POST["lien"].strip())
        
        if type_exp in ["Projet", "Autre type d'expérience"]:
                query = Experience.objects.filter(
                    type_exp=type_exp,
                    projet=projet,
                    user_id=request.user.id)
                # Verifier l'existence de l'expérience
                if query.exists():
                    return JsonResponse({
                            "status": "error",
                            "message": "Cette expérience existe déjà."})
                else:
                    tache = {}
                    for i in range(10):
                            task = "tache"+str(i)
                            t = request.POST.get(task, True)
                            if t == True :
                                pass
                            else:
                                tache[i] = bleach.clean(t.strip())
                                
                    type_experience = ""           
                    if type_exp == "Autre type d'expérience":
                        autre_type_exp = bleach.clean(request.POST["autre_type_exp"])
                        type_experience = autre_type_exp 
                    else:
                        type_experience = type_exp

                    experience = Experience(
                            type_exp = type_experience,
                            projet = projet,
                            tache = tache,
                            user_id = request.user.id,
                            lien = lien
                    )
                    count0 = Experience.objects.all().count()
                    experience.save()
                    count1 = Experience.objects.all().count()
                    # Verifier si l'ajout a été bien enregistré 
                    if count0 < count1:
                        return JsonResponse({
                            "status": "success",
                            "message": "Expérience enregistrée avec succès."})
                    else:
                        return JsonResponse({
                            "status": "error",
                            "message": "L'insertion a échouée."})
        else:
            entreprise = request.POST["entreprise"]
            date_debut = request.POST["date_debut"]
            date_fin = request.POST["date_fin"]
            # La date du debut doit être inférieure à la date de fin
            if date_debut > date_fin:
                return JsonResponse({
                    "status": "error",
                    "message": "La date du début doit être inférieure à celle de fin."})
            else:
                
                posteoccupe = bleach.clean(request.POST["posteoccupe"].strip())
                # Verifier l'existance de l'expérience
                query = Experience.objects.filter(date_debut=date_debut, date_fin=date_fin, user_id=request.user.id)
                if query.exists():
                    return JsonResponse({
                            "status": "error",
                            "message": "Cette expérience existe déjà."})
                else:
                    tache = {}
                    for i in range(10):
                        task="tache"+str(i)
                        t=request.POST.get(task, True)
                        if t == True :
                            pass
                        else:
                            tache[i] = bleach.clean(t.strip())

                    projet = bleach.clean(request.POST["projet"].strip())           
                    experience = Experience(
                            type_exp = type_exp,
                            posteoccupe = posteoccupe,
                            projet = projet,
                            tache = tache,
                            date_debut = date_debut,
                            date_fin = date_fin,
                            entreprise_id = entreprise,
                            user_id = request.user.id,
                            lien = lien
                        )
                    count0 = Experience.objects.all().count()
                    experience.save()
                    count1 = Experience.objects.all().count()
                    # Verifier si l'ajout a été bien enregistré 
                    if count0 < count1:
                        return JsonResponse({
                            "status": "success",
                            "message": "Expérience enregistrée avec succès."})
                    else:
                        return JsonResponse({
                            "status": "error",
                            "message": "L'insertion a échouée."})

    type_experiences = ["Employé(e)", "Stagiaire", "Alternance", "Projet", "Autre type d'expérience"]
    context = {
        "type_experiences":type_experiences,
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request),
        "parametre":parametre(),
        "date":date
    }
    return render(request, "add_exp.html", context)

@login_required(login_url='connection/login')
def edit_exp(request, id):
    date = datetime.datetime.now()
    
    experience_id = dechiffrer_param(str(id))
    
    experience = Experience.objects.get(id=experience_id)
    entreprises = Entreprise.objects.filter(user_id=request.user.id)
    status = 0
    if experience.type_exp in ["Employé(e)", "Stagiaire", "Alternance"]:
        status = 1

    #On vérifie si ce membre est authorisé à acceder à cette page ou pas.
    query = Experience.objects.filter(id=experience_id ,user_id=request.user.id)
    if query.exists():
        taches = eval(experience.tache)
        # Création de la session type_experience pour cacher ou afficher le formulaire
        request.session['type_exp'] = experience.type_exp
        
        type_experiences = ["Employé(e)", "Stagiaire", "Alternance", "Projet", "Autre type d'expérience"]
        new_type_experiences = []
        for type_experience in type_experiences:
            if experience.type_exp != type_experience:
                new_type_experiences.append(type_experience)
            
        context = {
                "status":status,
                "experience":experience,
                "entreprises":entreprises,
                "taches":taches,
                "type_experiences":new_type_experiences,
                "countanswer":nbnew_answer(request),
                "count":nbnew_message(request),
                "users":new_message(request),
                "parametre":parametre(),
                "date":date
            }
        return render(request, "edit_exp.html", context)
    else:
        return redirect("authorization")

@login_required(login_url='connection/login')
@csrf_exempt
def edit_ex(request):
    if request.method == "POST":
        id = int(request.POST["id"])
        try:
            experience = Experience.objects.get(id=id)
        except:
            experience = None
        
        if experience == None:
            return JsonResponse({
                "status": "error",
                "message": "Identifiant inexistant."})
        else:
            type_exp = request.POST["type_exp"]
            projet = bleach.clean(request.POST["projet"].strip())
            lien = bleach.clean(request.POST["lien"].strip())
            
            if type_exp in ["Employé(e)", "Stagiaire", "Alternance"]:
                posteoccupe = bleach.clean(request.POST["posteoccupe"].strip())
                entreprise = request.POST["entreprise"]
                date_debut = request.POST["date_debut"]
                date_fin = request.POST["date_fin"]
                if date_debut > date_fin:
                    return JsonResponse({
                        "status": "error",
                        "message": "La date du début doit être inférieure à celle de fin."})
                else:
                    #On verifie si l'experience avec les dates renseignées a été déjà enregistrée
                    query = Experience.objects.filter(
                        date_debut=date_debut,date_fin=date_fin,user_id=request.user.id
                    ).exclude(id=id)    
                    if query.exists():
                        return JsonResponse({
                            "status": "error",
                            "message": "Cette expérience existe déjà."})
                    else:
                        tache = {}
                        for i in range(10):
                            task = "tache"+str(i)
                            t = request.POST.get(task, True)
                            if t == True :
                                pass
                            else:
                                tache[i]=bleach.clean(t.strip())
                                

                        experience.type_exp = type_exp
                        experience.posteoccupe = posteoccupe
                        experience.projet = projet
                        experience.tache = tache
                        experience.date_debut = date_debut
                        experience.date_fin = date_fin
                        experience.entreprise_id = entreprise
                        experience.lien = lien

                        experience.save()
                        return JsonResponse({
                            "status": "success",
                            "message": "Expérience modifiée avec succès."})
            else:
                    # Verifier l'existence de l'experience des dates renseignées
                    query = Experience.objects.filter(projet=projet, user_id=request.user.id).exclude(id=id)    
                    if query.exists():
                        return JsonResponse({
                            "status": "error",
                            "message": "Cette expérience existe déjà."})
                    else:
                        tache = {}
                        for i in range(10):
                            task = "tache"+str(i)
                            t = request.POST.get(task, True)
                            if t == True :
                                pass
                            else:
                                tache[i] = bleach.clean(t.strip())

                            projet = bleach.clean(request.POST["projet"].strip())
                            
                        type_experience = ""           
                        if type_exp == "Autre type d'expérience":
                            autre_type_exp = bleach.clean(request.POST["autre_type_exp"])
                            type_experience = autre_type_exp 
                        else:
                            type_experience = type_exp

                        experience.type_exp = type_experience
                        experience.posteoccupe = ''
                        experience.projet = projet
                        experience.tache = tache
                        experience.date_debut = None
                        experience.date_fin = None
                        experience.entreprise_id = None
                        experience.lien = lien

                        experience.save()
                        return JsonResponse({
                            "status": "success",
                            "message": "Expérience modifiée avec succès."})
                        
def ajax_delete_experience(request, id):
    experience = Experience.objects.get(id=id)
    context = {
        "experience": experience
    }
    return render(request, "ajax_delete_experience.html", context)

@login_required(login_url='connection/login')
def del_exp(request,id):
    try:
        experience_id = dechiffrer_param(str(id))
        experience = Experience.objects.get(id=experience_id)
    except:
        experience = None
        
    if experience and experience.user.id == request.user.id:
        experience.delete()
        
    return redirect("experiences")

class statexp(View):
    def get(self, request, id, *args, **kwargs):
        experience = Experience.objects.get(id=id)
        if experience.status == 0:
            experience.status = 1
        else:
            experience.status = 0
        experience.save()
        context = {"experience":experience}
        return render(request, "statexp.html", context)
    
class getFormExperience(View):
    def get(self, request, id, *args, **kwargs):
        
        type_exp = id
        status = 0
        if type_exp in ["Employé(e)", "Stagiaire", "Alternance"]:
            status = 1
        experience = None
        context = {
            "experience":experience,
            "status":status
        }
        # Destruction de la session
        if 'type_exp' in request.session:
            del request.session['type_exp']
        return render(request, "ajax.html", context)
    
class getFormExperienceDate(View):
    def get(self, request, id, *args, **kwargs):
        
        type_exp = id
        status = 0
        if type_exp in ["Employé(e)", "Stagiaire", "Alternance"]:
            status = 1
            
        entreprises = Entreprise.objects.filter(user_id=request.user.id)
        
        context = {
            "type_exp":type_exp,
            "entreprises":entreprises,
            "status":status
        }
        return render(request, "ajaxdate.html", context)

class getFormExperienceEdit(View):
    def get(self, request, id, code, *args, **kwargs):
        type_exp = id
        experience = Experience.objects.get(id=code) 
        taches = eval(experience.tache)
        status = 0
        if type_exp in ["Employé(e)", "Stagiaire", "Alternance"]:
            status = 1
        
        # Création de la session type_experience pour cacher ou afficher le formulaire
        request.session['type_exp'] = experience.type_exp
           
        context = {
            "experience":experience,
            "taches":taches,
            "status":status
        }
        return render(request, "ajax.html", context)
    
class getFormExperienceEditDate(View):
    def get(self, request, id, code, *args, **kwargs):
        
        type_exp = id
        status = 0
        experience=Experience.objects.get(id=code) 
        if type_exp in ["Employé(e)", "Stagiaire", "Alternance"]:
            status = 1
        
        entreprises = Entreprise.objects.filter(user_id=request.user.id)
        # Création de la session type_experience pour cacher ou afficher le formulaire
        request.session['type_exp'] = type_exp 
        context = {
            "experience":experience,
            "entreprises":entreprises,
            "type_exp":type_exp,
            "status":status
        }
        return render(request, "ajaxdate.html", context)