# Importation des modules standard
import bleach
import re
import pdfkit
import base64

# Importation des modules tiers
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from datetime import datetime
from django.views import View
from django.db.models import Sum
from decimal import Decimal
from django.db import transaction
from django.http.response import HttpResponse
from django.template.loader import get_template
from django.contrib.sites.shortcuts import get_current_site

# Importation des modules locaux
from eajc.views import get_setting 
from eajcprojet.utils.crypto import dechiffrer_param
from .models import*
from contribution.models import Contribution


#========================== Contrat de remboursement ============================
@login_required(login_url='connection/login')
def contrats_remboursements(request):
    setting = get_setting()
    if setting is None:
        redirect("settings/maintenance")
        
    list_contrats = ContratRemboursement.objects.all().order_by("-id")
    contrats = []
    for contrat in list_contrats:
        dic = {}
        dic["contrat"] = contrat
        remboursements = contrat.remboursements.all()
        dic["remboursements"] = remboursements
        
        signatures = contrat.signaturecontrats.all()
        dic["signatures"] = signatures
        existence_signature = False
        if SignatureContrat.objects.filter(contratremboursement_id=contrat.id).exists():
            existence_signature = True
        
        dic["existence_signature"] = existence_signature
        
        # recuperer les actionnaires de ce projet
        contributions = Contribution.objects.filter(projet_id=contrat.projet.id)
        existence_actionnaire = False
        for contribution in contributions:
            if contribution.actionnaire.id == request.user.id:
                existence_actionnaire = True
        
        dic["existence_actionnaire"] = existence_actionnaire
        contrats.append(dic)
          
    paginator = Paginator(contrats, 10)
    num_page = request.GET.get('page')
    contrats = paginator.get_page(num_page)

    context = {
        "contrats": contrats,
        "setting": setting
    }
    return render(request, "contratremboursement/contrats_remboursements.html", context)


@login_required(login_url='connection/login')
def add_contrat_remboursement(request):
    
    user_id = request.user.id
    setting = get_setting()
    if setting is None:
        redirect("settings/maintenance")
    
    if request.method == "POST":
        projet_id = request.POST["projet"]
        description = bleach.clean(request.POST["description"].strip())
        date_debut = bleach.clean(request.POST["date_debut"].strip())
        date_fin = bleach.clean(request.POST["date_fin"].strip())
        montant_remboursement = bleach.clean(request.POST["montant_remboursement"].strip())
        date_contrat = bleach.clean(request.POST["date_contrat"].strip())
        
        # Conversion de date string en date pour mieux faire la comparaison
        date_format = "%Y-%m-%d"
        date_d = datetime.strptime(date_debut, date_format).date()
        # Récuperer le projet
        projet = get_object_or_404(Projet, id=projet_id)
        if date_d > projet.date_debut and date_d > projet.date_fin:
            
            if date_debut >= date_fin:
                return JsonResponse({
                    "status": "error",
                    "message": "Date de début doit être supérieure à la date de fin"})
            
            query = ContratRemboursement.objects.filter(projet=projet)
            if query.exists():
                return JsonResponse({
                    "status": "error",
                    "message": "Ce contrat existe déjà"})
            else:
                contrat = ContratRemboursement(
                    projet_id=projet_id,
                    description=description, 
                    date_debut=date_debut, 
                    date_fin=date_fin,
                    montant_remboursement=montant_remboursement,
                    date_contrat=date_contrat)
                # Nombre de contrats avant l'ajout
                count0 = ContratRemboursement.objects.all().count()
                contrat.save()
                # Nombre de contrats après l'ajout
                count1 = ContratRemboursement.objects.all().count()
                # On verifie si l'insertion a eu lieu ou pas.
                if count0 < count1:
                    return JsonResponse({
                        "status": "success",
                        "message": "Contrat enregistré avec succès."})
                else:
                    return JsonResponse({
                        "status": "error",
                        "message": "L'opération a échoué."})
        else:
            return JsonResponse({
                "status": "error",
                "message": "La date de début du contrat doit être supérieur à la date de fin du projet."})
            
    projets = Projet.objects.filter(responsable_id=user_id, type_projet="Individuel")
    context = {
        "setting": setting,
        "projets": projets
    }
    return render(request, "contratremboursement/add_contrat_remboursement.html", context)


