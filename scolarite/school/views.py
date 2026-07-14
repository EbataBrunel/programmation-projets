# Importation des modules standards
import bleach
import re
# Importation des modules tiers
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.views import View
from django.db.models import Count, Sum
from datetime import date, datetime, timedelta
from twilio.rest import Client
from django.conf import settings
from django.http import JsonResponse
# Importation des modules locaux
from .models import Setting
from app_auth.decorator import unauthenticated_customer, allowed_users
from app_auth.models import Student
from classe.models import Classe
from anneeacademique.models import AnneeCademique
from inscription.models import Inscription
from activity.models import Activity
from programme.models import Programme
from enseignement.models import Enseigner
from calendrier.models import Trimestre, EvenementScolaire
from absence.models import AbsenceAdmin, Absence
from salle.models import Salle
from emargement.models import Emargement
from paiement.models import Payment, Notification
from absence.models import Absencestudent
from composition.models import Composer
from renumeration.models import Renumeration, RenumerationAdmin
from contact.models import Contact, Message
from depense.models import Depense
from cycle.models import Cycle

permission_utilisateur = ['Promoteur', 'Directeur Général', 'Directeur des Etudes', 'Gestionnaire', 'Enseignant']
permission_admin = ['Promoteur', 'Directeur Général', 'Directeur des Etudes', 'Gestionnaire', 'Surveillant Général']
permission_promoteur_DG = ['Promoteur', 'Directeur Général']
permission_promoteur_enseignant = ['Promoteur', 'Directeur Général', 'Enseignant']

#=================================== Définition des mois ===================================== 
def format_mois(month):
    if month == "01":
        return "Janvier"
    elif month == "02":
        return "Février"
    elif month == "03":
        return "Mars"
    elif month == "04":
        return "Avril"
    elif month == "05":
        return "Mai"
    elif month == "06":
        return "Juin"
    elif month == "07":
        return "Juillet"
    elif month == "08":
        return "Août"
    elif month == "Septembre":
        return "09"
    elif month == "10":
        return "Octobre"
    elif month == "11":
        return "Novembre"
    else:
        return "Décembre"
    
# Calculter le salaire
def calcul_montant(cout_heure, heure_totale):
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

