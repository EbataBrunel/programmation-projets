# Importation des modules standards
import datetime
import os
import hashlib
# Importation des modules tiers
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib import messages
from PyPDF2 import PdfMerger
from django.conf import settings
#Imporation des modules locaux
from .models import*
from eab.views import nbnew_answer, nbnew_message, new_message, parametre
from eajc.utils.crypto import dechiffrer_param


# Convertir la taille du fichier en octet
def taille_de_fichier(taille):
    """
    Convertit la taille du fichier en octets dans une unité lisible (Ko, Mo, Go, To).
    Args:
        taille (int): Taille du fichier en octets.

    Returns:
        str: Taille du fichier avec une unité lisible.
    """
    # Liste des unités de taille
    tailles = ['octets', 'Ko', 'Mo', 'Go', 'To'] # Une liste des unités de taille, des octets aux téraoctets.   
    # Commence avec les octets
    index = 0
    while taille >= 1024 and index < len(tailles) - 1:
        taille /= 1024.0 # Divise la taille par 1024 à chaque itération pour passer à l'unité supérieure.
        index += 1
    
    # Retourne la taille avec deux décimales et l'unité appropriée
    return f"{taille:.2f} {tailles[index]}"


def get_file_hash(file):
    hash_md5 = hashlib.md5() # Cette objet de MD5 servira de stocker et calculer l'empreinte MD5.
    for chunk in file.chunks(): # Parcourir le fichier par morceau pour ne pas surcherger la memoire
        hash_md5.update(chunk) # Ajout de chaque morceau au calcul de hash et en mettant en même à jour le hash
    return hash_md5.hexdigest() # retourner l'empreinte MD5 sous forme de chaîne hexadécimale

def lms(request):
    date = datetime.datetime.now()

    if request.method == "POST":
        type = request.POST["type"]
        file = request.FILES["file"]
        
        # Vérifier l'extension du fichier
        if not file.name.endswith('.pdf'):
            messages.error(request, "Seuls les fichiers PDF sont acceptés.")       
        # Limiter la taille du fichier à 10 Mo
        elif file.size > 10 * 1024 * 1024:
            messages.error(request, "La taille du fichier ne doit pas dépasser 10 Mo.")
        else:
            liste_lms = Lettre_mot.objects.all()
            liste_empreint_md5 = []
            for l in liste_lms:
                liste_empreint_md5.append(get_file_hash(l.file))
                l.file.close()  # Fermer le fichier après le calcul du hash
            
            if get_file_hash(file) in liste_empreint_md5:
                messages.error(request, "Ce fichier existe déjà.")
            else:
                lm=Lettre_mot(user_id=request.user.id, type=type, file=file, date=date)
                lm.save()
        return redirect("lms")

    lms = Lettre_mot.objects.filter(user_id=request.user.id)
    list_lms = []
    for lm in lms:
        dic = {}
        dic["lm"] = lm
        # Taille du fichier
        size = lm.file.size 
        # Conversion de la taille du fichier
        dic["size"] = taille_de_fichier(size)
        list_lms.append(dic)
        
    types = ["Inscription","Stage","Alternance","Emploi"]
    context = {
        "lms":list_lms,
        "types":types,
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request),
        "parametre":parametre(),
        "date":date
    }
    return render(request, "lms.html", context)

@login_required(login_url='connection/login')
@csrf_exempt
def edit_lm(request,id):
    date = datetime.datetime.now()
    lm_id = dechiffrer_param(str(id))
    lm = Lettre_mot.objects.get(id=lm_id)
    types = ["Inscription","Stage","Alternance","Emploi"]
    new_types = []
    for type in types:
        if lm.type != type:
            new_types.append(type)

    context = {
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request),
        "parametre":parametre(),
        "date":date,
        "lm":lm,
        "types":new_types,
    }
    return render(request, "edit_lm.html", context)

@login_required(login_url='connection/login')
def edit_l(request):
    if request.method == "POST":
        id = int(request.POST["id"])
        try:
            lm = Lettre_mot.objects.get(id=id)
        except:
            lm = None

        if lm == None:
            return JsonResponse({
                "status": "error",
                "message": "Identifiant inexistant."})
        else:
            type = request.POST["type"]

            file = None
            if request.POST.get('file', True):
                file = request.FILES["file"]

            if file is not None:
                # Vérifier l'extension du fichier
                if not file.name.endswith('.pdf'):
                    return JsonResponse({
                        "status": "error",
                        "message": "Seuls les fichiers PDF sont acceptés."})
                # Limiter la taille du fichier à 10 Mo
                elif file.size > 10 * 1024 * 1024:
                    return JsonResponse({
                        "status": "error",
                        "message": "La taille du fichier est limité à 10 Mo."})
                else: 
                    liste_lms = Lettre_mot.objects.all()
                    liste_empreint_md5 = []
                    for l in liste_lms:
                        liste_empreint_md5.append(get_file_hash(l.file))
                        l.file.close()  # Fermer le fichier après le calcul du hash
                    
                    if get_file_hash(file) in liste_empreint_md5:
                        return JsonResponse({
                            "status": "error",
                            "message": "Cette lettre de motivation existe déjà."})
                    else:
                        # Vérifier si la lettre de motivation a un fichié associé et que le fichier existe réellement
                        if lm.file and hasattr(lm.file, 'path'):
                            #Suppression de la lettre de motivation et en même temps du fichier
                            # Chemin complet du fichier
                            file_path = lm.file.path
                            # Verifier l'existence du fichier
                            if os.path.exists(file_path):
                                os.remove(file_path)
                                
                    lm.file = file

            lm.type = type

            lm.save()
            return JsonResponse({
                "status": "success",
                "message": "Lettre de motivation modifiée avec succès."})

