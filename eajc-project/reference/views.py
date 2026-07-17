# Importation des modules standards
import datetime
import bleach
import re
# Importation des modules tiers
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views import View
# Imporation des modules locaux
from .models import *
from eab.views import nbnew_answer, nbnew_message, new_message, parametre
from eajc.utils.crypto import dechiffrer_param

def references(request):
    date = datetime.datetime.now()

    references = Reference.objects.filter(user_id=request.user.id).select_related('entreprise')
    context = {
        "references":references,
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request),
        "parametre":parametre(),
        "date":date
    }
    return render(request, "references.html", context)

@login_required(login_url='connection/login')
@csrf_exempt
def add_ref(request):
    date=datetime.datetime.now()

    if request.method == "POST":
        name = bleach.clean(request.POST["name"].strip())
        entreprise = request.POST["entreprise"]
        gender = request.POST["gender"]
        phone = bleach.clean(request.POST["phone"].strip())
        email = request.POST["email"]

        regexp = r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$"
        query = Reference.objects.filter(entreprise_id=entreprise,name=name,user_id=request.user.id)
        # Verifier l'existence de la référence
        if query.exists():
            return JsonResponse({
                    "status": "error",
                    "message": "Cette réference existe déjà."})
        elif not re.search(regexp, email): #On verifie si l'adresse e-mail correspond bien au format
            return JsonResponse({
                    "status": "error",
                    "message": "Le format de cet adresse mail ne correspond pas."})
        else:
                    
            experience = Reference(
                user_id = request.user.id,
                entreprise_id = entreprise,
                name = name,
                gender = gender,
                phone = phone,
                email = email
            )
            count0 = Reference.objects.all().count()
            experience.save()
            count1 = Reference.objects.all().count()
            # Verifier si l'ajout a été bien effectué ou pas
            if count0 < count1:
                return JsonResponse({
                    "status": "success",
                    "message": "Réference enregistrée avec succès."})
            else:
                return JsonResponse({
                    "status": "error",
                    "message": "L'inertion a échouée."})

    entreprises = Entreprise.objects.filter(user_id=request.user.id)

    context = {
        "entreprises":entreprises,
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request),
        "parametre":parametre(),
        "date":date
    }
    return render(request, "add_ref.html", context)

@login_required(login_url='connection/login')
def edit_ref(request,id):
    date = datetime.datetime.now()
    
    reference_id = dechiffrer_param(str(id))
    #Recupperer la réference
    reference = Reference.objects.get(id=reference_id)
    #Liste des entreprises de l'utilisateur
    entreprises = Entreprise.objects.filter(user_id=request.user.id).exclude(id=reference_id)
    #On vérifie si ce membre est authorisé à acceder à cette page ou pas.
    query = Reference.objects.filter(id=reference_id,user_id=request.user.id)
    if query.exists():
        context = {
            "reference":reference,
            "entreprises":entreprises,
            "countanswer":nbnew_answer(request),
            "count":nbnew_message(request),
            "users":new_message(request),
            "parametre":parametre(),
            "date":date
        }
        return render(request, "edit_ref.html", context)
    else:
        return redirect("authorization")

@login_required(login_url='connection/login')
@csrf_exempt
def edit_re(request):
    if request.method=="POST":
        id = int(request.POST["id"])
        try:
            reference = Reference.objects.get(id=id)
        except:
            reference = None
        
        if reference == None:
            return JsonResponse({
                    "status": "error",
                    "message": "Identifiant inexistant."})
        else:
            name = bleach.clean(request.POST["name"].strip())
            entreprise = request.POST["entreprise"]
            gender = request.POST["gender"]
            phone = bleach.clean(request.POST["phone"].strip())
            email = request.POST["email"]

            regexp = r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$"
            #On verifie si la reference a été déjà enregistrée
            query = Reference.objects.filter(entreprise_id=entreprise,name=name,user_id=request.user.id).exclude(id=id)    
            if query.exists():
                return JsonResponse({
                    "status": "error",
                    "message": "Cette réference existe déjà."})      
            elif not re.search(regexp, email): #On verifie si l'adresse e-mail correspond bien au format
                return JsonResponse({
                    "status": "error",
                    "message": "Le  format de l'adresse mail ne correspond pas."})
            else:
                reference.entreprise_id = entreprise
                reference.name = name
                reference.gender = gender
                reference.phone = phone
                reference.email = email

                reference.save()
                return JsonResponse({
                    "status": "success",
                    "message": "Réference enregistrée avec succès."})
                
def ajax_delete_reference(request, id):
    reference = Reference.objects.get(id=id)
    context = {
        "reference": reference
    }
    return render(request, "ajax_delete_reference.html", context)

@login_required(login_url='connection/login')
def del_ref(request,id):
    try:
        reference_id = dechiffrer_param(str(id))
        reference = Reference.objects.get(id=reference_id)
    except:
        reference = None
        
    if reference and reference.user.id == request.user.id:
        reference.delete()
    return redirect("references")

class statref(View):
    def get(self, request, id, *args, **kwargs):
        reference = Reference.objects.get(id=id)
        if reference.status == 0:
            reference.status = 1
        else:
            reference.status = 0
        reference.save()
        context = {"reference":reference}
        return render(request, "statref.html", context)
    
    
    
   