# Formatter le temps  
def format_temps(time):
    # Extraire les heures et les minutes en normalisant (si la somme dépasse 24 heures)
    total_matiere_seconds = time.total_seconds()
    total_matiere_hours = int(total_matiere_seconds // 3600) % 24  # Récupérer les heures (modulo 24 pour ne pas dépasser une journée)
    total_matiere_minutes = int((total_matiere_seconds % 3600) // 60)

    # Afficher le résultat au format HH:MM
    formatted_time = f"{total_matiere_hours:02}:{total_matiere_minutes:02}"   
    return formatted_time

def get_setting(anneeacademique_id):
    try:
        setting = Setting.objects.filter(anneeacademique_id=anneeacademique_id).first()
    except Exception as e:
        setting = None

    return setting

def months_actives(anneeacademique_id):
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

# Somme totale qu'on a payé les enseignants
def somme_total_renum_salle(salle_id, anneeacademique_id, month): 
    
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
                
            total_renum += calcul_montant(enseignement.cout_heure, formatted_time)
                
        return total_renum    
        
     
def maintenance(request):   
    return render(request, "settings/maintenance.html")

def authorization(request):
    context = { }
    return render(request, "settings/authorization.html", context)

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=permission_utilisateur)
def db_classe(request, id):
    anneeacademique_id = request.session.get('anneeacademique_id')
    setting = get_setting(anneeacademique_id)
    if setting is None:
        return redirect("settings/maintenance")
    
    cycle = Cycle.objects.get(id=id)
    request.session["cycle_id"] = cycle.id
    request.session["cycle_lib"] = cycle.libelle
    
    classes = Classe.objects.filter(cycle_id=cycle.id, anneeacademique_id=anneeacademique_id)    
    context = {
        "setting": setting,
        "classes": classes
    }
    
    return render(request, "settings/db_classe.html", context)

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=permission_utilisateur)
def dashboard(request, id):
    anneeacademique_id = request.session.get('anneeacademique_id')
    user_id = request.user.id
    setting = get_setting(anneeacademique_id)
    if setting is None:
        return redirect("settings/maintenance")
    
    classe = Classe.objects.get(id=id)
    request.session["classe_id"] = classe.id
    request.session["classe_lib"] = classe.libelle
    # Récuperer la dernière activité
    activity = Activity.objects.filter(anneeacademique_id=anneeacademique_id, type="Privée").order_by('-id').first()
    activity_status = False
    if activity:
        date_actuelle = date.today()
        if date_actuelle == activity.date:
            activity_status = True
    # Récuperer toutes les activités
    activities = Activity.objects.filter(anneeacademique_id=anneeacademique_id, type="Privée").order_by('-id')
       
    # Determiner le nombre d'administrateurs
    nb_amin = 0
    users = User.objects.all()
    for user in users:
        groups = user.groups.all()
        for group in groups:
            if group.name in permission_admin:
                nb_amin += 1
                break
    
    # Determiner le nombre d'enseignants
    nb_teachers = 0
    for user in users:
        groups = user.groups.all()
        for group in groups:
            if group.name in "Enseignant":
                nb_teachers += 1
                break
            
    # Determiner le nombre d'étudiants inscris cette année
    inscriptions = Inscription.objects.filter(anneeacademique_id=anneeacademique_id)
    nb_students = 0
    for i in inscriptions:
        if i.salle.classe.id == classe.id:
            nb_students += 1
            
            
    # Absence des administrateurs
    date_actuelle = date.today()
    absences_admin = AbsenceAdmin.objects.filter(date_absence=date_actuelle)
    
    # Absence des enseignants
    absences_enseignants = Absence.objects.filter(date_absence=date_actuelle)
    
    # Compter les nouveaux contacts 
    contacts_students = (Contact.objects.values("student_id")
                    .filter(anneeacademique_id=anneeacademique_id, user_id=user_id, sending_status=False, reading_status=0)
                    .annotate(nombre_messages=Count("student_id"))
    )
    nombre_contacts_students = 0
    for contact in contacts_students:
        nombre_contacts_students += contact["nombre_messages"]
        
    contacts_parents = (Contact.objects.values("parent_id")
                    .filter(anneeacademique_id=anneeacademique_id, user_id=user_id, sending_status=False, reading_status=0)
                    .annotate(nombre_messages=Count("parent_id"))
    )
    nombre_contacts_parents = 0
    for contact in contacts_parents:
        nombre_contacts_parents += contact["nombre_messages"]
        
    nombre_contacts = nombre_contacts_students + nombre_contacts_parents
    nombre_messages = Message.objects.filter(anneeacademique_id=anneeacademique_id, beneficiaire_id=user_id, reading_status=0).count()
    
    # Total des étudiants inscris chaque années
    groupes_inscriptions = Inscription.objects.values("anneeacademique_id").annotate(nombre_students=Count('student_id')).order_by("-anneeacademique_id")[:5]
    inscriptions = []
    for gi in groupes_inscriptions:
        anneeacademique = AnneeCademique.objects.get(id=gi["anneeacademique_id"])
        dic = {}
        dic["anneeacademique"] = anneeacademique
        dic["nombre_students"] = gi["nombre_students"]
        inscriptions.append(dic)
    
    context = {
        "setting": setting,
        "activity": activity,
        "activity_status": activity_status,
        "activities": activities,
        "nb_admin": nb_amin,
        "nb_teachers": nb_teachers,
        "nb_students": nb_students,
        "absences_admin": absences_admin,
        "absences_enseignants": absences_enseignants,
        "nombre_contacts": nombre_contacts,
        "nombre_messages": nombre_messages,
        "inscriptions": inscriptions
        
    }
    return render(request, "settings/dashboard.html", context=context)

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=permission_promoteur_enseignant)
def db(request):
    anneeacademique_id = request.session.get('anneeacademique_id')
    enseignant_id = request.user.id
    setting = get_setting(anneeacademique_id)
    if setting is None:
        return redirect("settings/maintenance")
    
    # Récuperer la dernière activité
    activity = Activity.objects.filter(anneeacademique_id=anneeacademique_id, type="Privée").order_by('-id').first()
    
    activity_status = False
    if activity:
        date_actuelle = date.today()
        if date_actuelle == activity.date:
            activity_status = True
    # Récuperer toutes les activités
    activities = Activity.objects.filter(anneeacademique_id=anneeacademique_id, type="Privée").order_by('-id')
        
    # Calucler le nombre total d'élèves inscris dans les salles de l'enseignant
    salles_enseignements = (Enseigner.objects.values("salle_id")
                            .filter(enseignant_id=enseignant_id, anneeacademique_id=anneeacademique_id)
                            .annotate(nombres_matieres=Count("matiere"))
    ) 
    
    nombre_eleves = 0
    for se in salles_enseignements:
        nombre_eleves += Inscription.objects.filter(salle_id=se["salle_id"], anneeacademique_id=anneeacademique_id).count()    
        
    # Determiner le salaire exact de l'enseignant du mois actuel
    date_actuel = date.today() # date actuelle
    month_actuel = date_actuel.strftime("%m") # Mois actuel
    month = format_mois(month_actuel)
    
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
                    
                dic_em["hour"] = format_temps(total_delta)
                
                list_emargements.append(dic_em)     
            
            dic_matiere["emargements"] = list_emargements        
            
            dic_matiere["total_time"] = format_temps(total_delta)
            
            # Calculer le montant à payer pour cette matière
            dic_matiere["montant_total_matiere"] = calcul_montant(enseignement.cout_heure, format_temps(total_delta))
            
            total_matiere_delta += total_delta
            
            matieres.append(dic_matiere)
        
        dic["total_matiere_time"] = format_temps(total_matiere_delta)
        dic["matieres"] = matieres
        
        montant_total = calcul_montant(somme_cout_heure, format_temps(total_matiere_delta))
        dic["montant_total_salle"] = montant_total
        tabEmargements.append(dic)
        total_salle_delta += total_matiere_delta
        
        montant_payer += montant_total
    
    # Récuperer les administrateurs
    users = User.objects.all()
    administrateurs = []
    nombre_admin = 0
    for user in users:
        if user.groups.exists():
            groups = user.groups.all()
            for group in groups:
                if group.name in ["Promoteur", "Directeur Général", "Directeur des Etudes", "Gestionnaire"]:
                    dic = {}
                    dic["administrateur"] = user
                    dic["nombre_groupes"] = user.groups.all().count() # Nombre de groupes de l'utilisateur
                    if dic not in administrateurs:
                        nombre_admin += 1
                        administrateurs.append(dic)

    # Nombre total d'étudiants inscris cette année
    nombre_total_student_inscris = Inscription.objects.filter(anneeacademique_id=anneeacademique_id).count()
    # Récuperer les enseignants de cetta année
    # Calucler le nombre total d'élèves inscris dans les salles de l'enseignant
    enseignants = []
    nombre_enseignants = 0
    for user in users:
        if user.groups.exists():
            groups = user.groups.all()
            for group in groups:
                if group.name == "Enseignant":
                    dic = {}
                    dic["enseignant"] = user
                    dic["nombre_groupes"] = user.groups.all().count() # Nombre de groupes de l'utilisateur
                    nombre_enseignants += 1
                    
                    enseignants.append(dic) 
        
    # Nombre de nouvelles payes de l'enseignant
    nombre_renumerations = Renumeration.objects.filter(personnel_id=enseignant_id, anneeacademique_id=anneeacademique_id, status=False).count()
    # Nombre d'absences de l'enseignants
    absences_groupes = (Absence.objects.values("salle_id")
                        .filter(enseignant_id=enseignant_id, anneeacademique_id=anneeacademique_id, status=False)
                        .annotate(nombre_absences=Count("salle_id"))
    )
    absence_totale = 0
    absences_enseignants = []
    for ag in absences_groupes:
        dic = {}
        # Récuperer la salle
        salle = Salle.objects.get(id=ag["salle_id"])
        dic["salle"] = salle
        dic["nombre_absences"] = ag["nombre_absences"]
        absence_totale += ag["nombre_absences"]
        
        absences_enseignants.append(dic)
        
    # Emargements de l'enseignants
    emargements_groupes = (Emargement.objects.values("salle_id")
                        .filter(enseignant_id=enseignant_id, anneeacademique_id=anneeacademique_id, status=False)
                        .annotate(nombre_emargements=Count("salle_id"))
    )
    emargements_total = 0
    emargements_enseignants = []
    for ag in emargements_groupes:
        dic = {}
        # Récuperer la salle
        salle = Salle.objects.get(id=ag["salle_id"])
        dic["salle"] = salle
        dic["nombre_emargements"] = ag["nombre_emargements"]
        emargements_total += ag["nombre_emargements"]
        emargements_enseignants.append(dic)
        
    nombre_absences = AbsenceAdmin.objects.filter(user_id=request.user.id, anneeacademique_id=anneeacademique_id, status=False).count()
    
    nombre_messages = Message.objects.filter(anneeacademique_id=anneeacademique_id, beneficiaire_id=request.user.id, reading_status=0).count()
    
    
    #============================== Récette =========================
    
    months = months_actives(anneeacademique_id)
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
            sum_renum = somme_total_renum_salle(me["salle_id"], anneeacademique_id, month)
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
    
    # Total des étudiants inscris chaque années
    groupes_inscriptions = Inscription.objects.values("anneeacademique_id").annotate(nombre_students=Count('student_id')).order_by("-anneeacademique_id")[:5]
    inscriptions = []
    for gi in groupes_inscriptions:
        anneeacademique = AnneeCademique.objects.get(id=gi["anneeacademique_id"])
        dic = {}
        dic["anneeacademique"] = anneeacademique
        dic["nombre_students"] = gi["nombre_students"]
        inscriptions.append(dic)
    
    group_name = request.session.get('group_name')
    template = ''
    if group_name in permission_promoteur_DG:
        template = 'global/base_sup_admin.html'
                  
    if group_name in ["Enseignant", "Surveillant Général"]:
        template = 'global/base.html' 
        
    context = {
        "setting": setting,
        "activities": activities,
        "activity": activity,
        "activity_status": activity_status,
        "montant_payer": montant_payer,
        "nombre_eleves": nombre_eleves,
        "administrateurs": administrateurs,
        "nombre_admin": nombre_admin,
        "nombre_total_student_inscris": nombre_total_student_inscris,
        "enseignants": enseignants,
        "nombre_enseignants": nombre_enseignants,
        "nombre_renumerations": nombre_renumerations,
        "absences_enseignants": absences_enseignants,
        "absence_totale": absence_totale,
        "emargements_enseignants": emargements_enseignants,
        "emargements_total": emargements_total,
        "nombre_absences": nombre_absences,
        "nombre_messages": nombre_messages,
        "caisses": caisses,
        "inscriptions": inscriptions,
        "template": template
    }
    
    return render(request, "settings/db.html", context)