@login_required(login_url='connection/login')
def edit_contrat_remboursement(request, id):
    setting = get_setting()
    if setting is None:
        redirect("settings/maintenance")
    
    contrat_id = int(dechiffrer_param(str(id)))    
    contrat = get_object_or_404(ContratRemboursement, id=contrat_id)

    projets = Projet.objects.filter(type_projet="Individuel").exclude(id=contrat.projet.id)
    context = {
            "setting": setting,
            "contrat": contrat,
            "projets": projets
    }
    return render(request, "contratremboursement/edit_contrat_remboursement.html", context)

@login_required(login_url='connection/login')
def edit_cr(request):
    if request.method == "POST":
        id = int(request.POST["id"])
        try:
            contrat = get_object_or_404(ContratRemboursement, id=id)
        except:
            contrat = None
        
        if contrat is None:
            return JsonResponse({
                    "status": "error",
                    "message": "Identifiant inexistant."})
        else:
            projet_id = request.POST["projet"]
            # Se proteger de l'attaque XSS(Injection du code javascript)
            description = bleach.clean(request.POST["description"].strip())
            date_debut = bleach.clean(request.POST["date_debut"].strip())
            date_fin = bleach.clean(request.POST["date_fin"].strip())
            montant_remboursement = bleach.clean(request.POST["montant_remboursement"].strip())
            
            # Nettoyer la valeur (supprimer les espaces et remplacer la virgule par un point)
            montant_remboursement = re.sub(r'\xa0', '', montant_remboursement)  # Supprime les espaces insécables
            montant_remboursement = montant_remboursement.replace(" ", "").replace(",", ".")
            

            try:
                montant_remboursement = Decimal(montant_remboursement)  # Convertir en Decimal
            except:
                return JsonResponse({
                    "status": "error",
                    "message": "Les coûts doivent être des nombres valides."})
            
            # Conversion de date string en date pour mieux faire la comparaison
            date_format = "%Y-%m-%d"
            date_d = datetime.strptime(date_debut, date_format).date()
            # Récuperer le projet
            projet = get_object_or_404(Projet, id=projet_id)
            if date_d > projet.date_fin:
                
                if date_debut > date_fin:
                    return JsonResponse({
                        "status": "error",
                        "message": "Date de début doit être supérieure à la date de fin"})
                
                #On exclut l que l'on veut modifier
                contrats = ContratRemboursement.objects.exclude(id=id)
                tabContrats = []
                for cont in contrats:
                    try:
                        tabContrats.append(cont.projet.id)
                    except Exception as e:
                        pass
                #On verifie si cette tâche existe déjà
                if projet_id in tabContrats:
                    return JsonResponse({
                        "status": "error",
                        "message": "Ce contrat existe déjà."})
                else:
                    contrat.projet_id = projet_id
                    contrat.description = description
                    contrat.date_debut = date_debut
                    contrat.date_fin = date_fin
                    contrat.montant_remboursement = montant_remboursement
                    contrat.save()
                    return JsonResponse({
                        "status": "success",
                        "message": "Contrat modifié avec succès."})
            else:
                return JsonResponse({
                    "status": "error",
                    "message": "La date de début et la date de fin d'une tâche doivent se situer entre la date de début et la date de fin du projet."})


@login_required(login_url='connection/login')
def del_contrat_remboursement(request, id):
    try: 
        contrat_id = int(dechiffrer_param(str(id))) 
        contrat = get_object_or_404(ContratRemboursement, id=contrat_id)
    except:
        contrat = None
        
    if contrat:
        contrat.delete()
    return redirect("contratremboursement/contrats_remboursements")


#=============================== Remboursement ======================

