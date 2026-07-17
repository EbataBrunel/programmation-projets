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

#=================== Gestion de l'entreprise ======================
@login_required(login_url='connection/login')
def entreprises(request):
    date = datetime.datetime.now()

    entreprises = Entreprise.objects.filter(user_id=request.user.id)
    context = {
        "entreprises":entreprises,
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request),
        "parametre":parametre(),
        "date":date
    }
    return render(request, "entreprises.html", context)

@login_required(login_url='connection/login')
@csrf_exempt
def add_ent(request):
    date = datetime.datetime.now()

    if request.method == "POST":
        name = bleach.clean(request.POST["name"].strip())
        country = bleach.clean(request.POST["country"].strip())
        city = bleach.clean(request.POST["city"].strip())
        query = Entreprise.objects.filter(name=name,user_id=request.user.id)
        # Verifier l'existence de l'entreprise
        if query.exists():
            return JsonResponse({
                    "status": "error",
                    "message": "Cette entreprise existe déjà."})
        else:
            count0 = Entreprise.objects.all().count()
            entreprise = Entreprise(name=name, country=country, city=city, user_id=request.user.id)
            entreprise.save()
            count1 = Entreprise.objects.all().count()
            # Verifier si l'ajout a été bien effectué
            if count0 < count1:
                return JsonResponse({
                    "status": "success",
                    "message": "Entreprise enregistrée avec succès."})
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
    return render(request, "add_ent.html", context)

@login_required(login_url='connection/login')
def edit_ent(request, id):
    date = datetime.datetime.now()
    entreprise_id = dechiffrer_param(str(id))
    entreprise = Entreprise.objects.get(id=entreprise_id)
    #On vérifie si ce membre est authorisé à acceder à cette page ou pas.
    query = Entreprise.objects.filter(id=entreprise_id, user_id=request.user.id)
    if query.exists():
        context = {
            "entreprise":entreprise,
            "countanswer":nbnew_answer(request),
            "count":nbnew_message(request),
            "users":new_message(request),
            "parametre":parametre(),
            "date":date
        }
        return render(request, "edit_ent.html", context)
    else:
        return redirect("authorization")

@login_required(login_url='connection/login')
@csrf_exempt
def edit_en(request):
    
    if request.method == "POST":
        id = int(request.POST["id"])
        try:
            entreprise = Entreprise.objects.get(id=id)
        except:
            entreprise = None

        if entreprise == None:
            return JsonResponse({
                    "status": "error",
                    "message": "Identifiant inexistant."})
        else:
            name = bleach.clean(request.POST["name"].strip())
            country = bleach.clean(request.POST["country"].strip())
            city = bleach.clean(request.POST["city"].strip())

            # Exclure l'entreprise de la liste des entreprises
            entreprises = Entreprise.objects.filter(user_id = request.user.id).exclude(id=id)
            tabEntreprise = []
            for ent in entreprises:
                tabEntreprise.append(ent.name)
            #O Verifier l'existence de entreprise
            if name in tabEntreprise:
                return JsonResponse({
                    "status": "error",
                    "message": "Cette entreprise existe déjà."})
            else:
                entreprise.name = name
                entreprise.country = country
                entreprise.city = city
                entreprise.save()
                return JsonResponse({
                    "status": "success",
                    "message": "Entreprise modifiée avec succès."})
            
def ajax_delete_entreprise(request, id):
    entreprise = Entreprise.objects.get(id=id)
    context = {
        "entreprise": entreprise
    }
    return render(request, "ajax_delete_entreprise.html", context)

@login_required(login_url='connection/login')
def del_ent(request,id):
    try:
        entreprise_id = dechiffrer_param(str(id))
        entreprise = Entreprise.objects.get(id=entreprise_id)
    except:
        entreprise = None
    
    if entreprise and entreprise.user.id == request.user.id:
        entreprise.delete()
    return redirect("entreprises")