@unauthenticated_customer
def home(request):
    anneeacademique_id = request.session.get('anneeacademique_id')
    student_id = request.session.get('student_id')
    setting = get_setting(anneeacademique_id)
    if setting is None:
        return redirect("settings/maintenance")
    
    # Nombre de nouveaux paiements
    nombre_nouveaux_payments = Payment.objects.filter(student_id=student_id, anneeacademique_id=anneeacademique_id, status=False).count()
    # Nombre de nouvelles absences
    absences_students = Absencestudent.objects.filter(student_id=student_id, status=False)
    nombre_absences_students = 0
    for absence in absences_students:
        if absence.emargement.anneeacademique.id == anneeacademique_id:
            nombre_absences_students += 1
    # Nombre de compositions des étudiants
    nombre_nouvelles_compositions = Composer.objects.filter(student_id=student_id, anneeacademique_id=anneeacademique_id, status=False).count()
    nombre_gestions_etudes =  nombre_absences_students + nombre_nouvelles_compositions
    
    #=========================== Cas du parent ===========================
    parent_id = request.session.get('parent_id')
    # Récuperer les enfants du parent
    students_parents = Student.objects.filter(parent_id=parent_id) 
    # Selectionner les enfants du parent qui sont inscris cette année
    tabinscription_parents = []
    tabstudents = []
    for student in students_parents:
        query = Inscription.objects.filter(anneeacademique_id=anneeacademique_id, student_id=student.id)
        if query.exists():
            # Récuperer l'inscription
            inscription = query.first()
            tabinscription_parents.append(inscription)
            tabstudents.append(student)
            
    # Nombre de nouveaux paiements des enfants
    nombres_nouveaux_paiements_parents = 0
    paiements_parents = []
    for student in tabstudents:
        dic = {}
        dic["student"] = student
        nombre_payes = Payment.objects.filter(anneeacademique_id=anneeacademique_id, student_id=student.id, status_parent=False).count()
        dic["nombre_payes"] = nombre_payes
        nombres_nouveaux_paiements_parents += nombre_payes
        paiements_parents.append(dic)
        
    gestions = []    
    total_gestion_etudes = 0   
    for inscription in tabinscription_parents:
        dic = {}
        dic["inscription"] = inscription
        # Absence des étudiants
        absences = Absencestudent.objects.filter(student_id=inscription.student.id, status_parent=0)
        nombre_absences = 0
        for absence in absences:
            if absence.emargement.anneeacademique.id == anneeacademique_id:
                nombre_absences += 1
        
        dic["nombre_absences"] = nombre_absences
        # Récuperer les composition de l'étudiant        
        nombre_compositions = Composer.objects.filter(anneeacademique_id=anneeacademique_id, student_id=inscription.student.id, status_parent=0).count()
            
        dic["nombre_compositions"] = nombre_compositions
        
        total_gestion_etudes += nombre_compositions + nombre_absences
        
        gestions.append(dic)
        
    # Nombre de nouveau contacts
    nombre_contacts_students = Contact.objects.filter(student_id=student_id, sending_status=True, reading_status=0, anneeacademique_id=anneeacademique_id).count() 
    # Nombre de notification des parents
    nombre_notifications_parents = Notification.objects.filter(parent_id=parent_id, anneeacademique_id=anneeacademique_id, status=False).count()      
    context = {
        "setting": setting,
        "nombre_nouveaux_payments": nombre_nouveaux_payments,
        "nombre_absences_students": nombre_absences_students,
        "nombre_nouvelles_compositions": nombre_nouvelles_compositions,
        "nombre_gestions_etudes": nombre_gestions_etudes,
        "inscriptions_parents": tabinscription_parents,
        "nombres_nouveaux_paiements_parents": nombres_nouveaux_paiements_parents,
        "paiements_parents": paiements_parents,
        "gestions": gestions,
        "total_gestion_etudes": total_gestion_etudes,
        "nombre_contacts_students": nombre_contacts_students,
        "nombre_notifications_parents": nombre_notifications_parents
    }
    return render(request, "settings/home.html", context=context)