@login_required(login_url='connection/login')
def remboursements(request):
    setting = get_setting()
    if setting is None:
        redirect("settings/maintenance")
        
    contrats_rembouresements = (Remboursement.objects.values("contratremboursement_id").annotate(nb_contrat=Count("contratremboursement_id")))
    tabContratRemboursement = []
    for cr in contrats_rembouresements:
        contratremboursement = ContratRemboursement.objects.get(id=cr["contratremboursement_id"])
        dic = {}
        dic["contratremboursement"] = contratremboursement
        remboursements = contratremboursement.remboursements.all().order_by("actionnaire_id")
        tabRemboursements = []
        for remboursement in remboursements:
            new_dic = {}
            new_dic["remboursement"] = remboursement
            signatures = remboursement.signatureremboursements.all()
            new_dic["signatures"] = signatures
            tabRemboursements.append(new_dic)
        dic["remboursements"] = tabRemboursements
        # Existence de la signature de contrat de remboursement
        existence_signature = False
        if SignatureRemboursement.objects.filter(membre_id=request.user.id).exists():
            existence_signature = True
        
        dic["existence_signature"] = existence_signature  
        # Récuperer les signatures
        signatures = SignatureRemboursement.objects.filter()  
        # Calucler le remboursement total
        remboursement_total = Remboursement.objects.filter(contratremboursement_id=cr["contratremboursement_id"]).aggregate(Sum('montant_remboursement'))['montant_remboursement__sum'] or 0
        dic["remboursement_total"] = remboursement_total
        dic["reste_remboursement"] = contratremboursement.montant_remboursement - remboursement_total
        tabContratRemboursement.append(dic)
            
    paginator = Paginator(tabContratRemboursement, 10)
    num_page = request.GET.get('page')
    tabContratRemboursement = paginator.get_page(num_page)

    context = {
        "contrats": tabContratRemboursement,
        "setting": setting
    }
    return render(request, "remboursement/remboursements.html", context)

@login_required(login_url='connection/login')
def add_remboursement(request):
    
    setting = get_setting()
    if setting is None:
        redirect("settings/maintenance")
    
    if request.method == "POST":
        contratremboursement_id = request.POST["contratremboursement"]
        actionnaire = bleach.clean(request.POST["actionnaire"].strip())
        justification = bleach.clean(request.POST["justification"].strip())
        date_remboursement = bleach.clean(request.POST["date_remboursement"].strip())
        montant_remboursement = bleach.clean(request.POST["montant_remboursement"].strip())
        mode_paiement = bleach.clean(request.POST["mode_paiement"].strip())

        remboursement = Remboursement(
        contratremboursement_id= contratremboursement_id,
        actionnaire_id = actionnaire, 
        justification=justification, 
        date_remboursement=date_remboursement, 
        montant_remboursement=montant_remboursement,
        mode_paiement=mode_paiement)
        # Nombre de remboursements avant l'ajout
        count0 = Remboursement.objects.all().count()
        remboursement.save()
        # Nombre de remboursements après l'ajout
        count1 = Remboursement.objects.all().count()
        # On verifie si l'insertion a eu lieu ou pas.
        if count0 < count1:
            # Mettre à jour le statut du contrat de remboursement
            contratremboursement = get_object_or_404(ContratRemboursement, id=contratremboursement_id)
            contratremboursement.statut = "En cours"
            contratremboursement.save()
            
            return JsonResponse({
                    "status": "success",
                    "message": "remboursement enregistré avec succès."})
        else:
            return JsonResponse({
                    "status": "error",
                    "message": "L'opération a échoué."})
            
    contratremboursements = ContratRemboursement.objects.all()
    modes_paiements = ['Virement bancaire', 'PayPal', 'Espèces', 'Chèque']
    context = {
        "setting": setting,
        "contratremboursements": contratremboursements,
        "modes_paiements": modes_paiements
    }
    return render(request, "remboursement/add_remboursement.html", context)


