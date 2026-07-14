# Importation des modules standards
import bleach
import re
import base64
import pdfkit
# Importation des modules tiers
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count, Sum
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from decimal import Decimal
from datetime import date
from django.db import transaction
from django.http.response import HttpResponse
from django.template.loader import get_template
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
# Importation des modules locaux
from .models import Renumeration, Contrat, RenumerationAdmin
from emargement.models import Emargement
from salle.models import Salle
from matiere.models import Matiere
from enseignement.models import Enseigner
from paiement.models import Payment
from depense.models import Depense
from anneeacademique.models import AnneeCademique
from inscription.models import Inscription
from school.views import get_setting
from app_auth.decorator import allowed_users

permission_gestionnaire = ['Promoteur', 'Directeur Général', 'Gestionnaire']
permission_gestionnaire_enseignant = ['Promoteur', 'Directeur Général', 'Gestionnaire', 'Enseignant']
permission_enseignant = ['Enseignant']
permission_gestionnaire_admin = ['Promoteur', 'Directeur Général', 'Directeur des Etudes', 'Gestionnaire']
permission_users = ['Promoteur', 'Directeur Général', 'Directeur des Etudes', 'Gestionnaire', 'Enseignant']

@login_required(login_url='connection/login')  
@allowed_users(allowed_roles=permission_gestionnaire)
def renumerations(request):
    setting = get_setting()
    if setting is None:
        return redirect("settings/maintenance")
 
    anneeacademique_id = request.session.get('anneeacademique_id')
        
    months_emargements = (Emargement.objects.values("month")
                       .filter(anneeacademique_id=anneeacademique_id)
                       .annotate(nb_emargements=Count("month")))
        
    months = []
    for me in months_emargements:
        months.append(me["month"])
        
    context = {
        "setting": setting,
        "months": months
    }
    
    return render(request, "renumerations.html", context)

@login_required(login_url='connection/connexion')  
@allowed_users(allowed_roles=permission_gestionnaire)
def personnel_renumeration(request):
    anneeacademique_id = request.session.get('anneeacademique_id')
    setting = get_setting(anneeacademique_id)
    if setting is None:
        return redirect("settings/maintenance")
        
    months_emargements = (Emargement.objects.values("month")
                       .filter(anneeacademique_id=anneeacademique_id)
                       .annotate(nb_emargements=Count("month")))
        
    months = []
    for me in months_emargements:
        months.append(me["month"])
        
    context = {
        "setting": setting,
        "months": months
    }
    
    return render(request, "personnel_renum.html", context)

def get_personnel_renumeration(request, month):
    anneeacademique_id = request.session.get('anneeacademique_id')
    setting = get_setting(anneeacademique_id)
    personnels_emargements = (Emargement.objects.values("enseignant_id")
                              .filter(month=month)
                              .annotate(nb_emargements=Count("enseignant_id")))
    
    renumerations= []
    for pe in personnels_emargements:
        dic = {}
        enseignant_id = pe["enseignant_id"]
        enseignant = User.objects.get(id=enseignant_id)
        dic["enseignant"] = enseignant
        renumeration = Renumeration.objects.filter(personnel_id=enseignant_id, month=month, anneeacademique_id=anneeacademique_id)
        if renumeration.exists():
            dic["status"] = "Payé"
        else:
            dic["status"] = "En cours"
        
        renumerations.append(dic)
        
    administrateurs = User.objects.filter(is_superuser=True)
    
    renumerations_admin = []
    for admin in administrateurs:
        dic = {}
        dic["administrateur"] = admin

        anneeacademique_id = request.session.get('anneeacademique_id')
        renumeration = RenumerationAdmin.objects.filter(user_id=admin.id, month=month, anneeacademique_id=anneeacademique_id)
        if renumeration.exists():
            dic["status"] = "Payé"
        else:
            dic["status"] = "En cours"
        renumerations_admin.append(dic)
        
    context = {
        "month": month,
        "renumerations": renumerations,
        "renumerations_admin": renumerations_admin,
        "setting": setting
    }       
    return render(request, "ajax_pers_renum.html", context)

def get_teacher_renumeration(request, month):
    anneeacademique_id = request.session.get('anneeacademique_id')
    setting = get_setting(anneeacademique_id)
    if setting is None:
        return redirect("settings/maintenance")

    renumerations = Renumeration.objects.filter(month=month, anneeacademique_id=anneeacademique_id)
    
    tabRenumerations= []
    somme_totale = 0
    for renumeration in renumerations:
        dic = {}
        dic["renumeration"] = renumeration
        dic["net_payer"] = float(renumeration.amount) + float(renumeration.indeminte)   
        tabRenumerations.append(dic)
        
        somme_totale += float(renumeration.amount) + float(renumeration.indeminte)
        
    renumerations_admin = RenumerationAdmin.objects.filter(month=month, anneeacademique_id=anneeacademique_id)
    
    tabRenumerations_admin= []
    somme_totale_admin = 0
    for renumeration in renumerations_admin:
        dic = {}
        dic["renumeration"] = renumeration
        dic["net_payer"] = float(renumeration.amount) + float(renumeration.indemnite)   
        tabRenumerations_admin.append(dic)
        
        somme_totale_admin += float(renumeration.amount) + float(renumeration.indemnite)
    
    total = somme_totale + somme_totale_admin    
    context = {
        "month": month,
        "renumerations": tabRenumerations,
        "sum_total" : somme_totale,
        "renumerations_admin": tabRenumerations_admin,
        "sum_total_admin" : somme_totale_admin,
        "total": total,
        "setting": setting
    }       
    return render(request, "ajax_teacher_renum.html", context)

