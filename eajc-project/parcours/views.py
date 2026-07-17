# Importation des modules standards
import datetime
import bleach
# Importation des modules tiers
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Importation des modules locaux
from eab.views import nbnew_answer, nbnew_message, new_message, parametre
from .models import*
from annee.models import*
from eajc.utils.crypto import dechiffrer_param


#=================== Gestion de parcours ======================
@login_required(login_url='connection/login')
def parcours(request):
    date = datetime.datetime.now()

    parcours = Parcours.objects.filter(user_id=request.user.id).select_related('etablissement','annee','formation').order_by('annee_id')

    context={
        "parcours" : parcours,
        "countanswer" : nbnew_answer(request),
        "count" : nbnew_message(request),
        "users" : new_message(request),
        "parametre" : parametre(),
        "date" : date
    }
    return render(request, "parcours.html", context)

@login_required(login_url='connection/login')
@csrf_exempt
def add_parcours(request):
    date = datetime.datetime.now()

    if request.method == "POST":
            annee = request.POST["annee"]
            annee1 = request.POST["annee1"]

            user = request.user.id
            etablissement = request.POST["etablissement"]
            formation = request.POST["formation"]
            niveau = request.POST["niveau"]
            
            if niveau == "Autre niveau":
                autre_niveau = bleach.clean(request.POST["autre_niveau"].strip())
                niveau = autre_niveau 
                
            query = Parcours.objects.filter(
                etablissement_id=etablissement, 
                annee_id=annee, 
                user_id=request.user.id
            )
            if query.exists():
                return JsonResponse({
                    "status": "error",
                    "message": "Ce parcours existe déjà."})
            else:
                parcours = Parcours(
                    niveau = niveau,
                    annee_id = annee,
                    annee1 = annee1,
                    etablissement_id = etablissement,
                    formation_id = formation,
                    user_id = user
                )
                count0 = Parcours.objects.all().count()
                parcours.save()
                count1 = Parcours.objects.all().count()
                if count0 < count1:
                    return JsonResponse({
                    "status": "success",
                    "message": "Parcours enregistré avec succès."})
                else:
                    return JsonResponse({
                    "status": "error",
                    "message": "L'insertion a échouée."})

    annees = Annee.objects.all().order_by("-libelle")
    etablissements = Etablissement.objects.filter(user_id=request.user.id)
    formations = Formation.objects.filter(user_id=request.user.id)
    niveaux = ["Bac + 1", "Bac + 2", "Bac + 3", "Bac + 4", "Bac + 5", "Bac + 6", "Bac + 7", "1ère année Ingénieur", "2ème année Ingénieur", "3ème année Ingénieur", "Autre niveau" ]

    context = {
        "etablissements":etablissements,
        "formations":formations,
        "annees":annees,
        "niveaux":niveaux,
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request),
        "parametre":parametre(),
        "date":date
    }
    return render(request, "add_parcours.html", context)

@login_required(login_url='connection/login')
def edit_parcours(request,id):
    date = datetime.datetime.now()
    
    parcours_id = dechiffrer_param(str(id))
    parcours = Parcours.objects.get(id=parcours_id)
    annees = Annee.objects.all()
    etablissements = Etablissement.objects.filter(user_id=request.user.id).exclude(id=parcours.etablissement.id)
    formations = Formation.objects.filter(user_id=request.user.id).exclude(id=parcours.formation.id)
    tabannee = []
    for annee in annees:
        if int(annee.libelle) > int(parcours.annee.libelle):
            tabannee.append(annee)

    niveaux = ["Bac + 1", "Bac + 2", "Bac + 3", "Bac + 4", "Bac + 5", "Bac + 6", "Bac + 7", "1ère année Ingénieur", "2ème année Ingénieur", "3ème année Ingénieur", "Autre niveau" ]
    new_niveaux = []
    for niveau in niveaux:
        if parcours.niveau != niveau:
            new_niveaux.append(niveau)
    # Verifier si ce membre est authorisé à acceder à cette page.
    query = Parcours.objects.filter(id=parcours_id, user_id=request.user.id)
    if query.exists():
        context = {
            "etablissements":etablissements,
            "formations":formations,
            "parcours":parcours,
            "annees":annees, 
            "tabannee":tabannee,
            'niveaux':new_niveaux,
            "countanswer":nbnew_answer(request),
            "count":nbnew_message(request),
            "users":new_message(request),
            "parametre":parametre(),
            "date":date
        }
        return render(request, "edit_parcours.html", context)
    else:
        return redirect("authorization")