@login_required(login_url='connection/login')
def del_lm(request,id):
    try:
        lm_id = dechiffrer_param(str(id))
        lm = Lettre_mot.objects.get(id=lm_id)
    except:
        lm = None
    if lm:
        # Vérifier si la lettre de motivation a un fichié associé et que le fichier existe réellement
        if lm.file and hasattr(lm.file, 'path'):
            #Suppression de la lettre de motivation et en même temps du fichier
            # Chemin complet du fichier
            file_path = lm.file.path
            # Verifier l'existence du fichier
            if os.path.exists(file_path):
                os.remove(file_path)
        lm.delete()
    return redirect("lms")

@login_required(login_url='connection/login')
def delete_lm(request,id):
    try:
        lm_id = dechiffrer_param(str(id))
        lm = Lettre_mot.objects.get(id=lm_id)
    except:
        lm = None
    if lm:
        # Vérifier si la lettre de motivation a un fichié associé et que le fichier existe réellement
        if lm.file and hasattr(lm.file, 'path'):
            #Suppression de la lettre de motivation et en même temps du fichier 
            # Chemin complet du fichier
            file_path = lm.file.path
            # Verifier l'existence du fichier
            if os.path.exists(file_path):
                os.remove(file_path)
        lm.delete()
    return redirect("all_lms")


@login_required(login_url='connection/login')
def all_lms(request):
    date = datetime.datetime.now()
    
    lms = Lettre_mot.objects.select_related('user').all().order_by("-id")
    list_lms = []
    for lm in lms:
        dic = {}
        dic["lm"] = lm
        # Taille du fichier
        size = lm.file.size 
        # Conversion de la taille du fichier
        dic["size"] = taille_de_fichier(size)
        list_lms.append(dic)
        
    context = {
        "lms":list_lms,
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request),
        "parametre":parametre(),
        "date":date
    }
    return render(request, "all_lms.html", context)

@login_required(login_url='connection/login')
def cv_lm(request):
    date = datetime.datetime.now()
    context = {
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request),
        "parametre":parametre(),
        "date":date
    }
    return render(request, "cv_lm.html", context)

# Ajouter la taille du fichier à la lettre de motivation
def add_size_lm(lms):
    list_lm = []
    n = 0
    for lm in lms:
        n += 1
        dic = {}
        dic["lm"] = lm
        # Taille du fichier
        size = lm.file.size 
        # Conversion de la taille du fichier
        dic["size"] = taille_de_fichier(size)
        # Numerotation
        dic["n"] = n
        list_lm.append(dic) 
    return list_lm

def p_lms(request):
    date = datetime.datetime.now()

    lms = Lettre_mot.objects.select_related('user').filter(statut=1)
    files = []
    for lm in lms:
        files.append(lm.file)
    # Fusionner les fichiers
    merger = PdfMerger()
    for file in files:
        merger.append(file)
    # Sauvergarder les fichier dans le repertoire upload
    output_file = os.path.join(settings.MEDIA_ROOT, "upload", "merger.pdf")
    merger.write(output_file)
    merger.close()

    # Lettres de motivation puliées (avec statut = 1)
    lms_ins = Lettre_mot.objects.filter(type="Inscription", statut=1)
    lms_sta = Lettre_mot.objects.filter(type="Stage", statut=1)
    lms_alt = Lettre_mot.objects.filter(type="Alternance", statut=1)
    lms_emp = Lettre_mot.objects.filter(type="Emploi", statut=1)

    context = {
        "lms":lms,
        "lms_ins":add_size_lm(lms_ins),
        "lms_sta":add_size_lm(lms_sta),
        "lms_alt":add_size_lm(lms_alt),
        "lms_emp":add_size_lm(lms_emp),
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request),
        "parametre":parametre(),
        "date":date
    }
    return render(request, "p_lms.html", context)

class ajaxlm(View):
    def get(self, request, id, *args, **kwargs): 
        # Création de la session type_experience pour cacher ou afficher le formulaire
        status = request.session['status'] = id
        context = {
            "statut":status
        }
        return render(request, "ajaxlm.html", context)
    
@login_required(login_url='connection/login')
@csrf_exempt
def valid_lm(request,id):
    date = datetime.datetime.now()
    
    if request.method == "POST":
        id = request.POST["id"]
        lm = Lettre_mot.objects.get(id=id)
        if lm :
            lm.statut=request.POST["statut"]
            lm.comment=request.POST["comment"]
            lm.save()
            return redirect("all_lms")

    lm = Lettre_mot.objects.get(id=id)
    types = ["Inscription","Stage","Alternance","Emploi"]
    new_types = []
    for type in types:
        if lm.type != type:
            new_types.append(type)
            
    # Création de la session type_experience pour cacher ou afficher le formulaire
    request.session['status'] = lm.statut

    context = {
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request),
        "parametre":parametre(),
        "date":date,
        "lm":lm,
        "types":new_types,
    }
    return render(request, "valid_lm.html", context)
