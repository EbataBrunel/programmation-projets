# Importation des modules standards
import datetime
import bleach
# Importation des modules tiers 
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from django.views import View
# Importation des modules locaux
from eab.views import nbnew_answer, nbnew_message, new_message, parametre
from .models import*
from eajc.utils.crypto import dechiffrer_param, chiffrer_param


##======================== Gestion de competences==============================
@login_required(login_url='connection/login')
def competences(request):
    date = datetime.datetime.now()

    competences = Competence.objects.values("type_competence_id").filter(user_id=request.user.id).annotate(effectif=Count("type_competence_id"))
    tabCompetences = []
    i = 0 # On crée cette valeur pour supprimer les compétences par type
    for competence in competences:
        competenceActif = Competence.objects.values("type_competence_id").filter(type_competence_id=competence["type_competence_id"],user_id=request.user.id,status=1).annotate(effectif=Count("type_competence_id"))
        competenceNoActif = Competence.objects.values("type_competence_id").filter(type_competence_id=competence["type_competence_id"],user_id=request.user.id,status=0).annotate(effectif=Count("type_competence_id"))
        
        countActif = 0
        for comp in competenceActif:
            countActif += comp["effectif"]
        
        countNoActif = 0
        for comp in competenceNoActif:
            countNoActif += comp["effectif"]
            
        # Récuperer le type de compétence
        type_competence = TypeCompetence.objects.get(id=competence["type_competence_id"])
        tab = {}
        tab["type_comp"] = type_competence
        tab["effectif"] = competence["effectif"]
        tab["active"] = countActif
        tab["noactive"] = countNoActif
        tabCompetences.append(tab)

    context = {
        "competences":tabCompetences,
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request),
        "parametre":parametre(),
        "date":date
    }
    return render(request, "competences.html",context)


@login_required(login_url='connection/login')
@csrf_exempt
def add_comp(request):
    date = datetime.datetime.now()

    if request.method == "POST":
        type_comp = request.POST["type_comp"]
        name = bleach.clean(request.POST["name"].strip())
        comment = bleach.clean(request.POST["comment"].strip())
        
        query = Competence.objects.filter(name=name, user_id=request.user.id)
        # Existence de la compétence
        if query.exists():
            return JsonResponse({
                "status": "error",
                "message": "Cette compétence existe déjà."})
        else:
            competence = Competence(type_competence_id=type_comp, name=name, comment=comment, user_id=request.user.id)
            count0 = Competence.objects.all().count()
            competence.save()
            count1 = Competence.objects.all().count()
            # Verifier si l'ajout a été bien effectué
            if count0 < count1:
                return JsonResponse({
                    "status": "success",
                    "message": "Compétence enregistrée avec succès."})
            else:
                return JsonResponse({
                    "status": "error",
                    "message": "L'insertion à echouée."})
            
    type_competences = TypeCompetence.objects.filter(user_id=request.user.id).order_by("name")
    context = {
        "type_competences": type_competences,
        "countanswer": nbnew_answer(request),
        "count": nbnew_message(request),
        "users": new_message(request),
        "parametre": parametre(),
        "date": date
    }
    return render(request, "add_comp.html", context)

def ajax_delete_competence(request, id):
    competence = Competence.objects.get(id=id)
    context = {
        "competence": competence
    }
    return render(request, "ajax_delete_competence.html", context)

@login_required(login_url='connection/login')
def del_comp(request, id):
    try:
        competence_id = int(dechiffrer_param(str(id)))
        competence = Competence.objects.get(id=competence_id)
    except:
        competence = None
        
    if competence and competence.user.id == request.user.id:
        competence.delete()
    return redirect("details_comp", id=chiffrer_param(str(competence.type_competence.id)))

def ajax_delete_multiple_competence(request, id):
    
    type_competence = TypeCompetence.objects.get(id=id)
    context = {
        "type_competence": type_competence
    }
    return render(request, "ajax_delete_multiple_competence.html", context)

@login_required(login_url='connection/login')
def delete_comp(request,id):
    type_competence_id = dechiffrer_param(str(id))
    competences = Competence.objects.filter(
        type_competence_id=type_competence_id, 
        user_id=request.user.id
    )
    # Supprimer toutes les compétences d'un type de compétence
    competences.delete()
    return redirect("competences")