# Formatter le temps  
def format_time(time):
    # Extraire les heures et les minutes en normalisant (si la somme dépasse 24 heures)
    total_matiere_seconds = time.total_seconds()
    total_matiere_hours = int(total_matiere_seconds // 3600) % 24  # Récupérer les heures (modulo 24 pour ne pas dépasser une journée)
    total_matiere_minutes = int((total_matiere_seconds % 3600) // 60)

    # Afficher le résultat au format HH:MM
    formatted_time = f"{total_matiere_hours:02}:{total_matiere_minutes:02}"   
    return formatted_time

# Calculter le salaire
def calculer_montant(cout_heure, heure_totale):
    """ Si 60min -> cout_heure
           15min -> x
           x = (15min * cout_heure) / 60min
    """
    heure_min = heure_totale.split(":")
    heure = heure_min[0]
    minute = heure_min[1]
    cout_min = (float(minute) * float(cout_heure))/60
    
    amount = float(cout_min) + float(heure)*float(cout_heure)
    return round(amount, 2)   

def recap_emargement(request, enseignant_id, month):
    anneeacademique_id = request.session.get('anneeacademique_id')
    setting = get_setting(anneeacademique_id)
    if setting is None:
        return redirect("settings/maintenance")

    salles_emargements = (Emargement.objects.values("salle_id")
                   .filter(enseignant_id=enseignant_id, month=month, anneeacademique_id=anneeacademique_id)
                   .annotate(nb_emargements=Count("salle_id")))
    
    tabEmargements = []
    total_salle_delta = timedelta(0)
    montant_payer = 0
    somme_cout_heure = 0
    for se in salles_emargements:
        dic = {}
        salle_id = se["salle_id"]
        salle = Salle.objects.get(id=salle_id)
        dic["salle"] = salle
        
        matieres_emargements = (Emargement.objects.values("matiere_id")
                   .filter(enseignant_id=enseignant_id, salle_id=salle_id, month=month, anneeacademique_id=anneeacademique_id)
                   .annotate(nb_emargements=Count("matiere_id")))
        
        matieres = []
        total_matiere_delta = timedelta(0)
        for me in matieres_emargements:
            dic_matiere = {}
            matiere_id = me["matiere_id"]
            matiere = Matiere.objects.get(id=matiere_id)
            dic_matiere["matiere"] = matiere    
            
            # Recupérer le cout par heure de cette matière
            enseignement = Enseigner.objects.filter(
                enseignant_id=enseignant_id, 
                salle_id=salle_id, 
                matiere_id=matiere_id, 
                anneeacademique_id=anneeacademique_id).first()
            dic_matiere["cout_heure"] = enseignement.cout_heure
            
            somme_cout_heure += enseignement.cout_heure
            
            emargements = Emargement.objects.filter(enseignant_id=enseignant_id, month=month, salle_id=salle_id, matiere_id=matiere_id, anneeacademique_id=anneeacademique_id)
            # Initialisation avec une durée nulle
            total_delta = timedelta(0)
            list_emargements = []
            for em in emargements:
                dic_em = {}
                dic_em["emargement"] = em
                # Convertir les objets time en timedelta
                start_delta = timedelta(hours=em.heure_debut.hour, minutes=em.heure_debut.minute)
                end_delta = timedelta(hours=em.heure_fin.hour, minutes=em.heure_fin.minute)
                # Calculer la somme des deux
                total_delta +=  end_delta - start_delta
                    
                dic_em["hour"] = format_time(total_delta)
                
                list_emargements.append(dic_em)     
            
            dic_matiere["emargements"] = list_emargements        
            
            dic_matiere["total_time"] = format_time(total_delta)
            
            # Calculer le montant à payer pour cette matière
            dic_matiere["montant_total_matiere"] = calculer_montant(enseignement.cout_heure, format_time(total_delta))
            
            total_matiere_delta += total_delta
            
            matieres.append(dic_matiere)
        
        dic["total_matiere_time"] = format_time(total_matiere_delta)
        dic["matieres"] = matieres
        
        montant_total = calculer_montant(somme_cout_heure, format_time(total_matiere_delta))
        dic["montant_total_salle"] = montant_total
        tabEmargements.append(dic)
        total_salle_delta += total_matiere_delta
        
        montant_payer += montant_total
        
    time_total = format_time(total_salle_delta)
        
    enseignant = User.objects.get(id=enseignant_id)
    # Verifier si l'enseignant a déjà été rénuméré ou pas
    query = Renumeration.objects.filter(personnel_id=enseignant_id, month=month, anneeacademique_id=anneeacademique_id)
    status_paye = False
    renumeration = query.first()
    net_payer = 0
    if query.exists():
        status_paye = True
        # Calculer le net
        net_payer = float(renumeration.amount) + float(renumeration.indeminte)  
         
    context = {
        "setting": setting,
        "emargements": tabEmargements,
        "enseignant": enseignant,
        "month": month,
        "time_total": time_total,
        "montant_payer": montant_payer,
        "status_paye": status_paye,
        "renumeration": renumeration,
        "net_payer": net_payer
    }       
    return render(request, "recap_emargement.html", context) 

# Calculer de l'enseignant le montant à payer 
def montant_payer(anneeacademique_id, enseignant_id, month):
    
    salles_emargements = (Emargement.objects.values("salle_id")
                   .filter(enseignant_id=enseignant_id, month=month, anneeacademique_id=anneeacademique_id)
                   .annotate(nb_emargements=Count("salle_id")))
    
    tabEmargements = []
    total_salle_delta = timedelta(0)
    montant_payer = 0
    for se in salles_emargements:
        dic = {}
        salle_id = se["salle_id"]
        salle = Salle.objects.get(id=salle_id)
        dic["salle"] = salle
        
        matieres_emargements = (Emargement.objects.values("matiere_id")
                   .filter(enseignant_id=enseignant_id, salle_id=salle_id, month=month, anneeacademique_id=anneeacademique_id)
                   .annotate(nb_emargements=Count("matiere_id")))
        
        matieres = []
        total_matiere_delta = timedelta(0)
        for me in matieres_emargements:
            dic_matiere = {}
            matiere_id = me["matiere_id"]
            matiere = Matiere.objects.get(id=matiere_id)
            dic_matiere["matiere"] = matiere    
            
            # Recupérer le cout par heure de cette matière
            enseignement = Enseigner.objects.filter(enseignant_id=enseignant_id, salle_id=salle_id, matiere_id=matiere_id, anneeacademique_id=anneeacademique_id).first()
            dic_matiere["cout_heure"] = enseignement.cout_heure
            
            emargements = Emargement.objects.filter(enseignant_id=enseignant_id, month=month, salle_id=salle_id, matiere_id=matiere_id, anneeacademique_id=anneeacademique_id)
            # Initialisation avec une durée nulle
            total_delta = timedelta(0)
            list_emargements = []
            for em in emargements:
                dic_em = {}
                dic_em["emargement"] = em
                # Convertir les objets time en timedelta
                start_delta = timedelta(hours=em.heure_debut.hour, minutes=em.heure_debut.minute)
                end_delta = timedelta(hours=em.heure_fin.hour, minutes=em.heure_fin.minute)
                # Calculer la somme des deux
                total_delta +=  end_delta - start_delta
                    
                dic_em["hour"] = format_time(total_delta)
                
                list_emargements.append(dic_em)     
            
            dic_matiere["emargements"] = list_emargements        
            
            dic_matiere["total_time"] = format_time(total_delta)
            
            # Calculer le montant à payer pour cette matière
            dic_matiere["montant_total_matiere"] = calculer_montant(enseignement.cout_heure, format_time(total_delta))
            
            total_matiere_delta += total_delta
            
            matieres.append(dic_matiere)
        
        dic["total_matiere_time"] = format_time(total_matiere_delta)
        dic["matieres"] = matieres
        
        montant_total = calculer_montant(enseignement.cout_heure, format_time(total_matiere_delta))
        dic["montant_total_salle"] = montant_total
        tabEmargements.append(dic)
        total_salle_delta += total_matiere_delta
        
        montant_payer += montant_total
        
    time_total = format_time(total_salle_delta)
    
    return time_total, montant_payer
    

@login_required(login_url='connection/connexion')
@allowed_users(allowed_roles=permission_gestionnaire)
def add_renumeration(request, enseignant_id, month):
    anneeacademique_id = request.session.get('anneeacademique_id')
    setting = get_setting(anneeacademique_id)
    if setting is None:
        return redirect("settings/maintenance")

    enseignant = User.objects.get(id=enseignant_id)
    total_time, mont_payer = montant_payer(anneeacademique_id, enseignant_id, month)
    context = {
        "setting": setting,
        "enseignant": enseignant,
        "month": month,
        "montant": mont_payer,
        "total_time": total_time
    }
    return render(request, "add_renumeration.html", context)

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=permission_gestionnaire)
def add_renum(request):
    user_id = request.user.id
    anneeacademique_id = request.session.get('anneeacademique_id')
    if request.method == "POST":
        enseignant_id = int(request.POST["enseignant"])
        month = request.POST["month"]
        amount = bleach.clean(request.POST["amount"].strip())
        indeminte = bleach.clean(request.POST["indemnite"].strip())
        
        amount_total = float(amount) + float(indeminte)
        
        query = Renumeration.objects.filter(personnel_id=enseignant_id, month=month, anneeacademique_id=anneeacademique_id)
        # Récuperer la délibération pour verifier si ses activités ont été cloturées ou pas
        anneescolaire = AnneeCademique.objects.filter(status_cloture=True, id=anneeacademique_id) 
        if anneescolaire.exists(): # Verifier si on a déjà cloturé les opérations de cette année
                return JsonResponse({
                    "status": "error",
                    "message": "Les opérations de cette année académique ont été déjà clôturées."}) 
        if query.exists():
            return JsonResponse({
                    "status": "error",
                    "message": "Cette rénumeration existe déjà."})
        else:
            renumeration = Renumeration(
                anneeacademique_id=anneeacademique_id,
                personnel_id=enseignant_id,
                month=month,
                amount=amount,
                indeminte=indeminte,
                total_amount=amount_total,
                user_id=user_id 
            )
            count0 = Renumeration.objects.all().count()
            renumeration.save()
            count1 = Renumeration.objects.all().count()
            # Verifier si l'ajout a été bien effectué ou pas
            if count0 < count1:
                return JsonResponse({
                        "status": "success",
                        "message": "Rénumération effectuée avec succès."})
            else:   
                return JsonResponse({
                        "status": "error",
                        "message": "L'opérations a échouée."})

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=permission_enseignant)
def mes_renumerations(request):
    user_id = request.user.id
    anneeacademique_id = request.session.get('anneeacademique_id')
    setting = get_setting(anneeacademique_id)
    if setting is None:
        return redirect("settings/maintenance")
    
    renumerations = Renumeration.objects.filter(personnel_id=user_id, anneeacademique_id=anneeacademique_id)
    
    tabrenumerations = []
    for renumeration in renumerations:
        dic_renum = {}
        dic_renum["renumeration"] = renumeration
        salles_emargements = (Emargement.objects.values("salle_id")
                    .filter(enseignant_id=user_id, month=renumeration.month, anneeacademique_id=anneeacademique_id)
                    .annotate(nb_emargements=Count("salle_id")))
    
        tabEmargements = []
        total_salle_delta = timedelta(0)
        montant_payer = 0
        somme_cout_heure = 0
        for se in salles_emargements:
            dic = {}
            salle_id = se["salle_id"]
            salle = Salle.objects.get(id=salle_id)
            dic["salle"] = salle
            
            matieres_emargements = (Emargement.objects.values("matiere_id")
                    .filter(enseignant_id=user_id, salle_id=salle_id, month=renumeration.month, anneeacademique_id=anneeacademique_id)
                    .annotate(nb_emargements=Count("matiere_id")))
            
            matieres = []
            total_matiere_delta = timedelta(0)
            for me in matieres_emargements:
                dic_matiere = {}
                matiere_id = me["matiere_id"]
                matiere = Matiere.objects.get(id=matiere_id)
                dic_matiere["matiere"] = matiere    
                
                # Recupérer le cout par heure de cette matière
                enseignement = Enseigner.objects.filter(
                    enseignant_id=user_id, 
                    salle_id=salle_id, 
                    matiere_id=matiere_id, 
                    anneeacademique_id=anneeacademique_id).first()
                dic_matiere["cout_heure"] = enseignement.cout_heure
                
                somme_cout_heure += enseignement.cout_heure
                
                emargements = Emargement.objects.filter(enseignant_id=user_id, month=renumeration.month, salle_id=salle_id, matiere_id=matiere_id, anneeacademique_id=anneeacademique_id)
                # Initialisation avec une durée nulle
                total_delta = timedelta(0)
                list_emargements = []
                for em in emargements:
                    dic_em = {}
                    dic_em["emargement"] = em
                    # Convertir les objets time en timedelta
                    start_delta = timedelta(hours=em.heure_debut.hour, minutes=em.heure_debut.minute)
                    end_delta = timedelta(hours=em.heure_fin.hour, minutes=em.heure_fin.minute)
                    # Calculer la somme des deux
                    total_delta +=  end_delta - start_delta
                        
                    dic_em["hour"] = format_time(total_delta)
                    
                    list_emargements.append(dic_em)     
                
                dic_matiere["emargements"] = list_emargements        
                
                dic_matiere["total_time"] = format_time(total_delta)
                
                # Calculer le montant à payer pour cette matière
                dic_matiere["montant_total_matiere"] = calculer_montant(enseignement.cout_heure, format_time(total_delta))
                
                total_matiere_delta += total_delta
                
                matieres.append(dic_matiere)
            
            dic["total_matiere_time"] = format_time(total_matiere_delta)
            dic["matieres"] = matieres
            
            montant_total = calculer_montant(somme_cout_heure, format_time(total_matiere_delta))
            dic["montant_total_salle"] = montant_total
            
            montant_total 
            
            tabEmargements.append(dic)
            
            total_salle_delta += total_matiere_delta
            
            montant_payer += montant_total
            
        dic_renum["emargements"] = tabEmargements
        dic_renum["time_total"] = format_time(total_salle_delta)
        dic_renum["montant_total"] = montant_payer
        dic_renum["net_payer"] = float(renumeration.amount) + float(renumeration.indeminte) 
        
        tabrenumerations.append(dic_renum)
        
        # Mise à jour du status de paiement de l'enseignant pour marquer la lecture
        renumeration.status = True
        renumeration.save()
       
    context = {
        "renumerations": tabrenumerations,
        "setting": setting
    }       
    return render(request, "mes_renumerations.html", context)     
        