# =============================== Gestion des études ====================================
@unauthenticated_customer
def resources_admin(request):
    anneeacademique_id = request.session.get('anneeacademique_id')
    setting = get_setting(anneeacademique_id)
    if setting is None:
        return redirect("settings/maintenance")
    
    student_id = request.session.get('student_id')
    # Récuperer l'année academique 
    anneeacademique = AnneeCademique.objects.get(id=anneeacademique_id)
    
    inscription = Inscription.objects.filter(anneeacademique_id=anneeacademique_id, student_id=student_id).first()
    programmes = Programme.objects.filter(anneeacademique_id=anneeacademique_id, salle_id=inscription.salle.id).select_related('matiere')
    
    trimestres_enseignements = (Enseigner.objects.values("trimestre")
                     .filter(anneeacademique_id=anneeacademique_id, salle_id=inscription.salle.id)
                     .annotate(nb_trimestre=Count("trimestre")))
    
    tabEnseignements = []   
    i = 0 
    for te in trimestres_enseignements:
        i += 1
        dic = {}
        
        dic["i"] = i
        dic["trimestre"] = te["trimestre"]
        enseignements = Enseigner.objects.filter(anneeacademique_id=anneeacademique_id, salle_id=inscription.salle.id, trimestre=te["trimestre"])
        dic["enseignements"] = enseignements
        tabEnseignements.append(dic)
        
    # Calendriers
    evenements_groupes = (EvenementScolaire.objects.values("trimestre_id")
                              .annotate(nombres_evenements=Count("trimestre_id"))
    )
    
    tabEvenements = []
    for eg in evenements_groupes:
        
        trimestre = Trimestre.objects.get(id=eg["trimestre_id"])
        if trimestre.anneeacademique.id == anneeacademique_id:
            dic = {}
            dic["trimestre"] = trimestre
            dic["nombres_evenements"] = eg["nombres_evenements"]
            dic["evenements"] = trimestre.evenementscolaires.all()
            tabEvenements.append(dic)
    
    # Liste des sujets
    subjects = ['Réclamation de notes', 'Harcèlement', 'Paiement des frais']      
    context = {
        "setting": setting,
        "programmes": programmes,
        "enseignements": tabEnseignements,
        "evenements": tabEvenements,
        "anneeacademique": anneeacademique,
        "subjects": subjects
    }
    return render(request, "settings/resources_admin.html", context=context)


