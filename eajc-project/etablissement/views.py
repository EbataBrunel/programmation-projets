# Importation des modules standard
import datetime
import bleach
# Importation des modules tiers
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Imporation des modules locaux
from eab.views import nbnew_answer, nbnew_message, new_message, parametre
from .models import*
from eajc.utils.crypto import dechiffrer_param

#=================== Gestion de l'établissemnt ======================
@login_required(login_url='connection/login')
def etablissements(request):
    date = datetime.datetime.now()

    etablissements = Etablissement.objects.filter(user_id=request.user.id)
    context = {
        "etablissements":etablissements,
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request),
        "parametre":parametre(),
        "date":date
    }
    return render(request, "etablissements.html", context)

@login_required(login_url='connection/login')
@csrf_exempt
def add_etab(request):
    date = datetime.datetime.now()

    if request.method == "POST":
        name = bleach.clean(request.POST["name"].strip())
        country = bleach.clean(request.POST["country"].strip())
        city = bleach.clean(request.POST["city"].strip())

        query = Etablissement.objects.filter(name=name, user_id=request.user.id)
        if query.exists():
            return JsonResponse({
                    "status": "error",
                    "message": "Cet établissement existe déjà."})
        else:
            etablissement = Etablissement(
                name=name,
                country=country,
                city=city,
                user_id=request.user.id
            )
            # Nombre d'établissements avant l'ajout
            count0 = Etablissement.objects.all().count()
            etablissement.save()
            # Nombre d'établissemnts après l'ajout
            count1 = Etablissement.objects.all().count()
            # On verifie si l'insertion a eu lieu ou pas.
            if count0 < count1:
                return JsonResponse({
                    "status": "success",
                    "message": "Etablissement enregistré avec succès."})
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
    return render(request, "add_etab.html", context)

@login_required(login_url='connection/login')
def edit_etab(request,id):
    date = datetime.datetime.now()
    
    etablissement_id = dechiffrer_param(str(id))
    etablissement = Etablissement.objects.get(id=etablissement_id)
    #On vérifie si ce membre est authorisé à acceder à cette page ou pas.
    query = Etablissement.objects.filter(id=etablissement_id, user_id=request.user.id)
    if query.exists():
        context = {
            "etablissement":etablissement,
            "countanswer":nbnew_answer(request),
            "count":nbnew_message(request),
            "users":new_message(request),
            "parametre":parametre(),
            "date":date
        }
        return render(request, "edit_etab.html", context)
    else:
        return redirect("authorization")

@login_required(login_url='connection/login')
@csrf_exempt
def edit_eta(request):
    if request.method=="POST":
        id = int(request.POST["id"])
        try:
            etablissement = Etablissement.objects.get(id=id)
        except:
            etablissement = None
        
        if etablissement == None:
            return JsonResponse({
                    "status": "error",
                    "message": "Identifiant inexistant."})
        else:
            # Se proteger de l'attaque XSS(Injection du code javascript)
            name = bleach.clean(request.POST["name"].strip())
            country = bleach.clean(request.POST["country"].strip())
            city = bleach.clean(request.POST["city"].strip())
            #On exclut l'établissement' que l'on veut modifier et on recupère les autres
            etablissements = Etablissement.objects.exclude(id=id)
            tabEtablissement = []
            for etab in etablissements:
                try:
                    if etab.user.id == request.user.id:
                        tabEtablissement.append(etab.name)
                except Exception as e:
                    pass
            #On verifie si cet établissement existe déjà
            if name in tabEtablissement:
                return JsonResponse({
                    "status": "error",
                    "message": "Cet établissement existe déjà."})
            else:
                etablissement.name = name
                etablissement.country = country
                etablissement.city = city
                etablissement.save()
                return JsonResponse({
                    "status": "success",
                    "message": "L'établissement modifié avec succès."})


def ajax_delete_etab(request, id):
    etablissement = Etablissement.objects.get(id=id)
    context = {
        "etablissement": etablissement
    }
    return render(request, "ajax_delete_etab.html", context)

@login_required(login_url='connection/login')
def del_etab(request, id):
    try:    
        etablissement_id = dechiffrer_param(str(id))
        etablissement = Etablissement.objects.get(id=etablissement_id)
    except:
        etablissement = None
        
    if etablissement:
        etablissement.delete()
    return redirect("etablissements")