#================== Gestion de contrats =================================
def status_contrat(contrat):
    # Date actuelle
    date_actuelle = date.today()
    status = "En attente"
    if contrat:
        if date_actuelle < contrat.date_debut:
            status = "En attente"
        elif contrat.date_debut <= date_actuelle and  date_actuelle <= contrat.date_fin:
            status = "En cours"
        if contrat.date_fin < date_actuelle:
            status = "Terminé"
    return status

# Statut du contrat
def status_contrat_user(user_id, anneeacademique_id):
    contrat = Contrat.objects.filter(user_id=user_id, anneeacademique_id=anneeacademique_id).order_by("-id").first()
    print(contrat)
    return status_contrat(contrat)

# Determiner les mois du contrat de l'utilisateur
def month_contrat_user(contrat):   

    start_date = contrat.date_debut
    end_date = contrat.date_fin 

    # Génération des mois dans l'intervalle
    months = []
    current_date = start_date.replace(day=1)  # S'assurer de commencer au début du mois

    while current_date <= end_date:
        months.append(current_date.strftime("%m"))
        # Passer au mois suivant
        next_month = current_date.month % 12 + 1
        next_year = current_date.year + (1 if current_date.month == 12 else 0)
        current_date = current_date.replace(month=next_month, year=next_year)

    month_format = []
    for month in months:
        if month == '01':
            month_format.append("Janvier")
        elif month == '02':
            month_format.append("Février")
        elif month == '03':
            month_format.append("Mars")
        elif month == '04':
            month_format.append("Avril")
        elif month == '05':
            month_format.append("Mai")
        elif month == '06':
            month_format.append("Juin")
        elif month == '07':
            month_format.append("Juillet")
        elif month == '08':
            month_format.append("Août")
        elif month == '09':
            month_format.append("Septembre")
        elif month == '10':
            month_format.append("Octobre")
        elif month == '11':
            month_format.append("Novembre")
        else:
            month_format.append("Décembre")
    return month_format  # Retourne la liste des mois
    
@login_required(login_url='connection/login')
@allowed_users(allowed_roles=permission_gestionnaire)
def contrats(request):
    anneeacademique_id = request.session.get('anneeacademique_id')
    setting = get_setting(anneeacademique_id)
    if setting is None:
        return redirect("settings/maintenance")

    contrats_users = (Contrat.objects.values("user_id")
                      .filter(anneeacademique_id=anneeacademique_id)
                      .annotate(nb_contrats=Count("user_id"))
    )
    tabcontrats = []
    for cu in contrats_users:
        user = User.objects.get(id=cu["user_id"])   
        dic = {}
        dic["user"] = user
        liste_contrats = Contrat.objects.filter(user_id=user.id, anneeacademique_id=anneeacademique_id).order_by("-date_fin")
        contrats = []
        for contrat in liste_contrats:
            new_dic = {}
            new_dic["contrat"] = contrat
            new_dic["status"] = status_contrat(contrat)
            contrats.append(new_dic)
            
        dic["contrats"] = contrats
        dic["nb_contrats"] = cu["nb_contrats"]
        # Récuperer le dernier contrat de l'utilisateur pour determiner son statut
        dernier_contrat = Contrat.objects.filter(user_id=user.id, anneeacademique_id=anneeacademique_id).order_by("-date_fin").first()
        dic["status"] = status_contrat(dernier_contrat)
        tabcontrats.append(dic)

    anneeacademique = AnneeCademique.objects.get(id=anneeacademique_id)
    context = {
        "setting": setting,
        "contrats": tabcontrats,
        "anneeacademique": anneeacademique
    }
    return render(request, "contrat/contrats.html", context)    