# =============================== Gestion des études ====================================
@unauthenticated_customer
def resources_admin_parent(request):
    anneeacademique_id = request.session.get('anneeacademique_id')
    setting = get_setting(anneeacademique_id)
    if setting is None:
        return redirect("settings/maintenance")
    
    # Récuperer l'année academique 
    anneeacademique = AnneeCademique.objects.get(id=anneeacademique_id)
    
    parent_id = request.session.get('parent_id')
    # Récuperer les enfants du parent
    students_parents = Student.objects.filter(parent_id=parent_id) 
    # Selectionner les enfants du parent qui sont inscris cette année
    tabinscription_parents = []
    tabstudents = []
    for student in students_parents:
        query = Inscription.objects.filter(anneeacademique_id=anneeacademique_id, student_id=student.id)
        if query.exists():
            # Récuperer l'inscription
            inscription = query.first()
            tabinscription_parents.append(inscription)
            tabstudents.append(student)
    
    resources = []
    for inscription in tabinscription_parents: 
        resource_dic = {}
        resource_dic["inscription"] = inscription
        programmes = Programme.objects.filter(anneeacademique_id=anneeacademique_id, salle_id=inscription.salle.id).select_related('matiere')
        resource_dic["programmes"] = programmes
        trimestres_enseignements = (Enseigner.objects.values("trimestre")
                        .filter(anneeacademique_id=anneeacademique_id, salle_id=inscription.salle.id)
                        .annotate(nb_trimestre=Count("trimestre")))
        
        tabEnseignements = []   
        i = 0 
        for te in trimestres_enseignements:
            i += 1
            dic = {}
            
            dic["i"] = i
            dic["trimestre"] = te["trimestre"]
            enseignements = Enseigner.objects.filter(anneeacademique_id=anneeacademique_id, salle_id=inscription.salle.id, trimestre=te["trimestre"])
            dic["enseignements"] = enseignements
            tabEnseignements.append(dic)
        
        resource_dic["enseignements"] = tabEnseignements
        resources.append(resource_dic)
        
    # Calendriers
    evenements_groupes = (EvenementScolaire.objects.values("trimestre_id")
                              .annotate(nombres_evenements=Count("trimestre_id"))
    )
    
    tabEvenements = []
    for eg in evenements_groupes:
        
        trimestre = Trimestre.objects.get(id=eg["trimestre_id"])
        if trimestre.anneeacademique.id == anneeacademique_id:
            dic = {}
            dic["trimestre"] = trimestre
            dic["nombres_evenements"] = eg["nombres_evenements"]
            dic["evenements"] = trimestre.evenementscolaires.all()
            tabEvenements.append(dic)
    
    # Liste des sujets
    subjects = ['Réclamation de notes', 'Harcèlement', 'Paiement des frais']      
    context = {
        "setting": setting,
        "resources": resources,
        "enseignements": tabEnseignements,
        "evenements": tabEvenements,
        "anneeacademique": anneeacademique,
        "subjects": subjects
    }
    return render(request, "settings/resources_admin_parent.html", context=context)

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=permission_utilisateur)
def resources_admin_user(request):
    anneeacademique_id = request.session.get('anneeacademique_id')
    setting = get_setting(anneeacademique_id)
    if setting is None:
        return redirect("settings/maintenance")
    
    # Récuperer l'année academique 
    anneeacademique = AnneeCademique.objects.get(id=anneeacademique_id)
    
    programmes_groupes = (
        Programme.objects.values('salle_id')
        .filter(anneeacademique_id=anneeacademique_id)
        .annotate(nombre_matieres=Count('matiere'))
    )

    liste_programmes = []
    for programme in programmes_groupes:
        dic = {}
        # Récuperer la salle
        salle = Salle.objects.get(id=programme["salle_id"])
        dic["salle"] = salle
        dic["nombre_matieres"] = programme["nombre_matieres"]
        # Récuperer tous les programmes de cette salle
        dic["programmes"] = Programme.objects.filter(anneeacademique_id=anneeacademique_id, salle_id=salle.id)
        liste_programmes.append(dic)
        
    enseignements_groupes = (
        Enseigner.objects.values('salle_id')
        .filter(anneeacademique_id=anneeacademique_id)
        .annotate(nombre_trimestre=Count('trimestre'))
    )

    liste_enseignements = []
    for enseignement in enseignements_groupes:
        dic_enseignement = {}
        # Récuperer la salle
        salle = Salle.objects.get(id=enseignement["salle_id"])
        dic_enseignement["salle"] = salle
        
        trimestres_enseignements = (Enseigner.objects.values("trimestre")
                        .filter(anneeacademique_id=anneeacademique_id, salle_id=salle.id)
                        .annotate(nb_matieres=Count("matiere")))
        
        tabEnseignements = []   
        i = 0 
        for te in trimestres_enseignements:
            i += 1
            dic = {}
            dic["i"] = i
            dic["trimestre"] = te["trimestre"]
            enseignements = Enseigner.objects.filter(anneeacademique_id=anneeacademique_id, trimestre=te["trimestre"])
            dic["enseignements"] = enseignements
            tabEnseignements.append(dic)
            
        dic_enseignement["enseignements"] = tabEnseignements
        liste_enseignements.append(dic_enseignement)
        
    # Calendriers
    evenements_groupes = (EvenementScolaire.objects.values("trimestre_id")
                              .annotate(nombres_evenements=Count("trimestre_id"))
    )
    
    tabEvenements = []
    for eg in evenements_groupes:
        
        trimestre = Trimestre.objects.get(id=eg["trimestre_id"])
        if trimestre.anneeacademique.id == anneeacademique_id:
            dic = {}
            dic["trimestre"] = trimestre
            dic["nombres_evenements"] = eg["nombres_evenements"]
            dic["evenements"] = trimestre.evenementscolaires.all()
            tabEvenements.append(dic)
        
    # Liste des sujets
    subjects = ['Réclamation de notes', 'Harcèlement', 'Harcèlement', 'Paiement des frais']  
    # Récuperer les administrateurs
    administrateurs = []
    users = User.objects.all()
    for user in users:
        if user.groups.exists():
            groups = user.groups.all()
            dic = {}
            dic["administrateur"] = user
            for group in groups:
                if group.name in ["Promoteur", "Directeur Général", "Directeur des Etudes", "Gestionnaire"]:                       
                    if dic not in administrateurs:
                        dic["group"] = group.name
                        administrateurs.append(dic)
    
    context = {
        "setting": setting,
        "programmes": liste_programmes,
        "enseignements": liste_enseignements,
        "evenements": tabEvenements,
        "anneeacademique": anneeacademique,
        "subjects": subjects,
        "administrateurs": administrateurs
    }
    return render(request, "settings/resources_admin_user.html", context=context)