@login_required(login_url='connection/login')
def edit_remboursement(request, id):
    setting = get_setting()
    if setting is None:
        redirect("settings/maintenance")
    
    remboursement_id = int(dechiffrer_param(str(id)))    
    remboursement = get_object_or_404(Remboursement, id=remboursement_id)

    contratremboursements = ContratRemboursement.objects.exclude(id=remboursement.contratremboursement.id)
    contributions = Contribution.objects.filter(projet_id=remboursement.contratremboursement.projet.id).exclude(actionnaire_id=remboursement.actionnaire.id)
    modes_paiements = ['Virement bancaire', 'PayPal', 'Espèces', 'Chèque']
    modes = [mode_paiement for mode_paiement in modes_paiements if mode_paiement != remboursement.mode_paiement]
    
    context = {
            "setting": setting,
            "remboursement": remboursement,
            "contratremboursements": contratremboursements,
            "contributions": contributions,
            "modes_paiements": modes
    }
    return render(request, "remboursement/edit_remboursement.html", context)


@login_required(login_url='connection/login')
def edit_remb(request):
    
    
    if request.method == "POST":
        
        id = int(request.POST["id"])
        try:
            remboursement = get_object_or_404(Remboursement, id=id)
        except:
            remboursement = None
        
        if remboursement is None:
            return JsonResponse({
                "status": "error",
                "message": "Identifiant inexistant."})
        else:            
            contratremboursement_id = request.POST["contratremboursement"]
            actionnaire = bleach.clean(request.POST["actionnaire"].strip())
            justification = bleach.clean(request.POST["justification"].strip())
            date_remboursement = bleach.clean(request.POST["date_remboursement"].strip())
            montant_remboursement = bleach.clean(request.POST["montant_remboursement"].strip())
            
            # Nettoyer la valeur (supprimer les espaces et remplacer la virgule par un point)
            montant_remboursement = re.sub(r'\xa0', '', montant_remboursement)  # Supprime les espaces insécables
            montant_remboursement = montant_remboursement.replace(" ", "").replace(",", ".")
            

            try:
                montant_remboursement = Decimal(montant_remboursement)  # Convertir en Decimal
            except:
                return JsonResponse({
                    "status": "error",
                    "message": "Les coûts doivent être des nombres valides."})

            
            remboursement.contratremboursement_id = contratremboursement_id
            remboursement.actionnaire_id = actionnaire
            remboursement.justification = justification
            remboursement.date_remboursement = date_remboursement 
            remboursement.montant_remboursement = montant_remboursement
            
            remboursement.save()
            
            return JsonResponse({
                        "status": "success",
                        "message": "Remboursement enregistré avec succès."})
                
                
@login_required(login_url='connection/login')
def del_remboursement(request, id):
    try:  
        remboursement_id = int(dechiffrer_param(str(id)))  
        remboursement = get_object_or_404(Remboursement, id=remboursement_id)
    except:
        remboursement = None
        
    if remboursement:
        remboursement.delete()
    return redirect("remboursement/remboursements")


def ajax_contrat_remboursement(request, contrat_id):
    contratremboursement = get_object_or_404(ContratRemboursement, id=contrat_id)
    contributions = Contribution.objects.filter(projet_id=contratremboursement.projet.id)
    context = {
        "contributions": contributions
    }
    return render(request, "ajax_contrat_remboursement.html", context)

def ajax_devise(request, projet_id):
    projet = get_object_or_404(Projet, id=projet_id)
    context = {
        "symbole": projet.devise.symbole
    }
    return render(request, "ajax_devise.html", context)