@login_required(login_url='connection/login')
@transaction.atomic
@allowed_users(allowed_roles=permission_gestionnaire)
def add_contrat(request):
    anneeacademique_id = request.session.get('anneeacademique_id')
    setting = get_setting(anneeacademique_id)
    if setting is None:
        return redirect("settings/maintenance")
    
    if request.method == "POST":

        user_id = request.POST["user"]
        type_contrat = request.POST["type_contrat"]
        poste = bleach.clean(request.POST["poste"].strip())
        description = bleach.clean(request.POST["description"].strip())
        date_debut = request.POST["date_debut"]
        date_fin = request.POST["date_fin"]
        amount = bleach.clean(request.POST["amount"].strip())
        
        # Nettoyer la valeur (supprimer les espaces et remplacer la virgule par un point)
        amount = re.sub(r'\xa0', '', amount)  # Supprime les espaces insécables
        amount = amount.replace(" ", "").replace(",", ".")

        try:
            amount = Decimal(amount)  # Convertir en Decimal
        except:
            return JsonResponse({
                "status": "error",
                "message": "Le montant doit être un nombre valide."})
        
        # Récuperer la délibération pour verifier si ses activités ont été cloturées ou pas
        anneescolaire = AnneeCademique.objects.filter(status_cloture=True, id=anneeacademique_id)          
        query = Contrat.objects.filter(user_id=user_id, date_debut=date_debut, date_fin=date_fin, anneeacademique_id=anneeacademique_id)
        # Récuperer le dernier contrat de cette année scolaire de l'utilisateur pour verifier si la date de fin du dernier est inférieure à la date de debut du nouveau contrata
        dernier_contrat = Contrat.objects.filter(user_id=user_id, anneeacademique_id=anneeacademique_id).order_by("-id").first() 
        
        if anneescolaire.exists(): # Verifier si on a déjà cloturé les opérations de cette année
                return JsonResponse({
                    "status": "error",
                    "message": "Les opérations de cette année académique ont été déjà clôturées."})  
        if dernier_contrat: # Récuperer le statut du dernier contrat pour vérifier s'il est déjà terminé pour enregistrer un nouveau
            status_contrat = status_contrat_user(user_id, anneeacademique_id)
            if status_contrat not in ["Terminé"]:
                return JsonResponse({
                    "status": "error",
                    "message": "Le dernier contrat de cet utilisateur doit d'abord terminer pour enrgistrer un nouveau contrat."})
            if dernier_contrat.date_fin > datetime.strptime(date_debut, "%Y-%m-%d").date(): # Conversion de la date début (str) en date
                return JsonResponse({
                    "status": "error",
                    "message": "La date de fin du dernier contrat de cet utilisateur doit être inférieure à la date de début du nouvaeu contrat."})
            if date_debut > date_fin:
                return JsonResponse({
                    "status": "error",
                    "message": "La date du début doit être inférieure ou égale à la date de fin."})
            if query.exists():
                return JsonResponse({
                        "status": "error",
                        "message": "Ce contrat existe déjà."})
            else:
                contrat = Contrat(
                    user_id=user_id, 
                    type_contrat=type_contrat, 
                    poste=poste,
                    description=description,
                    date_debut=date_debut,
                    date_fin=date_fin, 
                    amount=amount,
                    anneeacademique_id=anneeacademique_id,
                    admin_id=request.user.id)
                # Nombre de contrats avant l'ajout
                count0 = Contrat.objects.all().count()
                contrat.save()
                # Nombre de contrats après l'ajout
                count1 = Contrat.objects.all().count()
                # On verifie si l'insertion a eu lieu ou pas.
                if count0 < count1:
                    return JsonResponse({
                            "status": "success",
                            "message": "Contrat et la signature enregistrés avec succès."})
                else:
                    return JsonResponse({
                            "status": "error",
                            "message": "Insertion a échouée."})
        else:
            if date_debut > date_fin:
                return JsonResponse({
                    "status": "error",
                    "message": "La date du début doit être inférieure ou égale à la date de fin."})
            if query.exists():
                return JsonResponse({
                        "status": "error",
                        "message": "Ce contrat existe déjà."})
            else:
                contrat = Contrat(
                    user_id=user_id, 
                    type_contrat=type_contrat, 
                    poste=poste,
                    description=description,
                    date_debut=date_debut,
                    date_fin=date_fin, 
                    amount=amount,
                    anneeacademique_id=anneeacademique_id,
                    admin_id=request.user.id)
                # Nombre de contrats avant l'ajout
                count0 = Contrat.objects.all().count()
                contrat.save()
                # Nombre de contrats après l'ajout
                count1 = Contrat.objects.all().count()
                # On verifie si l'insertion a eu lieu ou pas.
                if count0 < count1:
                    return JsonResponse({
                            "status": "success",
                            "message": "Contrat enregistré avec succès."})
                else:
                    return JsonResponse({
                            "status": "error",
                            "message": "Insertion a échouée."})
                

    users = User.objects.all()

    context = {
        "setting": setting,
        "users": users
    }
    return render(request, "contrat/add_contrat.html", context)


@login_required(login_url='connection/login')
@allowed_users(allowed_roles=permission_gestionnaire)
def edit_contrat(request,id):
    anneeacademique_id = request.session.get('anneeacademique_id')
    setting = get_setting(anneeacademique_id)
    if setting is None:
        return redirect("settings/maintenance")
    
    contrat = Contrat.objects.get(id=id)
        
    users = User.objects.exclude(id=contrat.user.id)

    context = {
        "setting": setting,
        "users": users,
        "contrat": contrat
    }
    return render(request, "contrat/edit_contrat.html", context)
   

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=permission_gestionnaire)
def edit_ct(request):
    anneeacademique_id = request.session.get('anneeacademique_id')
    if request.method == "POST":
        id = int(request.POST["id"])
        try:
            contrat = Contrat.objects.get(id=id)
        except:
            contrat = None

        if contrat is None:
            return JsonResponse({
                    "status": "error",
                    "message": "Identifiant inexistant."})
        else: 
            user_id = request.POST["user"]
            type_contrat = request.POST["type_contrat"]
            poste = bleach.clean(request.POST["poste"].strip())
            description = bleach.clean(request.POST["description"].strip())
            date_debut = request.POST["date_debut"]
            date_fin = request.POST["date_fin"]
            amount = bleach.clean(request.POST["amount"].strip())
            
            # Récuperer la délibération pour verifier si ses activités ont été cloturées ou pas
            anneescolaire = AnneeCademique.objects.filter(status_cloture=True, id=anneeacademique_id) 
            # Recuperer tous contrats existants pour verifier s'il existe déjà un contrat à ces dates
            contrats = Contrat.objects.filter(user_id=user_id).exclude(id=id)
            status_date = False # Indique s'il existe déjà un contrat avec la date renseignée
            for contrat in contrats:
                date_d = datetime.strptime(date_debut, "%Y-%m-%d").date() # Conversion de la date début (str) en date  
                date_f = datetime.strptime(date_fin, "%Y-%m-%d").date() # Conversion de la date fin (str) en date  
                if (contrat.date_debut <= date_d and date_d <= contrat.date_fin) or (contrat.date_debut <= date_f and date_f <= contrat.date_fin):
                    status_date = True
                    break           
            
            # Nettoyer la valeur (supprimer les espaces et remplacer la virgule par un point)
            amount = re.sub(r'\xa0', '', amount)  # Supprime les espaces insécables
            amount = amount.replace(" ", "").replace(",", ".")

            try:
                amount = Decimal(amount)  # Convertir en Decimal
            except:
                return JsonResponse({
                    "status": "error",
                    "message": "Le montant doit être un nombre valide."})
            # Vérifier l'existence du contrat
            contrats = Contrat.objects.filter(date_debut=date_debut, date_fin=date_fin, user_id=user_id, anneeacademique_id=anneeacademique_id).exclude(id=id)
            tabContrat = []
            for c in contrats:   
                dic = {}
                dic["user_id"] = c.user.id
                dic["date_debut"] = c.date_debut
                dic["date_fin"] = c.date_fin
                dic["anneeacademique_id"] = c.anneeacademique.id
                tabContrat.append(dic)            
                
            new_dic = {}
            new_dic["user_id"] = int(user_id)
            new_dic["date_debut"] = date_debut
            new_dic["date_fin"] = date_fin
            new_dic["anneeacademique_id"] = int(anneeacademique_id)
            if anneescolaire.exists(): # Verifier si on a déjà cloturé les opérations de cette année
                return JsonResponse({
                    "status": "error",
                    "message": "Les opérations de cette année académique ont été déjà clôturées."})  
            if status_date :
                return JsonResponse({
                    "status": "error",
                    "message": "Un autre contrat existe déjà avec les dates renseignées."})
            if new_dic in tabContrat: # Vérifier l'existence du programme
                return JsonResponse({
                    "status": "error",
                    "message": "Ce contrat existe déjà."})
            if date_debut > date_fin:
                return JsonResponse({
                    "status": "error",
                    "message": "La date du début doit être inférieure ou égale à la date de fin."})
            else:
                contrat.user_id = user_id
                contrat.type_contrat = type_contrat
                contrat.poste = poste
                contrat.description = description
                contrat.date_debut = date_debut
                contrat.date_fin = date_fin
                contrat.amount = amount
                contrat.admin_id=request.user.id
                contrat.save()
                
                return JsonResponse({
                    "status": "success",
                    "message": "Contrat modifié avec succès."})


@login_required(login_url='connection/login')
@allowed_users(allowed_roles=permission_gestionnaire)
def del_contrat(request, id):
    anneeacademique_id = request.session.get('anneeacademique_id')
    setting = get_setting(anneeacademique_id)
    if setting is None:
        return redirect("settings/maintenance")
    
    contrat = Contrat.objects.get(id=id)
    # Nombre de contrats avant la suppression
    count0 = Contrat.objects.all().count()
    contrat.delete()
    # Nombre de contrats après la suppression
    count1 = Contrat.objects.all().count()
    if count1 < count0: 
        messages.success(request, "Elément supprimé avec succès.")
    else:
        messages.error(request, "La suppression a échouée.")
    return redirect("contrat/contrats")