@login_required(login_url='connection/login')
@csrf_exempt
def edit_par(request): 
    if request.method == "POST":
        id = int(request.POST["id"])
        try:
            parcours = Parcours.objects.get(id=id)
        except:
            parcours = None

        if parcours == None:
            return JsonResponse({
                    "status": "error",
                    "message": "Identifiant inexistant."})
        else:    
            annee = request.POST["annee"]
            annee1 = request.POST["annee1"]
            etablissement = request.POST["etablissement"]
            formation = request.POST["formation"]
            niveau = request.POST["niveau"]
            status = request.POST["status"]
            
            if niveau == "Autre niveau":
                autre_niveau = bleach.clean(request.POST["autre_niveau"].strip())
                niveau = autre_niveau 
                
            # Exclure le parcours que l'on veut modifier et on recupère les autres
            list_parcours = Parcours.objects.exclude(id=id)
            
            tabParcours = []
            for parcour in list_parcours:
                try:
                    if parcour.user.id == request.user.id :
                        tabParcours.append(parcour)
                except Exception as e:
                    pass

            # Verifier l'existence de ce parcours
            x=False
            for p in tabParcours:
                if int(annee) == p.annee.id and int(etablissement) == p.etablissement.id:
                    x=True
            if x :
                return JsonResponse({
                    "status": "error",
                    "message": "Ce parcours existe déjà."})
            else:
                parcours.annee_id = annee
                parcours.annee1 = annee1
                parcours.etablissement_id = etablissement
                parcours.formation_id = formation
                parcours.niveau = niveau
                parcours.statusan = status
                
                parcours.save()
            return JsonResponse({
                    "status": "success",
                    "message": "Parcours modifié avec succès."})
        
def ajax_delete_parcours(request, id):
    parcours = Parcours.objects.get(id=id)
    context = {
        "parcours": parcours
    }
    return render(request, "ajax_delete_parcours.html", context)


@login_required(login_url='connection/login')
def del_parcours(request,id):
    try:
        parcours_id = dechiffrer_param(str(id))
        parcours = Parcours.objects.get(id=parcours_id)
    except:
        parcours = None
        
    if parcours and parcours.user.id == request.user.id:
        parcours.delete()
    return redirect("parcours")

class fetchpar(View):
    def get(self, request, id, *args, **kwargs):
        #On compte le nombre de matière qui ne sont pas publiées
        parcoursNoActif = Parcours.objects.values("etablissement_id","annee_id","annee1").filter(annee_id=id,user_id=request.user.id,status=0).annotate(effectif=Count("annee_id"))
        #On compte le nombre de matière qui sont publiées
        parcoursActif = Parcours.objects.values("etablissement_id","annee_id","annee1").filter(annee_id=id,user_id=request.user.id,status=1).annotate(effectif=Count("annee_id"))

        countMatiereNoActif = 0
        for parcour in parcoursNoActif:
            countMatiereNoActif += parcour["effectif"]

        countMatiereActif = 0
        for parcour in parcoursActif:
            countMatiereActif += parcour["effectif"]

        countpar=countMatiereActif + countMatiereNoActif

        context={
            "countpar":countpar,
            "countactif":countMatiereActif,
            "countNoactif":countMatiereNoActif
        }
        return render(request, "fetchpar.html", context)

    
class status(View):
    def get(self, request, id, *args, **kwargs):
        return JsonResponse({'status':id})


class statpar(View):
    def get(self, request, id, *args, **kwargs):
        parcours = Parcours.objects.get(id=id)
        if parcours.status == 0:
            parcours.status = 1
        else:
            parcours.status = 0
        parcours.save()
        context = {"parcours":parcours}
        return render(request, "statpar.html", context)
    
class getAnnee(View):
    def get(self, request, id, *args, **kwargs):       
        tabAnnees = []
        annee = Annee.objects.get(id=id)
        annees = Annee.objects.all()

        for anne in annees:
            if int(anne.libelle) > int(annee.libelle):
                tabAnnees.append(anne)

        context = {
            "annees":tabAnnees
        }
        return render(request, "ajaxAnnee.html", context)
    

    
class getAnneeEdit(View):
    def get(self, request, id, *args, **kwargs):
        
        tabAnnees = []
        annee = Annee.objects.get(id=id)
        annees = Annee.objects.all()

        for anne in annees:
            if int(anne.libelle) > int(annee.libelle):
                tabAnnees.append(anne)

        context = {
            "annees":tabAnnees
        }
        return render(request, "ajaxAnnee.html", context)
    
class niveau(View):
    def get(self, request, id, *args, **kwargs):
        context = {"niveau":id}
        return render(request, "niveau.html", context)
    
