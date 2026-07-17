# Importation des modules standards
import datetime
import bleach
# Importation des modules tiers
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Importation des modules locaux
from .models import*
from eab.views import nbnew_answer, nbnew_message, new_message, parametre
from eajc.utils.crypto import dechiffrer_param


#=================== Gestion de formation ======================
@login_required(login_url='connection/login')
def formations(request):
    date = datetime.datetime.now()

    formations = Formation.objects.filter(user_id=request.user.id)
    context = {
        "formations":formations,
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request),
        "parametre":parametre(),
        "date":date
    }
    return render(request, "formations.html", context)

@login_required(login_url='connection/login')
@csrf_exempt
def add_form(request):
    date = datetime.datetime.now()

    if request.method == "POST":
        
        intitule = bleach.clean(request.POST["intitule"].strip())
        # Verifier l'existence de la formation
        query = Formation.objects.filter(intitule=intitule, user_id=request.user.id)
        if query.exists():
            return JsonResponse({
                    "status": "error",
                    "message": "Cette formation existe déjà."})
        else:
            formation = Formation(intitule=intitule, user_id=request.user.id)
            count0 = Formation.objects.all().count()
            formation.save()
            count1 = Formation.objects.all().count()
            # Verifier si l'ajout a été bien effectué
            if count0 < count1:
                return JsonResponse({
                    "status": "success",
                    "message": "Formation enregistrée avec succès."})
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
    return render(request, "add_form.html", context)

@login_required(login_url='connection/login')
def edit_form(request,id):
    date = datetime.datetime.now()
    
    formation_id = dechiffrer_param(str(id))
    formation = Formation.objects.get(id=formation_id)
    # Verifier si ce membre est authorisé à acceder à cette page ou pas.
    query = Formation.objects.filter(id=formation_id, user_id=request.user.id)
    if query.exists():
        context = {
            "formation":formation,
            "countanswer":nbnew_answer(request),
            "count":nbnew_message(request),
            "users":new_message(request),
            "parametre":parametre(),
            "date":date
        }
        return render(request, "edit_form.html", context)
    else:
        return redirect("authorization")

@login_required(login_url='connection/login')
@csrf_exempt
def edit_for(request):
    if request.method == "POST":
        id = int(request.POST["id"])
        try:
            formation = Formation.objects.get(id=id)
        except:
            formation = None

        if formation == None:
            return JsonResponse({
                    "status": "error",
                    "message": "Identifiant inexistant."})
        else:
            intitule = bleach.clean(request.POST["intitule"].strip())
            #On exclut la formation que l'on veut modifier et on recupère les autres
            formations = Formation.objects.filter(user_id = request.user.id).exclude(id = id)
            tabFormation = []
            for form in formations:
                tabFormation.append(form.intitule)
                
            #On verifie si cette formation existe déjà
            if intitule in tabFormation:
                return JsonResponse({
                    "status": "error",
                    "message": "Cette formation existe déjà."})
            else:
                formation.intitule = intitule
                formation.save()
                return JsonResponse({
                    "status": "success",
                    "message": "Formation modifiée avec succès."})
                
def ajax_delete_form(request, id):
    formatation = Formation.objects.get(id=id)
    context = {
        "formation": formatation
    }
    return render(request, "ajax_delete_form.html", context)

@login_required(login_url='connection/login')
def del_form(request,id):
    try:
        formation_id = dechiffrer_param(str(id))
        formation = Formation.objects.get(id=formation_id)
    except:
        formation = None
        
    if formation and formation.user.id == request.user.id:
        formation.delete()
    return redirect("formations")