def ajax_type_contrat(request, type_contrat):
    anneeacademique_id = request.session.get('anneeacademique_id')
    context = {
        "type_contrat": type_contrat,
        "setting": get_setting(anneeacademique_id)
    }
    return render(request, "ajax_type_contrat.html", context)

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=permission_users)
def contrats_user(request):
    user_id = request.user.id
    anneeacademique_id = request.session.get('anneeacademique_id')
    setting = get_setting(anneeacademique_id)
    if setting is None:
        return redirect("settings/maintenance")

    contrats = Contrat.objects.filter(user_id=user_id, anneeacademique_id=anneeacademique_id).order_by("-date_fin")
    tabcontrats = []
    for contrat in contrats:  
        dic = {}
        dic["contrat"] = contrat
        dic["status"] = status_contrat(contrat)
        tabcontrats.append(dic)

    context = {
        "setting": setting,
        "contrats": tabcontrats
    }
    return render(request, "contrat/contrats_user.html", context) 

def signer_contrat(request, contrat_id):
    contrat = Contrat.objects.get(id=contrat_id)
    contrat.status_signature = True
    contrat.date_signature = date.today()
    contrat.save()
    
    context = {
        "contrat": contrat
    }
    return render(request, "signer_contrat.html", context)

def ajax_delete_contrat(request, id):
    contrat = Contrat.objects.get(id=id)
    context = {
        "contrat": contrat
    }
    return render(request, "ajax_delete_contrat.html", context)


#================== Gestion de rénumeration =================================

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=permission_gestionnaire)
def renum_admin(request):
    anneeacademique_id = request.session.get('anneeacademique_id')
    setting = get_setting(anneeacademique_id)
    if setting is None:
        return redirect("settings/maintenance")
    
    renumerations_users = RenumerationAdmin.objects.values("user_id").filter(anneeacademique_id=anneeacademique_id).annotate(nb_renumerations=Count("user_id"))
    tabrenumerations = []
    for ru in renumerations_users:
        user = User.objects.get(id=ru["user_id"])   
        dic = {}
        dic["user"] = user
        dic["renumerations"] = RenumerationAdmin.objects.filter(user_id=ru["user_id"], anneeacademique_id=anneeacademique_id)
        dic["nb_renumerations"] = ru["nb_renumerations"]
        tabrenumerations.append(dic)

    anneeacademique = AnneeCademique.objects.get(id=anneeacademique_id)
    context = {
        "setting": setting,
        "renumerations": tabrenumerations,
        "anneeacademique": anneeacademique
    }
    return render(request, "renum/renum_admin.html", context)    

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=permission_gestionnaire)
@transaction.atomic
def add_renum_admin(request):
    anneeacademique_id = request.session.get('anneeacademique_id')
    setting = get_setting(anneeacademique_id)
    if setting is None:
        return redirect("settings/maintenance")

    if request.method == "POST":

        user_id = request.POST["user"]
        month = request.POST["month"]
        amount = bleach.clean(request.POST["amount"].strip())
        indemnite = bleach.clean(request.POST["indemnite"].strip())
        
        # Récuperer la délibération pour verifier si ses activités ont été cloturées ou pas
        anneescolaire = AnneeCademique.objects.filter(status_cloture=True, id=anneeacademique_id)     
        # Nettoyer la valeur (supprimer les espaces et remplacer la virgule par un point)
        amount = re.sub(r'\xa0', '', amount)  # Supprime les espaces insécables
        amount = amount.replace(" ", "").replace(",", ".")
        
        indemnite = re.sub(r'\xa0', '', indemnite)  # Supprime les espaces insécables
        indemnite = indemnite.replace(" ", "").replace(",", ".")

        try:
            amount = Decimal(amount)  # Convertir en Decimal
        except:
            return JsonResponse({
                "status": "error",
                "message": "Le montant doit être un nombre valide."})
        try:
            indemnite = Decimal(indemnite)  # Convertir en Decimal
        except:
            return JsonResponse({
                "status": "error",
                "message": "L'indemnité' doit être un nombre valide."})
                 
        query = RenumerationAdmin.objects.filter(user_id=user_id, month=month, anneeacademique_id=anneeacademique_id)
        if anneescolaire.exists(): # Verifier si on a déjà cloturé les opérations de cette année
                return JsonResponse({
                    "status": "error",
                    "message": "Les opérations de cette année académique ont déjà été clôturées."})   
        if query.exists():
            return JsonResponse({
                    "status": "error",
                    "message": "Cette rénumeration existe déjà."})
        else:
            total_amount = amount + indemnite
            renumeration = RenumerationAdmin(
                user_id=user_id, 
                month=month, 
                amount=amount,
                indemnite=indemnite,
                total_amount=total_amount,
                anneeacademique_id=anneeacademique_id,
                responsable_id=request.user.id)
            # Nombre de contrats avant l'ajout
            count0 = RenumerationAdmin.objects.all().count()
            renumeration.save()
            # Nombre de contrats après l'ajout
            count1 = RenumerationAdmin.objects.all().count()
            # On verifie si l'insertion a eu lieu ou pas.
            if count0 < count1:
                return JsonResponse({
                        "status": "success",
                        "message": "Rénumeration admlin enregistré avec succès."})
            else:
                return JsonResponse({
                    "status": "error",
                    "message": "Insertion a échouée."}) 

    months = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
    #Récuperer les utilisateurs
    users_contrats = (Contrat.objects.values("user_id")
                      .filter(anneeacademique_id=anneeacademique_id)
                      .annotate(nb_contrats=Count("user_id")))
    users = []
    for uc in users_contrats:
        user = User.objects.get(id=uc["user_id"])
        # Recuperer les groupes de l'utilisateurs
        groups = user.groups.all()
        for group in groups:
            if group.name in permission_gestionnaire_admin:
                users.append(user)
                break

    context = {
        "setting": setting,
        "months": months,
        "users": users
    }
    return render(request, "renum/add_renum_admin.html", context)


@login_required(login_url='connection/login')
@allowed_users(allowed_roles=permission_gestionnaire)
def edit_renum_admin(request,id):
    anneeacademique_id = request.session.get('anneeacademique_id')
    setting = get_setting(anneeacademique_id)
    if setting is None:
        return redirect("settings/maintenance")

    renumeration = RenumerationAdmin.objects.get(id=id)
        
    users = User.objects.exclude(id=renumeration.user.id)
    
    #Récuperer les utilisateurs
    users_contrats = (Contrat.objects.values("user_id")
                      .filter(anneeacademique_id=anneeacademique_id)
                      .annotate(nb_contrats=Count("user_id")))
    
    users = []
    for uc in users_contrats:
        user = User.objects.get(id=uc["user_id"])
        if user.id != renumeration.user.id:
            # Recuperer les groupes de l'utilisateurs
            groups = user.groups.all()
            for group in groups:
                if group.name in permission_gestionnaire_admin:
                    users.append(user)
                    break
        
    tab_months = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
    months = []
    for month in tab_months:
        if month != renumeration.month:
            months.append(month)
    context = {
        "setting": setting,
        "renumeration": renumeration,
        "users": users,
        "months": months
    }
    return render(request, "renum/edit_renum_admin.html", context)
   

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=permission_gestionnaire)
def edit_ra(request):
    anneeacademique_id = request.session.get('anneeacademique_id')
    if request.method == "POST":
        id = int(request.POST["id"])
        try:
            renumeration = RenumerationAdmin.objects.get(id=id)
        except:
            renumeration = None

        if renumeration is None:
            return JsonResponse({
                    "status": "error",
                    "message": "Identifiant inexistant."})
        else: 
            user_id = request.POST["user"]
            month = request.POST["month"]
            amount = bleach.clean(request.POST["amount"].strip())
            indemnite = bleach.clean(request.POST["indemnite"].strip())
            
            # Récuperer la délibération pour verifier si ses activités ont été cloturées ou pas
            anneescolaire = AnneeCademique.objects.filter(status_cloture=True, id=anneeacademique_id)    
            # Nettoyer la valeur (supprimer les espaces et remplacer la virgule par un point)
            amount = re.sub(r'\xa0', '', amount)  # Supprime les espaces insécables
            amount = amount.replace(" ", "").replace(",", ".")
            
            indemnite = re.sub(r'\xa0', '', indemnite)  # Supprime les espaces insécables
            indemnite = indemnite.replace(" ", "").replace(",", ".")

            try:
                amount = Decimal(amount)  # Convertir en Decimal
            except:
                return JsonResponse({
                    "status": "error",
                    "message": "Le montant doit être un nombre valide."})
                
            try:
                indemnite = Decimal(indemnite)  # Convertir en Decimal
            except:
                return JsonResponse({
                    "status": "error",
                    "message": "L'indemnité' doit être un nombre valide."})
            
            # Vérifier l'existence de la rénumeration
            renumerations = RenumerationAdmin.objects.filter(month=month, user_id=user_id, anneeacademique_id=anneeacademique_id).exclude(id=id)
            tabRenumeration = []
            for r in renumerations:   
                dic = {}
                dic["user_id"] = r.user.id
                dic["month"] = r.month
                dic["anneeacademique_id"] = r.anneeacademique.id
                tabRenumeration.append(dic)            
                
            new_dic = {}
            new_dic["user_id"] = int(user_id)
            new_dic["month"] = month
            new_dic["anneeacademique_id"] = int(anneeacademique_id)
            if anneescolaire.exists(): # Verifier si on a déjà cloturé les opérations de cette année
                return JsonResponse({
                    "status": "error",
                    "message": "Les opérations de cette année académique ont été déjà clôturées."})            
            if new_dic in tabRenumeration: # Vérifier l'existence de la rénumeration
                return JsonResponse({
                    "status": "error",
                    "message": "Cette rénumeration existe déjà."})
            else:
                renumeration.user_id = user_id
                renumeration.month = month
                renumeration.amount = amount
                renumeration.indemnite = indemnite
                renumeration.save()
                
                return JsonResponse({
                    "status": "success",
                    "message": "Rénumeration modifiée avec succès."})