def need_help(request):  
    anneeacademique_id = request.session.get('anneeacademique_id')
    setting = get_setting(anneeacademique_id)
    if setting is None:
        return redirect("settings/maintenance") 
    
    context = {
        "setting": setting
    }
    return render(request, "settings/help.html", context=context)


@login_required(login_url='connection/login')
@allowed_users(allowed_roles=permission_admin)
def index(request):
    anneeacademique_id = request.session.get('anneeacademique_id')
    group_name = request.session.get('group_name')
    setting = get_setting(anneeacademique_id)    
    if setting is None:
        return redirect("settings/maintenance")
    
    cycles = Cycle.objects.filter(anneeacademique_id=anneeacademique_id)
    tabcycles = []
    for cycle in cycles:
        dic = {}
        dic["cycle"] = cycle
        dic["nombre_classes"] = Classe.objects.filter(cycle_id=cycle.id).count()
        tabcycles.append(dic)
        
    anneeacademique = AnneeCademique.objects.get(id=anneeacademique_id)
    anneeacademiques = AnneeCademique.objects.exclude(id=anneeacademique_id)
    
    user = request.user
    groups = user.groups.all()
    access = False 
    for group in groups:
        if group.name in permission_promoteur_DG:
            access = True
            break
    
    # Supprimer le nom du group principal pour eviter des doublons
    tabgroups = []
    for group in groups:
        if group.name != group_name:
            tabgroups.append(group) 
            
    context = {
        "cycles": tabcycles,
        "anneeacademique": anneeacademique,
        "anneeacademiques": anneeacademiques,
        "permission_promoteur_DG": permission_promoteur_DG,
        "access": access,
        "groups": tabgroups,
        "group_name": group_name,
        "user": user,
        "setting": setting
    }
    return render(request, "index.html", context)

