# Importation des modules standards
import datetime
import bleach
# Importation des modules tiers
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.decorators.csrf import csrf_exempt
# Importation des modules locaux
from eab.views import nbnew_answer, nbnew_message, new_message, parametre
from .models import*
from app_auth.decorator import*

@login_required(login_url='connection/login')
@csrf_exempt
def baccalaureat(request):
    date = datetime.datetime.now()
    #Récuperer les établissements
    etablissements = Etablissement.objects.filter(user_id=request.user.id) 
    #Récuperer les années
    annees = Annee.objects.all().order_by("-id")
    baccalaureat = Baccalaureat.objects.filter(user_id=request.user.id).first()
    
    if request.method == "POST":
        if baccalaureat :
            anneeId = request.POST["annee"]
            etablissementId = request.POST["etablissement"]
            diplome = request.POST["diplome"]
            
            bac = Baccalaureat.objects.get(id=baccalaureat.id)
            bac.annee_id = anneeId
            bac.etablissement_id = etablissementId
            
            if diplome == "Autre BAC":
                autre_diplome = bleach.clean(request.POST["autre_diplome"].strip())
                diplome = autre_diplome 
                
            bac.diplome = diplome
            bac.save()
            return redirect("baccalaureat")
        else:
            anneeId = request.POST["annee"]
            etablissementId = request.POST["etablissement"]
            diplome = request.POST["diplome"]
            
            if diplome == "Autre BAC":
                autre_diplome = bleach.clean(request.POST["autre_diplome"].strip())
                diplome = autre_diplome 
            
            bac = Baccalaureat(
                user_id = request.user.id, 
                annee_id = anneeId, 
                etablissement_id = etablissementId, 
                diplome = diplome
            )
            bac.save()
            return redirect("baccalaureat")
        
    diplomes = [
        'BAC A1',
        'BAC A2',
        'BAC A3',
        'BAC A4',
        'BAC A5',
        'BAC C',
        'BAC D',
        'BAC E',
        'BAC F1',
        'BAC F2',
        'BAC F3',
        'BAC F4',
        "BAC Français ('inscription non-règlementée')",
        "BAC Français ('inscription règlementée')",
        "BAC Français ('lycée français')",
        'BAC G1',
        'BAC G2',
        'BAC G3',
        'BAC R1',
        'BAC R2',
        'BAC R3',
        'BAC R4',
        'BAC R5',
        'BAC R6',
        'BAC R7',
        'Autre BAC']  
    context = {
        "annees":annees,
        "etablissements":etablissements,
        "diplomes":diplomes,
        "baccalaureat":baccalaureat,
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request),
        "parametre":parametre(),
        "date":date
    }
    return render(request, "baccalaureat.html", context)

def delete_baccalaureat(request, id):
    try:
        baccalaureat = Baccalaureat.objects.get(id=id)
    except:
        baccalaureat = None
        
    if baccalaureat and baccalaureat.user.id == request.user.id:
        baccalaureat.delete()
        
    return redirect("baccalaureat")

class diplome(View):
    def get(self, request, id, *args, **kwargs):
        context = {"diplome":id}
        return render(request, "diplome.html", context)