@login_required(login_url='connection/login')
@allowed_users(allowed_roles=permission_gestionnaire)
def del_renum_admin(request,id):
    anneeacademique_id = request.session.get('anneeacademique_id')
    setting = get_setting(anneeacademique_id)
    if setting is None:
        return redirect("settings/maintenance")
    
    renumeration = RenumerationAdmin.objects.get(id=id)
    # Nombre de contrats avant la suppression
    count0 = RenumerationAdmin.objects.all().count()
    renumeration.delete()
    # Nombre de contrats après la suppression
    count1 = RenumerationAdmin.objects.all().count()
    if count1 < count0: 
        messages.success(request, "Elément supprimé avec succès.")
    else:
        messages.error(request, "La suppression a échouée.")
    return redirect("renum/renum_admin")

def ajax_delete_renum_admin(request, id):
    renumeration = RenumerationAdmin.objects.get(id=id)
    context = {
        "renumeration": renumeration
    }
    return render(request, "ajax_delete_renum_admin.html", context)


@login_required(login_url='connection/login')
@allowed_users(allowed_roles=permission_gestionnaire_admin)
def mes_renum_admin(request):
    anneeacademique_id = request.session.get('anneeacademique_id')
    setting = get_setting(anneeacademique_id)
    if setting is None:
        return redirect("settings/maintenance")
    
    renumerations = RenumerationAdmin.objects.filter(anneeacademique_id=anneeacademique_id, user_id=request.user.id)
    context = {
        "setting": setting,
        "renumerations": renumerations
    }
    return render(request, "renum/mes_renum_admin.html", context)  

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=permission_gestionnaire)
def recapitulatif(request):
    anneeacademique_id = request.session.get('anneeacademique_id')
    setting = get_setting(anneeacademique_id)
    if setting is None:
        return redirect("settings/maintenance")
    
    months = month_actifs(anneeacademique_id)
    context = {
        "months": months,
        "setting": setting
    }
    return render(request, "recapitulatif.html", context)

def ajax_type_contrat(request, type_contrat):
    anneeacademique_id = request.session.get('anneeacademique_id')
    setting = get_setting(anneeacademique_id)
    print(type_contrat)
    context = {
        "type_contrat": type_contrat,
        "setting": setting
    }
    return render(request, "ajax_type_contrat.html", context)

# Selectionner les mois du contrat de l'utilisateur
def ajax_user_month_contrat(request, user_id):
    anneeacademique_id = request.session.get('anneeacademique_id')
    contrats = Contrat.objects.filter(user_id=user_id, anneeacademique_id=anneeacademique_id).order_by("id")
    months = []
    for contrat in contrats:
        months += month_contrat_user(contrat)
    context = {
        "months": months
    }
    return render(request, "ajax_user_month_contrat.html", context)

def ajax_user_amount(request, user_id, month):
    anneeacademique_id = request.session.get('anneeacademique_id')
    contrats = Contrat.objects.filter(user_id=user_id, anneeacademique_id=anneeacademique_id).order_by("id")
    amount = 0
    for contrat in contrats:
        months = month_contrat_user(contrat) # Récuperer tous les mois de ce contrat
        if month in months: # Verifier si ce mois fait parti des mois de ce contrat
            amount = contrat.amount
    context = {
        "amount": amount,
        "setting": get_setting(anneeacademique_id)
    }
    return render(request, "ajax_user_amount.html", context)