@login_required(login_url='connection/login')
def setting(request):
    anneeacademique_id = request.session.get('anneeacademique_id')
    setting = get_setting(anneeacademique_id)
    
    if setting is None:
        return redirect("settings/maintenance")
    
    setting = Setting.objects.filter(anneeacademique_id=anneeacademique_id).order_by("-id")[0]    
        
    context = {
        "setting": setting
    }
    return render(request, "settings/setting.html",context)
    
@login_required(login_url='connection/login')
@allowed_users(allowed_roles=permission_promoteur_DG)
def setting_supuser(request):
    anneeacademique_id = request.session.get('anneeacademique_id')
    setting = get_setting(anneeacademique_id)
    
    if setting is None:
        return redirect("settings/maintenance")
    else:       
        if request.method == "POST":           
            id = request.POST["id"]
            if id:                
                sett = Setting.objects.get(id=id)
                appname = bleach.clean(request.POST["appname"].strip())
                appeditor = bleach.clean(request.POST["appeditor"].strip())
                version = bleach.clean(request.POST["version"].strip())
                theme = request.POST["theme"].strip()
                text_color = request.POST["text_color"]
                address = bleach.clean(request.POST["address"].strip())
                devise = bleach.clean(request.POST["devise"].strip())
                email = request.POST["email"]
                
                #On verifie si l'adresse e-mail correspond bien
                regexp = r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$"
                if not re.search(regexp, email):
                    messages.error(request, "Le format de l'adresse e-mail ne correspond pas.")
                else:
                    
                    phone = bleach.clean(request.POST["phone"].strip())
                    logo = None
                    if request.POST.get('logo', True):
                        logo = request.FILES["logo"]
                    width = request.POST["width"].strip()
                    height = request.POST["height"].strip()

                    sett.appname = appname
                    sett.appeditor = appeditor
                    sett.version = version
                    sett.theme = theme
                    sett.text_color = text_color
                    sett.devise = devise
                    sett.address = address
                    sett.email = email
                    sett.phone = phone
                    if logo is not None:
                        sett.logo = logo
                    sett.width_logo = width
                    sett.height_logo = height
                    sett.anneeacademique_id = anneeacademique_id

                    sett.save()
                    messages.success(request, "Paramètre modifié avec succès.")
                    return redirect("settings/setting_supuser")
            else:
                appname = bleach.clean(request.POST["appname"].strip())
                appeditor = bleach.clean(request.POST["appeditor"].strip())
                version = bleach.clean(request.POST["version"].strip())
                theme = request.POST["theme"]
                text_color = request.POST["text_color"]
                address = bleach.clean(request.POST["address"].strip())
                devise = bleach.clean(request.POST["devise"].strip())
                email = request.POST["email"]
                #On verifie si l'adresse e-mail correspond bien
                regexp = r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$"
                if not re.search(regexp, email):
                    messages.error(request, "Le format de l'adresse e-mail ne correspond pas.")
                else:
                    phone = bleach.clean(request.POST["phone"].strip())
                    logo = None
                    if request.POST.get('logo', True):
                            logo = request.FILES["logo"]
                    width = bleach.clean(request.POST["width"].strip())
                    height = bleach.clean(request.POST["height"].strip())

                    sett = Setting(
                        appname = appname,
                        appeditor = appeditor,
                        version = version,
                        theme = theme,
                        text_color = text_color,
                        devise = devise,
                        address = address,
                        email = email,
                        phone = phone,
                        logo = logo,
                        width_logo = width,
                        height_logo = height,
                        anneeacademique_id =  anneeacademique_id)
                    
                    sett.save()
                    messages.success(request, "Paramètre enregistré avec succès.")
                    return redirect("settings/setting_supuser")

        context = {
            "setting": setting
        }
        return render(request, "settings/setting_supuser.html",context)
    