@transaction.atomic
def update_statut_remboursement(request):
    if request.method == "POST":
        remboursement_id = request.POST["id"]
        statut = bleach.clean(request.POST["statut"].strip())        
        #Recuperer le remboursement
        remboursement = get_object_or_404(Remboursement, id=remboursement_id)
        
        remboursement.statut = statut
        remboursement.save()
        
        if remboursement.statut == "Approuvé":
            # Ajouter la signature de remboursement ou la décharge
            signature = SignatureRemboursement(
                remboursement_id=remboursement_id,
                membre_id=request.user.id)
            
            signature.save()
        
        # récuperer le contrat
        contratremboursement = get_object_or_404(ContratRemboursement, id=remboursement.contratremboursement.id)
        # Mettre à jour le statut du contrat de remboursement    
        # montant total remboursé 
        montant_total_rembourse = Remboursement.objects.filter(contratremboursement_id=remboursement.contratremboursement.id).aggregate(Sum('montant_remboursement'))['montant_remboursement__sum'] or 0
        # liste des remboursements
        remboursements = Remboursement.objects.filter(contratremboursement_id=remboursement.contratremboursement.id)
        
        nb_remboursement = remboursements.count()
        nb_remb = 0
        for remb in remboursements:
            if remb.statut == "Approuvé": 
                nb_remb += 1
                
        if (montant_total_rembourse >= contratremboursement.montant_remboursement) and (nb_remboursement == nb_remb):
            contratremboursement.statut = "Terminé"
            contratremboursement.save()
        
        context = {
            "statut": remboursement.statut
        }
        return render(request, "update_statut_remboursement.html", context) 


# ============================ signature ============================
def add_signature(request):
    user_id = request.user.id
    if request.method == "POST":
        contratremboursement_id = request.POST["id"]  
        
        signature  = SignatureContrat(contratremboursement_id=contratremboursement_id, membre_id=user_id)
        # Nombre de signatures avant l'ajout
        count0 = SignatureContrat.objects.all().count()
        signature.save()
        # Nombre de signatures après l'ajout
        count1 = SignatureContrat.objects.all().count()
        # On verifie si l'insertion a eu lieu ou pas.
        if count0 < count1:        
            context = {
                "statut": "success",
                "contratremboursement_id": contratremboursement_id
            }
            return render(request, "signature/button-signature.html", context)  
        else:
            context = {
                "statut": "error" 
            }
            return render(request, "signature/button-signature.html", context)
        
        
@login_required(login_url='connection/login')
def document_signature_contrat(request, contrat_id):
    setting = get_setting()
    contratremboursement = get_object_or_404(ContratRemboursement, id=contrat_id)
    
    projet = get_object_or_404(Projet, id=contratremboursement.projet.id)
    signatures = SignatureContrat.objects.filter(contratremboursement_id=contrat_id)
    # Chemin vers notre image
    image_path = setting.logo

    # Lire l'image en mode binaire et encoder en Base64
    base64_string = base64.b64encode(image_path.read()).decode('utf-8')

    context = {
        "base64_image": base64_string,
        "setting": setting,
        "contratremboursement": contratremboursement,
        "projet": projet,
        "signatures" : signatures,
        'domain':get_current_site(request).domain
    }
    template = get_template("signature/document_signature_contrat.html")
    html = template.render(context)
    options = {
        'page-size': 'Letter',
        'encoding': "UTF-8",
    }
    pdf = pdfkit.from_string(html, False, options)
    reponse = HttpResponse(pdf, content_type='application/pdf')
    reponse['Content-Disposition'] = f"attachment; filename=Contrat_{request.user.last_name }_{ request.user.first_name }.pdf"
    return reponse


@login_required(login_url='connection/login')
def document_decharge_remboursement(request, remboursement_id):
    setting = get_setting()
    id = int(dechiffrer_param(str(remboursement_id)))
    remboursement = get_object_or_404(Remboursement, id=id)
 
    projet = get_object_or_404(Projet, id=remboursement.contratremboursement.projet.id)
    # Chemin vers notre image
    image_path = setting.logo

    # Lire l'image en mode binaire et encoder en Base64
    base64_string = base64.b64encode(image_path.read()).decode('utf-8')

    context = {
        "base64_image": base64_string,
        "setting": setting,
        "remboursement": remboursement,
        "projet": projet,
        'domain':get_current_site(request).domain
    }
    template = get_template("signature/document_decharge_remboursement.html")
    html = template.render(context)
    options = {
        'page-size': 'Letter',
        'encoding': "UTF-8",
    }
    pdf = pdfkit.from_string(html, False, options)
    reponse = HttpResponse(pdf, content_type='application/pdf')
    reponse['Content-Disposition'] = f"attachment; filename=Decharge_{request.user.last_name }_{ request.user.first_name }.pdf"
    return reponse