def total_renum_salle(salle_id, anneeacademique_id, month):
    
        matieres_emargements = (Emargement.objects.values("matiere_id")
                                .filter(anneeacademique_id=anneeacademique_id, month=month, salle_id=salle_id)
                                .annotate(nb_matieres=Count("matiere_id")))
        
        total_renum = 0
        for me in matieres_emargements:
            
            emargements = Emargement.objects.filter(anneeacademique_id=anneeacademique_id, month=month, salle_id=salle_id, matiere_id=me["matiere_id"])
            # Initialisation avec une durée nulle
            total_delta = timedelta(0)
            for em in emargements:
                    # Convertir les objets time en timedelta
                    start_delta = timedelta(hours=em.heure_debut.hour, minutes=em.heure_debut.minute)
                    end_delta = timedelta(hours=em.heure_fin.hour, minutes=em.heure_fin.minute)
                    # Calculer la somme des deux
                    total_delta +=  end_delta - start_delta
                    
            # Extraire les heures et les minutes en normalisant (si la somme dépasse 24 heures)
            total_seconds = total_delta.total_seconds()
            total_hours = int(total_seconds // 3600) % 24  # Récupérer les heures (modulo 24 pour ne pas dépasser une journée)
            total_minutes = int((total_seconds % 3600) // 60)

            # Afficher le résultat au format HH:MM
            formatted_time = f"{total_hours:02}:{total_minutes:02}"
                
            # Recuperer le cout par heure de la matière
            enseignement = Enseigner.objects.filter(
                    salle_id=salle_id,
                    matiere_id=me["matiere_id"],
                    anneeacademique_id=anneeacademique_id).first()
                
            total_renum += calculer_montant(enseignement.cout_heure, formatted_time)
                
        return total_renum    
    
# Recuperer les salles ou les élèves ont payé, ou encore les enseignants ont été rénumeré  
def get_salles(month, anneeacademique_id):
    #Récuperer les salles
    salles = Salle.objects.all()
    tabSalles = []
    tabSallePay = []    
    salles_payments = (Payment.objects.values("salle_id")
                        .filter(month=month, anneeacademique_id=anneeacademique_id)
                        .annotate(nb_payments=Count("salle_id")))
    for sp in salles_payments:
        tabSallePay.append(sp["salle_id"])
        
    tabSalleEmar = []    
    salles_emargements = (Emargement.objects.values("salle_id")
                       .filter(month=month, anneeacademique_id=anneeacademique_id)
                       .annotate(nb_emargements=Count("salle_id")))
    for sp in salles_emargements:
        tabSalleEmar.append(sp["salle_id"])
        
    for salle in salles:
        if (salle.id in tabSallePay) or (salle.id in tabSalleEmar):
            if salle.id not in tabSalles:
                tabSalles.append(salle.id)
                
    return tabSalles 
      
    
def ajax_recapitulatif(request, month):
    anneeacademique_id = request.session.get('anneeacademique_id')
    salles = []
    total_reste = 0
    total_paiement_student = 0
    total_renum_enseignant = 0
    months_emargements = get_salles(month, anneeacademique_id)
    
    for salle_id in months_emargements:
        dic = {}
        # Recuperer la salle
        salle = Salle.objects.get(id=salle_id)
        dic["salle"] = salle
        # Somme totale payée par les étudiants
        sum_payment = (Payment.objects.filter( salle_id=salle.id, month=month, anneeacademique_id=anneeacademique_id).aggregate(Sum('amount'))['amount__sum'] or 0)
        dic["sum_payment"] = sum_payment
        # Somme totale qu'on a payé les enseignants
        sum_renum = total_renum_salle(salle.id, anneeacademique_id, month)
        dic["sum_renum"] = float(sum_renum)
        dic["reste"] = float(sum_payment) - float(sum_renum)
        
        total_reste += float(sum_payment) - float(sum_renum)
        total_paiement_student += sum_payment
        total_renum_enseignant += sum_renum
        
        salles.append(dic)
        
    # Calculer toutes les indemnités des enseignant d'un mois
    sum_indemnite = (Renumeration.objects.filter(month=month, anneeacademique_id=anneeacademique_id).aggregate(Sum('indeminte'))['indeminte__sum'] or 0)
    # Récuperer les renumération
    renumerations = Renumeration.objects.filter(month=month, anneeacademique_id=anneeacademique_id).exclude(indeminte=0)
    
    # Calucler le montant total de renumeration des enseignants
    total_amount = (RenumerationAdmin.objects.filter(month=month, anneeacademique_id=anneeacademique_id).aggregate(Sum('amount'))['amount__sum'] or 0)
    total_indemnite = (RenumerationAdmin.objects.filter(month=month, anneeacademique_id=anneeacademique_id).aggregate(Sum('indemnite'))['indemnite__sum'] or 0)
    total_renum_admin = float(total_amount) + float(total_indemnite)
    
    
    # Recupérer les dépenses d'un mois
    total_depense = 0
    tabdepenses = []
    type_depenses = (Depense.objects.values("signe")
                     .filter(month=month, anneeacademique_id=anneeacademique_id)
                     .annotate(sum_depense=Sum("amount")))
    for tp in type_depenses:
        dic = {}
        dic["signe"] = tp["signe"]
        dic["sum_depense"] = tp["sum_depense"]
        dic["depenses"] = Depense.objects.filter(signe=tp["signe"], month=month, anneeacademique_id=anneeacademique_id)
        tabdepenses.append(dic)
        if tp["signe"] == "Entrée":     
            total_depense += float(tp["sum_depense"])
        else:
            total_depense = total_depense - float(tp["sum_depense"])
    
    
    
    recette_month = float(total_reste) - float(sum_indemnite) - total_renum_admin + total_depense
    
    context = {
        "setting": get_setting(anneeacademique_id),
        "salles": salles,
        "total_reste": total_reste,
        "total_paiement_student": total_paiement_student,
        "total_renum_enseignant": total_renum_enseignant,
        "sum_indemnite": sum_indemnite,
        "renumerations": renumerations,
        "month": month,
        "total_renum_admin": total_renum_admin,
        "depenses": tabdepenses,
        "recette_month": recette_month
    }
    return render(request, "ajax_recapitulatif.html", context)


def month_actifs(anneeacademique_id):
    months = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
    tabMonths = []
    
    tabMonthRenumEns = []
    months_renum_ens = (Renumeration.objects.values("month")
                        .filter(anneeacademique_id=anneeacademique_id)
                        .annotate(nb_emargements=Count("month")))
    for me in months_renum_ens:
        tabMonthRenumEns.append(me["month"])
    
    tabMonthPay = []    
    months_payments = (Payment.objects.values("month")
                        .filter(anneeacademique_id=anneeacademique_id)
                        .annotate(nb_payments=Count("month")))
    for mp in months_payments:
        tabMonthPay.append(mp["month"])
        
    tabMonthRenum = []    
    months_renumerations = (RenumerationAdmin.objects.values("month")
                        .filter(anneeacademique_id=anneeacademique_id)
                        .annotate(nb_renumerations=Count("month")))
    for mr in months_renumerations:
        tabMonthRenum.append(mr["month"])
        
    tabMonthDepense = []    
    months_depenses = (Depense.objects.values("month")
                        .filter(anneeacademique_id=anneeacademique_id)
                        .annotate(nb_depenses=Count("month")))
    for mr in months_depenses:
        tabMonthDepense.append(mr["month"])
        
    for month in months:
        if (month in tabMonthRenumEns) or (month in tabMonthPay) or (month in tabMonthRenum) or (month in tabMonthDepense):
            if month not in tabMonths:
                tabMonths.append(month) 
    
    return tabMonths
 
@login_required(login_url='connection/login')           
@allowed_users(allowed_roles=permission_gestionnaire)       
def caisse(request):
    anneeacademique_id = request.session.get('anneeacademique_id')
    months = month_actifs(anneeacademique_id)
    caisses = []
    recette_totale = 0
    for month in months:
        dic_caisse = {}
        dic_caisse["month"] = month
        total_renum_enseignant = 0        
        # Somme totale payée par les étudiants
        total_paiement_student = (Payment.objects.filter(month=month, anneeacademique_id=anneeacademique_id).aggregate(Sum('amount'))['amount__sum'] or 0)
            
        months_emargements = (Emargement.objects.values("salle_id")
                        .filter(month=month, anneeacademique_id=anneeacademique_id)
                        .annotate(nb_emargements=Count("salle_id")))
        
        for me in months_emargements:
            # Somme totale qu'on a payé les enseignants
            sum_renum = total_renum_salle(me["salle_id"], anneeacademique_id, month)
            total_renum_enseignant += sum_renum
            
        # Calculer toutes les indemnités des enseignant d'un mois
        sum_indemnite = (Renumeration.objects.filter(month=month, anneeacademique_id=anneeacademique_id).aggregate(Sum('indeminte'))['indeminte__sum'] or 0)
        
        # Calucler le montant total de renumeration des administarteurs
        total_amount = (RenumerationAdmin.objects.filter(month=month, anneeacademique_id=anneeacademique_id).aggregate(Sum('amount'))['amount__sum'] or 0)
        total_indemnite = (RenumerationAdmin.objects.filter(month=month, anneeacademique_id=anneeacademique_id).aggregate(Sum('indemnite'))['indemnite__sum'] or 0)
        total_renum_admin = float(total_amount) + float(total_indemnite)
        
        
        # Recupérer les dépenses d'un mois
        total_depense = 0
        tabdepenses = []
        type_depenses = (Depense.objects.values("signe")
                        .filter(month=month, anneeacademique_id=anneeacademique_id)
                        .annotate(sum_depense=Sum("amount")))
        for tp in type_depenses:
            dic = {}
            dic["signe"] = tp["signe"]
            dic["sum_depense"] = tp["sum_depense"]
            dic["depenses"] = Depense.objects.filter(signe=tp["signe"], month=month, anneeacademique_id=anneeacademique_id)
            tabdepenses.append(dic)
            
            if tp["signe"] == "Entrée":
                total_depense += float(tp["sum_depense"])
            else:
                total_depense = total_depense - float(tp["sum_depense"]) 
        
        recette_month = float(total_paiement_student) - float(total_renum_enseignant) - float(sum_indemnite) - total_renum_admin + total_depense
        
        dic_caisse["recette_month"] = recette_month
        
        recette_totale += recette_month
        
        caisses.append(dic_caisse)
        
    # somme total des inscription
    salles_inscriptions = Inscription.objects.values("salle_id").filter(anneeacademique_id=anneeacademique_id).annotate(nb_inscriptions=Count("salle_id"))
    tabSalles = []
    total_inscription = 0
    for si in salles_inscriptions:
        dic = {}
        salle = Salle.objects.get(id=si["salle_id"])
        dic["salle"] = salle
        total_inscription_salle = Inscription.objects.filter(salle_id=si["salle_id"], anneeacademique_id=anneeacademique_id).aggregate(Sum("amount"))["amount__sum"] or 0
        dic["total_inscription_salle"] = total_inscription_salle
        
        total_inscription += total_inscription_salle
        tabSalles.append(dic)
    total = float(recette_totale) + float(total_inscription)
    context = {
        "setting": get_setting(anneeacademique_id),
        "caisses": caisses,
        "recette_totale": recette_totale,
        "totale": total,
        "total_inscription": total_inscription,
        "salles": tabSalles
        
    }
    return render(request, "caisse.html", context) 

def comparaison_recette_par_annee_scolaire(id):
    annees_academiques = AnneeCademique.objects.filter(id__lte=id).order_by('-id')[:3]
    recettes_globales = []
    months_globales = []
    for annee_academique in annees_academiques:
        dic_globle = {}
        dic_globle["anneeacademique"] = annee_academique
        anneeacademique_id = annee_academique.id
        months = month_actifs(anneeacademique_id)
        caisses = []
        recette_totale = 0
        for month in months:
            dic_caisse = {}
            dic_caisse["month"] = month
            # Somme totale payée par les étudiants
            total_paiement_student = (Payment.objects.filter(month=month, anneeacademique_id=anneeacademique_id).aggregate(Sum('amount'))['amount__sum'] or 0)
            total_renum_enseignant = 0
            months_emargements = (Emargement.objects.values("salle_id")
                            .filter(month=month, anneeacademique_id=anneeacademique_id)
                            .annotate(nb_emargements=Count("salle_id")))
            
            for me in months_emargements:
                # Somme totale qu'on a payé les enseignants
                sum_renum = total_renum_salle(me["salle_id"], anneeacademique_id, month)
                total_renum_enseignant += sum_renum
                
            # Calculer toutes les indemnités des enseignant d'un mois
            sum_indemnite = (Renumeration.objects.filter(month=month, anneeacademique_id=anneeacademique_id).aggregate(Sum('indeminte'))['indeminte__sum'] or 0)
            
            # Calucler le montant total de renumeration des enseignants
            total_amount = (RenumerationAdmin.objects.filter(month=month, anneeacademique_id=anneeacademique_id).aggregate(Sum('amount'))['amount__sum'] or 0)
            total_indemnite = (RenumerationAdmin.objects.filter(month=month, anneeacademique_id=anneeacademique_id).aggregate(Sum('indemnite'))['indemnite__sum'] or 0)
            total_renum_admin = float(total_amount) + float(total_indemnite)
            
            
            # Recupérer les dépenses d'un mois
            total_depense = 0
            tabdepenses = []
            type_depenses = (Depense.objects.values("signe")
                            .filter(month=month, anneeacademique_id=anneeacademique_id)
                            .annotate(sum_depense=Sum("amount")))
            for tp in type_depenses:
                dic = {}
                dic["signe"] = tp["signe"]
                dic["sum_depense"] = tp["sum_depense"]
                dic["depenses"] = Depense.objects.filter(signe=tp["signe"], month=month, anneeacademique_id=anneeacademique_id)
                tabdepenses.append(dic)
                if tp["signe"] == "Entrée":
                    total_depense += float(tp["sum_depense"])
                else:
                    total_depense = total_depense - float(tp["sum_depense"])  
            
            recette_month = float(total_paiement_student) - float(total_renum_enseignant) - float(sum_indemnite) - total_renum_admin + total_depense
            
            dic_caisse["recette_month"] = int(recette_month)
            
            recette_totale += recette_month
            
            caisses.append(dic_caisse)
            
            # Récuperer les mois actifs dans au moins une année scolaire
            if month not in months_globales:
                months_globales.append(month)
            
        dic_globle["caisses"] = caisses 
        
        recettes_globales.append(dic_globle)
    return recettes_globales, months_globales

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=permission_gestionnaire)
def apercu_global(request):
    anneeacademique_id = request.session.get('anneeacademique_id')
    months = month_actifs(anneeacademique_id)
    caisses = []
    recette_totale = 0
    for month in months:
        dic_caisse = {}
        dic_caisse["month"] = month
        # Somme totale payée par les étudiants
        total_paiement_student = (Payment.objects.filter(month=month, anneeacademique_id=anneeacademique_id).aggregate(Sum('amount'))['amount__sum'] or 0)
        total_renum_enseignant = 0
        months_emargements = (Emargement.objects.values("salle_id")
                        .filter(month=month, anneeacademique_id=anneeacademique_id)
                        .annotate(nb_emargements=Count("salle_id")))
        
        for me in months_emargements:
            # Somme totale qu'on a payé les enseignants
            sum_renum = total_renum_salle(me["salle_id"], anneeacademique_id, month)
            total_renum_enseignant += sum_renum
            
        # Calculer toutes les indemnités des enseignant d'un mois
        sum_indemnite = (Renumeration.objects.filter(month=month, anneeacademique_id=anneeacademique_id).aggregate(Sum('indeminte'))['indeminte__sum'] or 0)
        
        # Calucler le montant total de renumeration des enseignants
        total_amount = (RenumerationAdmin.objects.filter(month=month, anneeacademique_id=anneeacademique_id).aggregate(Sum('amount'))['amount__sum'] or 0)
        total_indemnite = (RenumerationAdmin.objects.filter(month=month, anneeacademique_id=anneeacademique_id).aggregate(Sum('indemnite'))['indemnite__sum'] or 0)
        total_renum_admin = float(total_amount) + float(total_indemnite)
        
        
        # Recupérer les dépenses d'un mois
        total_depense = 0
        tabdepenses = []
        type_depenses = (Depense.objects.values("signe")
                        .filter(month=month, anneeacademique_id=anneeacademique_id)
                        .annotate(sum_depense=Sum("amount")))
        for tp in type_depenses:
            dic = {}
            dic["signe"] = tp["signe"]
            dic["sum_depense"] = tp["sum_depense"]
            dic["depenses"] = Depense.objects.filter(signe=tp["signe"], month=month, anneeacademique_id=anneeacademique_id)
            tabdepenses.append(dic)
            
            if tp["signe"] == "Entrée":
                total_depense += float(tp["sum_depense"])
            else:
                total_depense = total_depense - float(tp["sum_depense"])    
        
        recette_month = float(total_paiement_student) - float(total_renum_enseignant) - float(sum_indemnite) - total_renum_admin + total_depense
        
        dic_caisse["recette_month"] = int(recette_month)
        
        recette_totale += recette_month
        
        caisses.append(dic_caisse)
        
    recettes_globales, months_globales = comparaison_recette_par_annee_scolaire(anneeacademique_id)
    
    context = {
        "setting": get_setting(anneeacademique_id),
        "caisses": caisses,
        "recette_totale": int(recette_totale),
        "recettes_globales":  recettes_globales,
        "months_globales": months_globales
        
    }
    return render(request, "apercu_global.html", context) 


@login_required(login_url='connection/login')
@allowed_users(allowed_roles=permission_gestionnaire_enseignant)
def bulletin_paie_enseignant(request, id):
    anneeacademique_id = request.session.get('anneeacademique_id')
    setting = get_setting(anneeacademique_id)
    
    renumeration = Renumeration.objects.get(id=id)
    anneeacademique  = AnneeCademique.objects.get(id=anneeacademique_id)
    
    # Chemin vers notre image
    image_path = setting.logo

    # Lire l'image en mode binaire et encoder en Base64
    base64_string = base64.b64encode(image_path.read()).decode('utf-8')
    # Date actuelle
    date_actuelle = date.today()
    
    # Récuperer le poste
    contrat = Contrat.objects.filter(user_id=renumeration.personnel.id, anneeacademique_id=anneeacademique_id).order_by("-id").first()
    poste = contrat.poste
    context = {
        "renumeration": renumeration,   
        "poste": poste,   
        "base64_image": base64_string, 
        "setting": setting,
        "anneeacademique": anneeacademique,
        "date_actuelle": date_actuelle
    }
    template = get_template("bulletin_paie_enseignant.html")
    html = template.render(context)
    options = {
        'page-size': 'Letter',
        'encoding': "UTF-8",
    }
    pdf = pdfkit.from_string(html, False, options)
    reponse = HttpResponse(pdf, content_type='application/pdf')
    reponse['Content-Disposition'] = f"attachment; filename=Bulletin_paie_{ renumeration.personnel.last_name }_{ renumeration.personnel.first_name }.pdf"
    return reponse

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=permission_gestionnaire_enseignant)
def bulletin_paie_admin(request, id):
    anneeacademique_id = request.session.get('anneeacademique_id')
    setting = get_setting(anneeacademique_id)
    
    renumeration = RenumerationAdmin.objects.get(id=id)
    anneeacademique  = AnneeCademique.objects.get(id=anneeacademique_id)
    
    # Chemin vers notre image
    image_path = setting.logo

    # Lire l'image en mode binaire et encoder en Base64
    base64_string = base64.b64encode(image_path.read()).decode('utf-8')
    # Date actuelle
    date_actuelle = date.today()
    
    # Récuperer le poste
    contrat = Contrat.objects.filter(user_id=renumeration.user.id, anneeacademique_id=anneeacademique_id).order_by("-id").first()
    poste = contrat.poste
    context = {
        "renumeration": renumeration,   
        "poste": poste,   
        "base64_image": base64_string, 
        "setting": setting,
        "anneeacademique": anneeacademique,
        "date_actuelle": date_actuelle
    }
    template = get_template("bulletin_paie_admin.html")
    html = template.render(context)
    options = {
        'page-size': 'Letter',
        'encoding': "UTF-8",
    }
    pdf = pdfkit.from_string(html, False, options)
    reponse = HttpResponse(pdf, content_type='application/pdf')
    reponse['Content-Disposition'] = f"attachment; filename=Bulletin_paie_{ renumeration.user.last_name }_{ renumeration.user.first_name }.pdf"
    return reponse      
        