class ajaxyear(View):
    def get(self, request, id, *args, **kwargs):
        setting = get_setting(id)
        print(id)
        anneeacademique = AnneeCademique.objects.get(id=id)
        request.session["anneeacademique_id"] = anneeacademique.id
        request.session["annee_debut"] = anneeacademique.annee_debut
        request.session["annee_fin"] = anneeacademique.annee_fin
        request.session["separateur"] = anneeacademique.separateur

        anneeacademiques = AnneeCademique.objects.exclude(id=id)       
        
        user = request.user
        groups = user.groups.all()
        group_name = request.session.get('group_name')
        
        # Supprimer le nom du group principal pour eviter des doublons
        tabgroups = []
        for group in groups:
            if group.name != group_name:
                tabgroups.append(group) 
              
        
        cycles = Cycle.objects.filter(anneeacademique_id=id)
        tabcycles = []
        for cycle in cycles:
            dic = {}
            dic["cycle"] = cycle
            dic["nombre_classes"] = Classe.objects.filter(cycle_id=cycle.id, anneeacademique_id=id)
            tabcycles.append(dic)
            
        context = {
            "setting": setting,
            "groups": tabgroups,
            "anneeacademique": anneeacademique,
            "anneeacademiques": anneeacademiques,
            "cycles": tabcycles
        }
        return render(request, "ajaxyear.html", context)
    
class fetchgroup(View):
    def get(self, request, id, *args, **kwargs):

        user = User.objects.get(id=id)
        tabGroup = []
        for g in user.groups.all():
            tabGroup.append(g)

        context = {
            "groupes": tabGroup,
            "user": user
        }
        return render(request, "fetchgroup.html", context)
    
class ajax_group_name(View):
    def get(self, request, group_name, *args, **kwargs):
        anneeacademique_id = request.session.get('anneeacademique_id') 
        setting = get_setting(anneeacademique_id)
        user = request.user
        groups = user.groups.all()
        request.session["group_name"] = group_name
        
        # Supprimer le nom du group principal pour eviter des doublons
        tabgroups = []
        for group in groups:
            if group.name != group_name:
                tabgroups.append(group) 
              
        anneeacademique = AnneeCademique.objects.get(id=anneeacademique_id)
        anneeacademiques = AnneeCademique.objects.exclude(id=anneeacademique_id)
        
        cycles = Cycle.objects.filter(anneeacademique_id=anneeacademique_id)
        tabcycles = []
        for cycle in cycles:
            dic = {}
            dic["cycle"] = cycle
            dic["nombre_classes"] = Classe.objects.filter(cycle_id=cycle.id, anneeacademique_id=anneeacademique_id)
            tabcycles.append(dic)
        context = {
            "setting": setting,
            "groups": tabgroups,
            "anneeacademique": anneeacademique,
            "anneeacademiques": anneeacademiques,
            "cycles": tabcycles
        }
        return render(request, "ajax_group_name.html", context)

def send_sms(to, message):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=message,
        from_=settings.TWILIO_PHONE_NUMBER,
        to=to
    )
    return message.sid  # tu peux logguer ou afficher l'ID si besoin


def send_message(request):
    to = '+330755873258'  # numéro du destinataire
    msg = "Bonjour Monsieur Ngalebo Le Prince d'avoir inscris votre enfant dans notre école"
    sid = send_sms(to, msg)
    
    return redirect('settings/help')