@login_required(login_url='connection/login')
def details_comp(request, id):
    date = datetime.datetime.now()
    
    
    type_competence_id = int(dechiffrer_param(str(id)))
    competences = Competence.objects.filter(
        type_competence_id=type_competence_id, 
        user_id=request.user.id)
    
    # Récuperer le type de compétence
    type_competence = TypeCompetence.objects.get(id=type_competence_id)
    context = {
        "type_competence":type_competence,
        "competences":competences,
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request),
        "parametre":parametre(),
        "date":date
    }
    return render(request, "details_comp.html",context)

@login_required(login_url='connection/login')
def edit_comp(request, id):
    date = datetime.datetime.now()
    competence_id = int(dechiffrer_param(str(id)))
    competence = Competence.objects.get(id=competence_id)
    #On vérifie si ce membre est authorisé à acceder à cette page ou pas.
    query = Competence.objects.filter(id=competence_id,user_id=request.user.id)
    if query.exists():
        
        comments = ["Maternelle", "Courant", "Débutant", "Intermediaire", "Avancé"]
        tabComments = []
        for comment in comments:
            if competence.comment != comment:
                tabComments.append(comment)
                
        type_competences = TypeCompetence.objects.filter(user_id=request.user.id).order_by("name")
        tabType_competences = []
        for type_comp in type_competences:
            if type_comp.id != competence.type_competence.id:
                tabType_competences.append(type_comp)
                
        context = {
            "competence": competence,
            "comments": tabComments,
            "type_competences": tabType_competences,
            "countanswer": nbnew_answer(request),
            "count": nbnew_message(request),
            "users": new_message(request),
            "parametre": parametre(),
            "date": date
        }
        return render(request, "edit_comp.html", context)
    else:
        return redirect("authorization")

@login_required(login_url='connection/login')
@csrf_exempt
def edit_cmp(request):
    if request.method == "POST":
        id = int(request.POST["id"])
        try:
            competence = Competence.objects.get(id=id)
        except:
            competence = None
        
        if competence == None:
            return JsonResponse({
                "status": "error",
                "message": "Identifiant inexistant."})
        else:
            type_comp = request.POST["type_comp"]
            name = bleach.clean(request.POST["name"].strip())
            comment = bleach.clean(request.POST["comment"].strip())
            #On exclut la compétence que l'on veut modifier et on recupère les autres
            competences = Competence.objects.exclude(id=id)
            tabCompetence = []
            for comp in competences:
                try:
                    if comp.user.id == request.user.id:
                        tabCompetence.append(comp.name)
                except Exception as e:
                    pass
            #On verifie si cette compétence existe déjà
            if name in tabCompetence:
                return JsonResponse({
                    "status": "error",
                    "message": "Cette compétence existe déjà."})
            else:
                competence.type_competence_id = type_comp
                competence.name = name
                competence.comment = comment
                competence.save()
                return JsonResponse({
                    "status": "success",
                    "message": "Compétence enregistrée avec succès."})


class statcomp(View):
    def get(self, request, id, *args, **kwargs):
        competence = Competence.objects.get(id=id)
        if competence.status == 0:
            competence.status = 1
        else:
            competence.status = 0
        competence.save()

        context={"competence":competence}
        return render(request, "statcomp.html", context)

class fetchcomp(View):
    def get(self, request, id, *args, **kwargs):

        competenceActif = Competence.objects.values("type_competence_id").filter(type_competence_id=id,user_id=request.user.id,status=1).annotate(effectif=Count("type_competence_id"))
        competenceNoActif = Competence.objects.values("type_competence_id").filter(type_competence_id=id,user_id=request.user.id,status=0).annotate(effectif=Count("type_competence_id"))
        
        countActif = 0
        for comp in competenceActif:
            countActif += comp["effectif"]
        
        countNoActif = 0
        for comp in competenceNoActif:
            countNoActif += comp["effectif"]

        countcomp = countActif+countNoActif

        context = {
            "countcomp":countcomp,
            "countactif":countActif,
            "countNoactif":countNoActif
        }
        return render(request, "fetchcomp.html", context)

