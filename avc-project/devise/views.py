# Importation des modules standard
import bleach
# Importation des modules tiers
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
# Importation des modules locaux
from eajc.views import get_setting 
from eajcprojet.utils.crypto import dechiffrer_param
from .models import*


#========================== Progrès du projet personnel ============================
@login_required(login_url='connection/login')
def devises(request):
    setting = get_setting()
    if setting is None:
        redirect("settings/maintenance")
           
    devises = Devise.objects.all()
    context = {
        "devises": devises,
        "setting": setting
    }
    return render(request, "devises.html", context)


@login_required(login_url='connection/login')
def add_devise(request):

    setting = get_setting()
    if setting is None:
        redirect("settings/maintenance")
    
    if request.method == "POST":
        nom = bleach.clean(request.POST["nom"].strip())
        symbole = bleach.clean(request.POST["symbole"].strip())

        query = Devise.objects.filter(nom=nom)
        if query.exists():
            return JsonResponse({
                "status": "error",
                "message": "Ce progrès existe déjà"})
        else:
            devise = Devise(
                nom=nom,
                symbole=symbole)
            # Nombre de dévise avant l'ajout
            count0 = Devise.objects.all().count()
            devise.save()
            # Nombre de dévises après l'ajout
            count1 = Devise.objects.all().count()
            # On verifie si l'insertion a eu lieu ou pas.
            if count0 < count1:
                return JsonResponse({
                    "status": "success",
                    "message": "Dévise enregistrée avec succès."})
            else:
                return JsonResponse({
                    "status": "error",
                    "message": "L'opération a échoué."})
    context = {
        "setting": setting
    }
    return render(request, "add_devise.html", context)


@login_required(login_url='connection/login')
def edit_devise(request, id):
    setting = get_setting()
    if setting is None:
        redirect("settings/maintenance")
        
    devise_id = int(dechiffrer_param(str(id)))
        
    devise = get_object_or_404(Devise, id=devise_id)
    context = {
            "setting": setting,
            "devise": devise
    }
    return render(request, "edit_devise.html", context)

@login_required(login_url='connection/login')
def edit_dev(request):
    if request.method == "POST":
        id = int(request.POST["id"])
        try:
            devise = get_object_or_404(Devise, id=id)
        except:
            devise = None
        
        if devise is None:
            return JsonResponse({
                    "status": "error",
                    "message": "Identifiant inexistant."})
        else:
            # Se proteger de l'attaque XSS(Injection du code javascript)
            nom = bleach.clean(request.POST["nom"].strip())
            symbole = bleach.clean(request.POST["symbole"].strip())
            #On exclut la dévise que l'on veut modifier
            devises = Devise.objects.exclude(id=id)
            tabDevises = []
            for dv in devises:
                tabDevises.append(dv.nom)
            if nom in tabDevises:
                return JsonResponse({
                    "status": "error",
                    "message": "Cette dévise existe déjà."})
            else:
                devise.nom = nom
                devise.symbole = symbole
                devise.save()
                return JsonResponse({
                    "status": "success",
                    "message": "Dévise modifiée avec succès."})

def ajax_delete_devise(request, id):
    devise = Devise.objects.get(id=id)
    context = {
        "devise": devise
    }
    return render(request, "ajax_delete_devise.html", context)

@login_required(login_url='connection/login')
def del_devise(request, id):
    try:    
        devise_id = int(dechiffrer_param(str(id)))
        devise = get_object_or_404(Devise, id=devise_id)
    except:
        devise = None
        
    if devise:
        devise.delete()
    return redirect("devises")