class ajaxcomp(View):
    def get(self, request, id, *args, **kwargs):
        # Récuperer le type de compétence
        type_competence = TypeCompetence.objects.get(id=id)
        comments = ["Maternelle", "Courant", "Débutant", "Intermediaire", "Avancé"]
        context = {
            "type_comp":type_competence.name,
            "comments": comments
        }
        return render(request, "ajaxcomp.html", context)
    
    
# ================== Gestion de type de competence =========================

@login_required(login_url='connection/login')
@csrf_exempt
def type_competences(request):
    
    date = datetime.datetime.now()

    typeCompetences = TypeCompetence.objects.filter(user_id=request.user.id)
   
    context = {
        "typeCompetences":typeCompetences,
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request),
        "parametre":parametre(),
        "date":date
    }
    return render(request, "typeCompetence/type_competences.html", context)


@login_required(login_url='connection/login')
@csrf_exempt
def add_type_competence(request):
    date = datetime.datetime.now()

    if request.method == "POST":
        name = bleach.clean(request.POST["name"].strip())
        query = TypeCompetence.objects.filter(name=name,user_id=request.user.id)
        # Verifier l'existence du type de competence
        if query.exists():
            return JsonResponse({
                "status": "error",
                "message": "Ce type de compétence existe déjà."})
        else:
            count0 = TypeCompetence.objects.all().count()
            entreprise = TypeCompetence(name=name, user_id=request.user.id)
            entreprise.save()
            count1 = TypeCompetence.objects.all().count()
            # Verifier si l'ajout a été bien effectué
            if count0 < count1:
                return JsonResponse({
                    "status": "success",
                    "message": "Type de classe enregistré avec succès."})
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
    return render(request, "typeCompetence/add_typeCompetence.html", context)

@login_required(login_url='connection/login')
def edit_type_competence(request,id):
    date = datetime.datetime.now()
    
    type_id = int(dechiffrer_param(str(id)))
    type = TypeCompetence.objects.get(id=type_id)
    #On vérifie si ce membre est authorisé à acceder à cette page ou pas.
    query = TypeCompetence.objects.filter(id=type_id, user_id=request.user.id)
    if query.exists():
        context = {
            "type":type,
            "countanswer":nbnew_answer(request),
            "count":nbnew_message(request),
            "users":new_message(request),
            "parametre":parametre(),
            "date":date
        }
        return render(request, "typeCompetence/edit_typeCompetence.html", context)
    else:
        return redirect("authorization")

@login_required(login_url='connection/login')
@csrf_exempt
def edit_typec(request):
    
    if request.method == "POST":
        id = int(request.POST["id"])
        try:
            type = TypeCompetence.objects.get(id=id)
        except:
            type = None

        if type == None:
            return JsonResponse({
                "status": "error",
                "message": "Identifiant inexistant."})
        else:
            name = bleach.clean(request.POST["name"].strip())

            # Exclure ce type de compétence de la liste des type de compétences
            types = TypeCompetence.objects.filter(user_id = request.user.id).exclude(id=id)
            tabtypeCompetence = []
            for ent in types:
                tabtypeCompetence.append(ent.name)
            #O Verifier l'existence du type de compétence
            if name in tabtypeCompetence:
                return JsonResponse({
                    "status": "error",
                    "message": "Ce type de compétence existe déjà."})
            else:
                type.name = name
                type.save()
                return JsonResponse({
                    "status": "success",
                    "message": "Type de compétence modifié avec succès."})
                
def ajax_delete_type_competence(request, id):
    type = TypeCompetence.objects.get(id=id)
    context = {
        "type": type
    }
    return render(request, "ajax_delete_type_competence.html", context)


@login_required(login_url='connection/login')
def del_type_competence(request,id):
    try:
        type_id = int(dechiffrer_param(str(id)))
        type = TypeCompetence.objects.get(id=type_id)
    except:
        type = None
    
    if type and type.user.id == request.user.id:
        type.delete()
    return redirect("typeCompetence/type_competences")
