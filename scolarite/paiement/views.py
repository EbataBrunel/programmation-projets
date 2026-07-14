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
from django.views import View
from decimal import Decimal
from django.core.exceptions import ObjectDoesNotExist
from datetime import date
from django.http.response import HttpResponse
from django.template.loader import get_template
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
# Importation des modules locaux
from .models import*
from school.views import get_setting
from inscription.models import Inscription
from anneeacademique.models import AnneeCademique
from app_auth.models import Parent, Student
from app_auth.decorator import allowed_users, unauthenticated_customer

permission_gestionnaire = ['Promoteur', 'Directeur Général', 'Gestionnaire']
#=================================== Définition des mois ===================================== 
def format_month(month):
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
    
def periode_annee_scolaire(anneeacademique_id):
    try:
        anneeacademique = AnneeCademique.objects.get(id=anneeacademique_id)
    except ObjectDoesNotExist:
        return []  # Retourne une liste vide si l'année académique n'existe pas

    start_date = anneeacademique.start_date
    end_date = anneeacademique.end_date

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

def debut_month_actuel(anneeacademique_id): # Liste des mois du début de la peéiode de l'année scolaire jusqu'au mois actuel
    # Récuperer tous les mois de l'année académique
    months = periode_annee_scolaire(anneeacademique_id)
    date_actuel = date.today() # date actuelle
    month_actuel = date_actuel.strftime("%m") # Mois actuel
    month_actuel = format_month(month_actuel)
    # Récuperer les tous mois du début de la rentrée jusqu'au mois actuel
    tabMonths = []
    for month in months:
        if month == month_actuel:
            tabMonths.append(month)
            break
        else:
            tabMonths.append(month)
    return tabMonths

# Recuperer les mois aux quels les élèves ont payé dans cette période scolaire
def month_payment(anneeacademique_id):
    tabMonths = []
    months = periode_annee_scolaire(anneeacademique_id) # Récuperer tous les mois de l'année scolaire
    liste_months = debut_month_actuel(anneeacademique_id) # Liste des mois allant du début de la periode de l'année scolaire jusqu'au mois actuel
    
    for  month in months:
        if month in liste_months:
            tabMonths.append(month)
        else:
            if Payment.objects.filter(month=month, anneeacademique_id=anneeacademique_id).exists():
                tabMonths.append(month)
    return tabMonths

# Recuperer les mois aux quels les élèves ont payé allant du mois actuel au dernier mois de la période scolaire
def payment_month_actuel_dernier(anneeacademique_id):
    tabMonths = []
    months = periode_annee_scolaire(anneeacademique_id) # Récuperer tous les mois de l'année scolaire
    liste_months = debut_month_actuel(anneeacademique_id) # Liste des mois allant du début de la periode de l'année scolaire jusqu'au mois actuel
    
    for  month in months:
        if (month in liste_months) or Payment.objects.filter(month=month, anneeacademique_id=anneeacademique_id).exists():
            continue
        else:
            tabMonths.append(month)
    return tabMonths

# Verifier si l'élève à payer tous les mois précèdant aux quels il est autorisé à payer
def payment_next_month(month, salle_id, student_id, anneeacademique_id):
    # Récuperer la période de l'année scolaire
    months = periode_annee_scolaire(anneeacademique_id)
    print(month)
    print(months)
    # Recuperer les mois précédants
    tabmonths = []
    for m in months:
        if m == month:
            break
        else:
            tabmonths.append(m)
    print(tabmonths)
    tabnewmonth = []
    for m in tabmonths:
        # Verifier si l'étudiant n'est pas autorisé à payer ce mois
        query_autorisation = AutorisationPayment.objects.filter(salle_id=salle_id, student_id=student_id, anneeacademique_id=anneeacademique_id, month=m)
        # Verifier si les étudiants de cette salle ne sont pas autorisés à payer ce mois 
        query_autorisation_salle = AutorisationPaymentSalle.objects.filter(salle_id=salle_id, anneeacademique_id=anneeacademique_id, month=m)
        if query_autorisation_salle.exists() or query_autorisation.exists():
            pass
        else:
            tabnewmonth.append(m)
            
    print(tabnewmonth)       
    status_paiement = False       
    for m in tabnewmonth:
        query = Payment.objects.filter(salle_id=salle_id, student_id=student_id, anneeacademique_id=anneeacademique_id, month=m)  
        if query.exists():
            pass
        else:
            status_paiement = True
            break
        
    return status_paiement 
# ====================================== Gestion de paiements ======================================

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=permission_gestionnaire)
def payments(request):
    anneeacademique_id = request.session.get('anneeacademique_id')
    setting = get_setting(anneeacademique_id)
    if setting is None:
        return redirect("settings/maintenance")
    
    classe_id = request.session.get('classe_id')
    salles_payments = (Payment.objects.values("salle_id")
                     .filter(anneeacademique_id = anneeacademique_id)
                     .annotate(effectif=Count("salle_id")))
    
    tabSalles = []
    for sp in salles_payments:        
        salle = Salle.objects.get(id=sp["salle_id"])               
        if salle.classe.id == classe_id:
            # Compter le nombre d'étudiants qui ont payé
            students_payments = (Payment.objects.values("student_id")
                                 .filter(anneeacademique_id = anneeacademique_id, salle_id=salle.id)
                                 .annotate(nb_payment=Count('student_id')))
            nb_students = 0
            for st in students_payments:
                nb_students += 1
            dic = {}
            dic["salle"] = salle
            dic["nb_students"] = nb_students
            tabSalles.append(dic)

    anneeacademique = AnneeCademique.objects.get(id=anneeacademique_id) 
    context = {
        "setting": setting,
        "salles": tabSalles,
        "anneeacademique": anneeacademique
    }
    return render(request, "payments.html", context)

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=permission_gestionnaire)
def students_payments(request, salle_id):
    anneeacademique_id = request.session.get('anneeacademique_id')
    setting = get_setting(anneeacademique_id)
    if setting is None:
        return redirect("settings/maintenance")

    students_payments = (Payment.objects.values("student_id")
                     .filter(anneeacademique_id = anneeacademique_id, salle_id=salle_id)
                     .annotate(nb_payments=Count("student_id")))
    
    tabStudents = []
    for sp in students_payments:        
        student = Student.objects.get(id=sp["student_id"])               
        dic = {}
        dic["student"] = student
        dic["nb_payments"] = sp["nb_payments"]
        tabStudents.append(dic)
                
    salle = Salle.objects.get(id=salle_id)
    anneeacademique = AnneeCademique.objects.get(id=anneeacademique_id) 
    context = {
        "setting": setting,
        "students": tabStudents,
        "salle": salle,
        "anneeacademique": anneeacademique
    }
    return render(request, "students_payments.html", context)  

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=permission_gestionnaire)
def detail_payment(request, salle_id, student_id):
    anneeacademique_id = request.session.get('anneeacademique_id')
    setting = get_setting(anneeacademique_id)
    if setting is None:
        return redirect("settings/maintenance")
    
    salle = Salle.objects.get(id=salle_id)
    student = Student.objects.get(id=student_id)
    payments = Payment.objects.filter(salle_id=salle_id, student_id=student_id, anneeacademique_id=anneeacademique_id)
    
    # Récuperer tous les mois de l'année académique
    months = periode_annee_scolaire(anneeacademique_id)
    date_actuel = date.today() # date actuelle
    month_actuel = date_actuel.strftime("%m") # Mois actuel
    month_actuel = format_month(month_actuel)
    # Récuperer tous les mois du début de la rentrée jusqu'au mois actuel
    tabMonths = []
    for month in months:
        if month == month_actuel:
            tabMonths.append(month)
            break
        else:
            tabMonths.append(month)
            
    # Récuperer tous les paiements de l'étudiant du début de la rentrée jusqu'à ce jour
    tabMonthPaye = []
    montant_restant = 0
    for month in tabMonths:
        dic = {}
        dic["month"] = month
        # Verifier si l'élève est autoriser à payer ce mois ou pas
        autorisation = AutorisationPayment.objects.filter(salle_id=salle_id, student_id=student_id, month=month, anneeacademique_id=anneeacademique_id)
        # Verifier si les élèves de cette salles sont autorisés à payer ce mois
        query_autorisation_salle = AutorisationPayment.objects.filter(salle_id=salle_id, month=month, anneeacademique_id=anneeacademique_id)
        if autorisation.exists() or query_autorisation_salle.exists():
            dic["status"] = "Ne paye pas"
        else:
            payment = Payment.objects.filter(salle_id=salle_id, student_id=student_id, month=month, anneeacademique_id=anneeacademique_id)
            if payment.exists():
                paye = payment.first()
                if paye.amount < salle.price:
                    dic["status"] = "Avance"
                    montant_restant += (salle.price - paye.amount)
                else:
                    dic["status"] = "Payé"
            else:
                dic["status"] = "Impayé"
                montant_restant += salle.price
                
        tabMonthPaye.append(dic)
    
    anneeacademique = AnneeCademique.objects.get(id=anneeacademique_id)             
    context = {
        "setting": setting,
        "payments": payments,
        "salle": salle,
        "student": student,
        "montant_restant": montant_restant,
        "months_payes" : tabMonthPaye,
        "anneeacademique": anneeacademique
    }
    return render(request, "detail_payment.html", context)
    

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=permission_gestionnaire)
def add_payment(request):
    anneeacademique_id = request.session.get('anneeacademique_id')
    setting = get_setting(anneeacademique_id)
    if setting is None:
        return redirect("settings/maintenance")
    
    user_id = request.user.id
    classe_id = request.session.get('classe_id')
    if request.method == "POST":

        salle_id = request.POST["salle"]
        student_id = request.POST["student"]
        month = bleach.clean(request.POST["month"].strip())
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
         
        paiements = Payment.objects.filter(salle_id=salle_id, student_id=student_id, anneeacademique_id=anneeacademique_id)   
        for payment in paiements:
            # Recupérer la salle
            salle = Salle.objects.get(id=salle_id)
            if payment.amount < salle.price:
                return JsonResponse({
                    "status": "error",
                    "message": "Completez d'abord les frais d'un mois avant d'effectuer un nouveau paiement."})
        
        # Récuperer la délibération pour verifier si ses activités ont été cloturées ou pas
        anneescolaire = AnneeCademique.objects.filter(status_cloture=True, id=anneeacademique_id) 
        # Verifier si l'étudiant est autorisé à payer ce mois ou pas
        query_autorisation = AutorisationPayment.objects.filter(salle_id=salle_id, student_id=student_id, anneeacademique_id=anneeacademique_id, month=month)
        # Verifier si les étudiants ne sont pas autorisés à payer ce mois pour cette salle
        query_autorisation_salle = AutorisationPaymentSalle.objects.filter(salle_id=salle_id, anneeacademique_id=anneeacademique_id, month=month)
        query = Payment.objects.filter(salle_id=salle_id, student_id=student_id, anneeacademique_id=anneeacademique_id, month=month)        
        if anneescolaire.exists(): # Verifier si on a déjà cloturé les opérations de cette année
                return JsonResponse({
                    "status": "error",
                    "message": "Les opérations de cette année académique ont été déjà clôturées."})
        if query_autorisation_salle.exists():
            return JsonResponse({
                    "status": "error",
                    "message": "Les étudiants ne pas autorisés à payer ce mois pour cette salle."})
        if query_autorisation.exists():
            return JsonResponse({
                    "status": "error",
                    "message": "Cet élève n'est pas autorisé à payer ce mois."})
            
        if payment_next_month(month, salle_id, student_id, anneeacademique_id): 
            return JsonResponse({
                    "status": "error",
                    "message": "Il existe au moins un mois précédent que cet élève n'a pas encore payé."})
            
        if query.exists():
            return JsonResponse({
                    "status": "error",
                    "message": "Ce paiement existe déjà."})
        else:
            payment = Payment(
                salle_id=salle_id, 
                student_id=student_id, 
                user_id=user_id, 
                month=month, 
                amount=amount, 
                anneeacademique_id=anneeacademique_id)
            
            # Nombre de paiement avant l'ajout
            count0 = Payment.objects.all().count()
            payment.save()
            # Nombre de paiements après l'ajout
            count1 = Payment.objects.all().count()
            # On verifie si l'insertion a eu lieu ou pas.
            if count0 < count1:
                return JsonResponse({
                    "status": "success",
                    "message": "Paiement enregistré avec succès."})
            else:
                return JsonResponse({
                    "status": "error",
                    "message": "Le paiement a échoué."})

    salles = Salle.objects.filter(classe_id=classe_id, anneeacademique_id=anneeacademique_id)
    months = periode_annee_scolaire(anneeacademique_id)
    mode_paiements = ["Espèce", "Virement", "Mobile"]
    context={
        "setting": setting,
        "salles": salles,
        "months": months,
        "mode_paiements": mode_paiements
    }
    return render(request, "add_payment.html", context)

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=permission_gestionnaire)
def edit_payment(request,id):
    anneeacademique_id = request.session.get('anneeacademique_id')
    setting = get_setting(anneeacademique_id)
    if setting is None:
        return redirect("settings/maintenance")
    
    classe_id = request.session.get('classe_id')
    payment = Payment.objects.get(id=id)
        
    salles = Salle.objects.filter(classe_id=classe_id, anneeacademique_id=anneeacademique_id).exclude(id=payment.salle.id)
    # Recuperer tous les étudints de cette salle
    inscriptions = Inscription.objects.filter(salle_id=payment.salle.id, anneeacademique_id=anneeacademique_id)
    students = []
    for inscription in inscriptions:
        if payment.student.id != inscription.student.id:
            students.append(inscription.student)
    
    months = periode_annee_scolaire(anneeacademique_id)
    tabMonths = []
    for month in months:
        if month != months:
            tabMonths.append(month)

    mode_paiements = ["Espèce", "Virement", "Mobile"]
    tab_mode_paiements = []
    for mode_paiement in mode_paiements:
        if mode_paiement != payment.mode_paiement:
            tab_mode_paiements.append(mode_paiement)
         
    context = {
        "setting": setting,
        "payment": payment,
        "salles": salles,
        "students": students,
        "months": months,
        "mode_paiements": tab_mode_paiements
    }
    return render(request, "edit_payment.html", context)


@login_required(login_url='connection/login')
@allowed_users(allowed_roles=permission_gestionnaire)
def edit_py(request):
    anneeacademique_id = request.session.get('anneeacademique_id')
    user_id = request.user.id
    if request.method == "POST":
        id = int(request.POST["id"])
        try:
            payment = Payment.objects.get(id=id)
        except:
            payment = None

        if payment is None:
            return JsonResponse({
                    "status": "error",
                    "message": "Identifiant inexistant."})
        else: 
            salle_id = request.POST["salle"]
            student_id = request.POST["student"]
            month = bleach.clean(request.POST["month"].strip())
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
                
            # Verifier l'existence du paiement
            payments = Payment.objects.filter(anneeacademique_id=anneeacademique_id, student_id=student_id).exclude(id=id)
            tabPayments = []
            for p in payments:
                dic = {}
                dic["salle_id"] = p.salle.id
                dic["student_id"] = p.student.id
                dic["month"] = p.month 
                
                tabPayments.append(dic)
            
            new_dic = {}
            new_dic["salle_id"] = int(salle_id)
            new_dic["student_id"] = int(student_id)  
            new_dic["month"] = month 
            
            # Récuperer la délibération pour verifier si ses activités ont été cloturées ou pas
            anneescolaire = AnneeCademique.objects.filter(status_cloture=True, id=anneeacademique_id) 
            # Verifier si l'étudiant est autorisé à payer ce mois ou pas
            query_autorisation = AutorisationPayment.objects.filter(salle_id=salle_id, student_id=student_id, anneeacademique_id=anneeacademique_id, month=month)
            # Verifier si les étudiants ne sont pas autorisés à payer ce mois pour cette salle
            query_autorisation_salle = AutorisationPaymentSalle.objects.filter(salle_id=salle_id, anneeacademique_id=anneeacademique_id, month=month)
            if anneescolaire.exists(): # Verifier si on a déjà cloturé les opérations de cette année
                return JsonResponse({
                    "status": "error",
                    "message": "Les opérations de cette année académique ont été déjà clôturées."})
            if query_autorisation_salle.exists():
                return JsonResponse({
                        "status": "error",
                        "message": "Les étudiants ne pas autorisés à payer ce mois pour cette salle."})
            if query_autorisation.exists():
                return JsonResponse({
                        "status": "error",
                        "message": "Cet élève n'est pas autorisé à payer ce mois."})
            
            if new_dic in tabPayments:
                return JsonResponse({
                    "status": "error",
                    "message": "Ce paiement existe déjà."}) 
            else:
                payment.salle_id = salle_id
                payment.student_id = student_id
                payment.month = month
                payment.amount = amount
                payment.user_id = user_id
                payment.save()
                return JsonResponse({
                    "status": "success",
                    "message": "Paiement modifié avec succès."})

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=permission_gestionnaire)
def del_payment(request, id):
    anneeacademique_id = request.session.get('anneeacademique_id')
    setting = get_setting(anneeacademique_id)
    if setting is None:
        return redirect("settings/maintenance")
    
    try:
        payment = Payment.objects.get(id=id)
    except:
        payment = None
        
    if payment:
        # Nombre de paiements avant la suppression
        count0 = Payment.objects.all().count()
        payment.delete()
        # Nombre de paiements après la suppression
        count1 = Payment.objects.all().count()
        if count1 < count0: 
            messages.success(request, "ELément supprimé avec succès.")
        else:
            messages.error(request, "La suppression a échouée.")
    return redirect("detail_payment", payment.salle.id, payment.student.id)


#============================ Gestion des autorisations de payments ==================================
@login_required(login_url='connection/login')
@allowed_users(allowed_roles=permission_gestionnaire)
def autorisation_payments(request):
    anneeacademique_id = request.session.get('anneeacademique_id')
    setting = get_setting(anneeacademique_id)
    if setting is None:
        return redirect("settings/maintenance")
    
    classe_id = request.session.get('classe_id')
    salles_authorisations = (AutorisationPayment.objects.values("salle_id")
                     .filter(anneeacademique_id = anneeacademique_id)
                     .annotate(nb_etudiants=Count("salle_id")))
    
    tabSalles = []
    for sp in salles_authorisations:        
        salle = Salle.objects.get(id=sp["salle_id"])               
        if salle.classe.id == classe_id:
            # Compter le nombre d'étudiants qui ne sont pas autorisés à payer
            nb_students = (AutorisationPayment.objects.values("student_id")
                                 .filter(anneeacademique_id = anneeacademique_id, salle_id=salle.id)
                                 .aggregate(Count('student_id'))['student_id__count'] or 0)        
            dic = {}
            dic["salle"] = salle
            dic["nb_students"] = nb_students
            tabSalles.append(dic)
    anneeacademique = AnneeCademique.objects.get(id=anneeacademique_id) 
    context = {
        "setting": setting,
        "salles": tabSalles,
        "anneeacademique": anneeacademique
    }
    return render(request, "autorisation/autorisation_payments.html", context)

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=permission_gestionnaire)
def detail_autorisation_payments(request, salle_id):
    anneeacademique_id = request.session.get('anneeacademique_id')
    setting = get_setting(anneeacademique_id)
    if setting is None:
        return redirect("settings/maintenance")
    
    students_autorisations = (AutorisationPayment.objects.values("student_id")
                     .filter(anneeacademique_id=anneeacademique_id, salle_id=salle_id)
                     .annotate(nb_autorisations=Count("student_id")))
    
    tabStudents = []
    for sp in students_autorisations:        
        student = Student.objects.get(id=sp["student_id"])               
        dic = {}
        dic["student"] = student
        dic["nb_autorisations"] = sp["nb_autorisations"]
        dic["autorisations"] = AutorisationPayment.objects.filter(anneeacademique_id=anneeacademique_id, salle_id=salle_id, student_id=student.id)
        tabStudents.append(dic)
                
    salle = Salle.objects.get(id=salle_id)
    anneeacademique = AnneeCademique.objects.get(id=anneeacademique_id) 
    context = {
        "setting": setting,
        "students": tabStudents,
        "salle": salle,
        "anneeacademique": anneeacademique
    }
    return render(request, "autorisation/detail_autorisation_payments.html", context)
    

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=permission_gestionnaire)
def add_autorisation_payment(request):
    anneeacademique_id = request.session.get('anneeacademique_id')
    setting = get_setting(anneeacademique_id)
    if setting is None:
        return redirect("settings/maintenance")
    
    user_id = request.user.id
    classe_id = request.session.get('classe_id')
    if request.method == "POST":

        salle_id = request.POST["salle"]
        student_id = request.POST["student"]
        month = bleach.clean(request.POST["month"].strip())
        justification = bleach.clean(request.POST["justification"].strip())
        # Récuperer la délibération pour verifier si ses activités ont été cloturées ou pas
        anneescolaire = AnneeCademique.objects.filter(status_cloture=True, id=anneeacademique_id) 
        query = AutorisationPayment.objects.filter(salle_id=salle_id, student_id=student_id, anneeacademique_id=anneeacademique_id, month=month)        
        if anneescolaire.exists(): # Verifier si on a déjà cloturé les opérations de cette année
                return JsonResponse({
                    "status": "error",
                    "message": "Les opérations de cette année académique ont été déjà clôturées."})
        if query.exists():
            return JsonResponse({
                    "status": "error",
                    "message": "Cette autorisation de paiement existe déjà."})
        else:
            autorisation = AutorisationPayment(
                salle_id=salle_id, 
                student_id=student_id, 
                user_id=user_id, 
                month=month, 
                justification=justification, 
                anneeacademique_id=anneeacademique_id)
            
            # Nombre d'autorisations avant l'ajout
            count0 = AutorisationPayment.objects.all().count()
            autorisation.save()
            # Nombre d'autorisations après l'ajout
            count1 = AutorisationPayment.objects.all().count()
            # On verifie si l'insertion a eu lieu ou pas.
            if count0 < count1:
                return JsonResponse({
                    "status": "success",
                    "message": "Autorisation enregistrée avec succès."})
            else:
                return JsonResponse({
                    "status": "error",
                    "message": "L'autorisation a échouée."})

    salles = Salle.objects.filter(classe_id=classe_id, anneeacademique_id=anneeacademique_id)
    months = periode_annee_scolaire(anneeacademique_id)
    context={
        "setting": setting,
        "salles": salles,
        "months": months
    }
    return render(request, "autorisation/add_autorisation_payment.html", context)

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=permission_gestionnaire)
def edit_autorisation_payment(request,id):
    anneeacademique_id = request.session.get('anneeacademique_id')
    setting = get_setting(anneeacademique_id)
    if setting is None:
        return redirect("settings/maintenance")
    
    classe_id = request.session.get('classe_id')
    autorisation = AutorisationPayment.objects.get(id=id)
        
    salles = Salle.objects.filter(classe_id=classe_id, anneeacademique_id=anneeacademique_id).exclude(id=autorisation.salle.id)
    # Recuperer tous les étudints de cette salle
    inscriptions = Inscription.objects.filter(salle_id=autorisation.salle.id, anneeacademique_id=anneeacademique_id)
    students = []
    for inscription in inscriptions:
        if autorisation.student.id != inscription.student.id:
            students.append(inscription.student)
    
    months = periode_annee_scolaire(anneeacademique_id)
    tabMonths = []
    for month in months:
        if month != months:
            tabMonths.append(month)

    context={
        "setting": setting,
        "autorisation": autorisation,
        "salles": salles,
        "students": students,
        "months": months
    }
    return render(request, "autorisation/edit_autorisation_payment.html", context)


@login_required(login_url='connection/login')
@allowed_users(allowed_roles=permission_gestionnaire)
def edit_ap(request):
    anneeacademique_id = request.session.get('anneeacademique_id')
    user_id = request.user.id
    if request.method == "POST":
        id = int(request.POST["id"])
        try:
            autorisation = AutorisationPayment.objects.get(id=id)
        except:
            autorisation = None

        if autorisation is None:
            return JsonResponse({
                    "status": "error",
                    "message": "Identifiant inexistant."})
        else: 
            salle_id = request.POST["salle"]
            student_id = request.POST["student"]
            month = bleach.clean(request.POST["month"].strip())
            justification = bleach.clean(request.POST["justification"].strip())
             
            # Récuperer la délibération pour verifier si ses activités ont été cloturées ou pas
            anneescolaire = AnneeCademique.objects.filter(status_cloture=True, id=anneeacademique_id)    
            # Verifier l'existence du paiement
            autorisations = AutorisationPayment.objects.filter(anneeacademique_id=anneeacademique_id, student_id=student_id).exclude(id=id)
            tabAutorisations = []
            for p in autorisations:
                dic = {}
                dic["salle_id"] = p.salle.id
                dic["student_id"] = p.student.id
                dic["month"] = p.month 
                
                tabAutorisations.append(dic)
            
            new_dic = {}
            new_dic["salle_id"] = int(salle_id)
            new_dic["student_id"] = int(student_id)  
            new_dic["month"] = month 
            if anneescolaire.exists(): # Verifier si on a déjà cloturé les opérations de cette année
                return JsonResponse({
                    "status": "error",
                    "message": "Les opérations de cette année académique ont été déjà clôturées."})
            if new_dic in tabAutorisations:
                return JsonResponse({
                    "status": "error",
                    "message": "Cette autorisation de paiement existe déjà."}) 
            else:
                autorisation.salle_id = salle_id
                autorisation.student_id = student_id
                autorisation.month = month
                autorisation.justification = justification
                autorisation.user_id = user_id
                autorisation.save()
                return JsonResponse({
                    "status": "success",
                    "message": "Autorisation de paiement modifiée avec succès."})

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=permission_gestionnaire)
def del_autorisation_payment(request, id):
    anneeacademique_id = request.session.get('anneeacademique_id')
    setting = get_setting(anneeacademique_id)
    if setting is None:
        return redirect("settings/maintenance")
    
    try:
        authorisation = AutorisationPayment.objects.get(id=id)
    except:
        authorisation = None
        
    if authorisation:
        # Nombre d'autorisations avant la suppression
        count0 = AutorisationPayment.objects.all().count()
        authorisation.delete()
        # Nombre de d'autorisations après la suppression
        count1 = AutorisationPayment.objects.all().count()
        if count1 < count0: 
            messages.success(request, "Elément supprimé avec succès.")
        else:
            messages.error(request, "La suppression a échouée.")
        
        return redirect("autorisation/detail_autorisation_payments", authorisation.salle.id)

def ajax_delete_autorisation_student(request, id):
    autorisation = AutorisationPayment.objects.get(id=id)
    context = {
        "autorisation": autorisation
    }
    return render(request, "ajax_delete_autorisation_student.html", context)

# ====================================== Gestion d'autorisation de paiements d'une salle  
@login_required(login_url='connection/login')
@allowed_users(allowed_roles=permission_gestionnaire)
def autorisation_payments_salle(request):
    anneeacademique_id = request.session.get('anneeacademique_id')
    setting = get_setting(anneeacademique_id)
    if setting is None:
        return redirect("settings/maintenance")
    
    classe_id = request.session.get('classe_id')
    salles_authorisations = (AutorisationPaymentSalle.objects.values("salle_id")
                     .filter(anneeacademique_id=anneeacademique_id)
                     .annotate(nb_etudiants=Count("salle_id")))
    
    tabSalles = []
    for sp in salles_authorisations:        
        salle = Salle.objects.get(id=sp["salle_id"])               
        if salle.classe.id == classe_id:
            # Compter le nombre d'étudiants qui ne sont pas autorisés à payer
            nb_months = (AutorisationPaymentSalle.objects.values("month")
                                 .filter(anneeacademique_id=anneeacademique_id, salle_id=salle.id)
                                 .aggregate(Count('month'))['month__count'] or 0)        
            dic = {}
            dic["salle"] = salle
            dic["nb_months"] = nb_months
            dic["autorisations"] = AutorisationPaymentSalle.objects.filter(anneeacademique_id = anneeacademique_id, salle_id=salle.id)
            tabSalles.append(dic)

    anneeacademique = AnneeCademique.objects.get(id=anneeacademique_id) 
    context = {
        "setting": setting,
        "salles": tabSalles,
        "anneeacademique": anneeacademique
    }
    return render(request, "autorisation_paye_salle/autorisation_payments_salle.html", context)
    

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=permission_gestionnaire)
def add_autorisation_payment_salle(request):
    anneeacademique_id = request.session.get('anneeacademique_id')
    setting = get_setting(anneeacademique_id)
    if setting is None:
        return redirect("settings/maintenance")
    
    user_id = request.user.id
    classe_id = request.session.get('classe_id')
    if request.method == "POST":

        salle_id = request.POST["salle"]
        month = bleach.clean(request.POST["month"].strip())
        justification = bleach.clean(request.POST["justification"].strip())
        # Récuperer la délibération pour verifier si ses activités ont été cloturées ou pas
        anneescolaire = AnneeCademique.objects.filter(status_cloture=True, id=anneeacademique_id)  
        query = AutorisationPaymentSalle.objects.filter(salle_id=salle_id, anneeacademique_id=anneeacademique_id, month=month)        
        if anneescolaire.exists(): # Verifier si on a déjà cloturé les opérations de cette année
                return JsonResponse({
                    "status": "error",
                    "message": "Les opérations de cette année académique ont été déjà clôturées."})
        if query.exists():
            return JsonResponse({
                    "status": "error",
                    "message": "Cette autorisation de paiement de la salle existe déjà."})
        else:
            autorisation = AutorisationPaymentSalle(
                salle_id=salle_id,  
                user_id=user_id, 
                month=month, 
                justification=justification, 
                anneeacademique_id=anneeacademique_id)
            
            # Nombre d'autorisations avant l'ajout
            count0 = AutorisationPaymentSalle.objects.all().count()
            autorisation.save()
            # Nombre d'autorisations après l'ajout
            count1 = AutorisationPaymentSalle.objects.all().count()
            # On verifie si l'insertion a eu lieu ou pas.
            if count0 < count1:
                return JsonResponse({
                    "status": "success",
                    "message": "Autorisation de paiement de la salle enregistrée avec succès."})
            else:
                return JsonResponse({
                    "status": "error",
                    "message": "L'autorisation a échouée."})

    salles = Salle.objects.filter(classe_id=classe_id, anneeacademique_id=anneeacademique_id)
    months = periode_annee_scolaire(anneeacademique_id)
    context = {
        "setting": setting,
        "salles": salles,
        "months": months
    }
    return render(request, "autorisation_paye_salle/add_autorisation_payment_salle.html", context)

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=permission_gestionnaire)
def edit_autorisation_payment_salle(request, id):
    anneeacademique_id = request.session.get('anneeacademique_id')
    setting = get_setting(anneeacademique_id)
    if setting is None:
        return redirect("settings/maintenance")
    
    classe_id = request.session.get('classe_id')
    autorisation = AutorisationPaymentSalle.objects.get(id=id)
        
    salles = Salle.objects.filter(classe_id=classe_id, anneeacademique_id=anneeacademique_id).exclude(id=autorisation.salle.id)
    
    months = periode_annee_scolaire(anneeacademique_id)
    tabMonths = []
    for month in months:
        if month != months:
            tabMonths.append(month)

    context = {
        "setting": setting,
        "autorisation": autorisation,
        "salles": salles,
        "months": months
    }
    return render(request, "autorisation_paye_salle/edit_autorisation_payment_salle.html", context)


@login_required(login_url='connection/login')
@allowed_users(allowed_roles=permission_gestionnaire)
def edit_aps(request):
    anneeacademique_id = request.session.get('anneeacademique_id')
    user_id = request.user.id
    if request.method == "POST":
        id = int(request.POST["id"])
        try:
            autorisation = AutorisationPaymentSalle.objects.get(id=id)
        except:
            autorisation = None

        if autorisation is None:
            return JsonResponse({
                    "status": "error",
                    "message": "Identifiant inexistant."})
        else: 
            salle_id = request.POST["salle"]
            month = bleach.clean(request.POST["month"].strip())
            justification = bleach.clean(request.POST["justification"].strip())
             
            # Récuperer la délibération pour verifier si ses activités ont été cloturées ou pas
            anneescolaire = AnneeCademique.objects.filter(status_cloture=True, id=anneeacademique_id)    
            # Verifier l'existence du paiement
            autorisations = AutorisationPaymentSalle.objects.filter(anneeacademique_id=anneeacademique_id, salle_id=salle_id).exclude(id=id)
            tabAutorisations = []
            for p in autorisations:
                dic = {}
                dic["salle_id"] = p.salle.id
                dic["month"] = p.month 
                
                tabAutorisations.append(dic)
            
            new_dic = {}
            new_dic["salle_id"] = int(salle_id)
            new_dic["month"] = month 
            if anneescolaire.exists(): # Verifier si on a déjà cloturé les opérations de cette année
                return JsonResponse({
                    "status": "error",
                    "message": "Les opérations de cette année académique ont été déjà clôturées."})
            if new_dic in tabAutorisations:
                return JsonResponse({
                    "status": "error",
                    "message": "Cette autorisation de paiement de la salle existe déjà."}) 
            else:
                autorisation.salle_id = salle_id
                autorisation.month = month
                autorisation.justification = justification
                autorisation.user_id = user_id
                autorisation.save()
                return JsonResponse({
                    "status": "success",
                    "message": "Autorisation de paiement de la salle modifiée avec succès."})

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=permission_gestionnaire)
def del_autorisation_payment_salle(request,id):
    anneeacademique_id = request.session.get('anneeacademique_id')
    setting = get_setting(anneeacademique_id)
    if setting is None:
        return redirect("settings/maintenance")
    
    try:
        authorisation = AutorisationPaymentSalle.objects.get(id=id)
    except:
        authorisation = None
        
    if authorisation:
        # Nombre d'autorisations de paiements avant la suppression
        count0 = AutorisationPaymentSalle.objects.all().count()
        authorisation.delete()
        # Nombre d'autorisations de paiements après la suppression
        count1 = AutorisationPaymentSalle.objects.all().count()
        if count1 < count0: 
            messages.success(request, "ELément supprimé avec succès.")
        else:
            messages.error(request, "La suppression a échouée.")
    return redirect("autorisation_paye_salle/autorisation_payments_salle")

def ajax_delete_autorisation_salle(request, id):
    autorisation = AutorisationPaymentSalle.objects.get(id=id)
    context = {
        "autorisation": autorisation
    }
    return render(request, "ajax_delete_autorisation_salle.html", context)

class get_student_inscris_salle(View):
    def get(self, request, id, *args, **kwargs):
        anneeacademique_id = request.session.get('anneeacademique_id')
        inscriptions = Inscription.objects.filter(salle_id=id, anneeacademique_id=anneeacademique_id)
        students = []
        for inscription in inscriptions:
            students.append(inscription.student)
            
        context = {
            "students": students
        }
        return render(request, "ajax_student_inscris.html", context)
    
# ====================== Comptabilité ============================

# Compter le nombre d'élèves inscris dans une salle
def nombre_student_inscris(salle_id, anneeacademique_id):
    nb_inscriptions = Inscription.objects.filter(anneeacademique_id=anneeacademique_id, salle_id=salle_id).count()
    return nb_inscriptions

# Somme de paiement par mois
def summ_payment_month(anneeacademique_id, salle_id, month):
    somme_payment = (Payment.objects.filter(anneeacademique_id=anneeacademique_id, salle_id=salle_id, month=month)
                            .aggregate(Sum("amount"))["amount__sum"])
    if somme_payment:
        return somme_payment
    else:
        return ""
       
# Somme total de paiement par mois de toutes les salles 
def summ_total_payment_month_all_sall(anneeacademique_id, month):
    
    salles = Salle.objects.all()
    total = 0
    for salle in salles:
        somme = (Payment.objects.filter(anneeacademique_id=anneeacademique_id, salle_id=salle.id, month=month)
                                .aggregate(Sum('amount'))['amount__sum'] or 0)
        total = total + somme
    
    return total  

# Somme total que les étudiants doivent payer par mois dans chaque salle 
def summ_total_a_payer_month_all_sall(anneeacademique_id, month):
    
    salles = Salle.objects.all()
    total = 0
    for salle in salles:
        if AutorisationPaymentSalle.objects.filter(anneeacademique_id=anneeacademique_id, salle_id=salle.id, month=month).exists():
            continue
        else:
            total = total + salle.price * nombre_student_inscris(salle.id, anneeacademique_id)
    
    return total      
            
@login_required(login_url='connection/login') 
@allowed_users(allowed_roles=permission_gestionnaire)   
def comptabilite_payment(request):
    anneeacademique_id = request.session.get('anneeacademique_id')
    setting = get_setting(anneeacademique_id)
    if setting is None:
        return redirect("settings/maintenance")
    
    salles_payments = (Payment.objects.values("salle_id")
                           .filter(anneeacademique_id=anneeacademique_id)
                           .annotate(somme_frais=Sum("amount")))
    
    salles = []
    total = 0
    total_inscris = 0
    # Récuperer la période de l'année scolaire
    months = periode_annee_scolaire(anneeacademique_id)
    # Recuperer les mois aux quels les élèves ont payé allant du mois actuel au dernier mois de la période scolaire
    tab_month_payments = payment_month_actuel_dernier(anneeacademique_id)
    for si in salles_payments:
        total += si["somme_frais"] 
        salle = Salle.objects.get(id=si["salle_id"])
        dic = {}
        dic["salle"] = salle
        dic["somme_frais"] = si["somme_frais"]
        # Récuperer le nombre d'étudiant inscris dans une salle
        nb_student_inscris = nombre_student_inscris(si["salle_id"], anneeacademique_id)
        dic["nb_student_inscris"] = nb_student_inscris
        total_inscris += nb_student_inscris 
        total_amounts = []
        total_restant = 0 # Total restant dans une salle pendant plusieurs mois  
        for month in months:
            # Verifier si les étudiants sont autorisés à payer ce mois pour cette salle
            if AutorisationPaymentSalle.objects.filter(anneeacademique_id=anneeacademique_id, salle_id=salle.id, month=month).exists():
                dic_amount = {}
                dic_amount["total_mensuel"] = 0
                dic_amount["total_mensuel_restant"] = 0
                dic_amount["nb_student_paye"] = 0
                dic_amount["nb_student_no_paye"] = 0
                       
                total_amounts.append(dic_amount)
            else:
                if month not in tab_month_payments: # Verifier si ce mois ne vient pas après le mois actuel           
                    dic_amount = {}
                    # somme total de frais d'un mois
                    total_mensuel = summ_payment_month(anneeacademique_id, salle.id, month)
                    if total_mensuel:
                        dic_amount["total_mensuel"] = total_mensuel
                    else:
                        dic_amount["total_mensuel"] = 0
                    # Calculer le nombre d'étudiants qui ont payé
                    nb_student_paye = (Payment.objects.filter(anneeacademique_id=anneeacademique_id, salle_id=salle.id, month=month)
                                    .aggregate(Count("student_id"))["student_id__count"])
                    dic_amount["nb_student_paye"] = nb_student_paye
                    dic_amount["nb_student_no_paye"] = nb_student_inscris - nb_student_paye
                    # Calucler le montant restant des étudiant pour un mois
                    if total_mensuel:
                        total_mensuel_restant = float(salle.price * nb_student_inscris) - float(total_mensuel)
                        dic_amount["total_mensuel_restant"] = total_mensuel_restant
                        total_restant += total_mensuel_restant
                    else:
                        total_mensuel_restant = float(salle.price * nb_student_inscris)
                        dic_amount["total_mensuel_restant"] = total_mensuel_restant
                        total_restant += total_mensuel_restant
                        
                    total_amounts.append(dic_amount)
                else:
                    if Payment.objects.filter(month=month, anneeacademique_id=anneeacademique_id).exists():
                        dic_amount = {}
                        # somme total de frais d'un mois
                        total_mensuel = summ_payment_month(anneeacademique_id, salle.id, month)
                        if total_mensuel:
                            dic_amount["total_mensuel"] = total_mensuel
                        else:
                            dic_amount["total_mensuel"] = 0
                        # Calculer le nombre d'étudiants qui ont payé
                        nb_student_paye = (Payment.objects.filter(anneeacademique_id=anneeacademique_id, salle_id=salle.id, month=month)
                                        .aggregate(Count("student_id"))["student_id__count"])
                        dic_amount["nb_student_paye"] = nb_student_paye
                        dic_amount["nb_student_no_paye"] = nb_student_inscris - nb_student_paye
                        # Calucler le montant restant des étudiant pour un mois
                        if total_mensuel:
                            total_mensuel_restant = float(salle.price * nb_student_inscris) - float(total_mensuel)
                            dic_amount["total_mensuel_restant"] = total_mensuel_restant
                            total_restant += total_mensuel_restant
                        else:
                            total_mensuel_restant = float(salle.price * nb_student_inscris)
                            dic_amount["total_mensuel_restant"] = total_mensuel_restant
                            total_restant += total_mensuel_restant
                            
                        total_amounts.append(dic_amount)
                    else:
                        dic_amount = {}
                        dic_amount["total_mensuel"] = 0
                        dic_amount["total_mensuel_restant"] = 0
                        dic_amount["nb_student_paye"] = 0
                        dic_amount["nb_student_no_paye"] = 0
                        
                        total_amounts.append(dic_amount)
            
            
        dic["total_restant"] = float(total_restant)    
        dic["total_amounts"] = total_amounts   
        salles.append(dic)
    
    # Somme totale par mois de toutes les salles 
    sommes_totales = []   
    reste_total = 0
    for month in months:
        if month in tab_month_payments:
            if Payment.objects.filter(anneeacademique_id=anneeacademique_id, month=month).exists():
                    dic = {}
                    # Somme total que les étudiants ont payé par mois dans chaque salle
                    total_all_sall = summ_total_payment_month_all_sall(anneeacademique_id, month)
                    dic["total"] = total_all_sall
                    # Somme total que les étudiants doivent payer dans chaque salle
                    total_a_payer_all_sall =  summ_total_a_payer_month_all_sall(anneeacademique_id, month)
                    reste = float(total_a_payer_all_sall) - float(total_all_sall)
                    dic["total_restant"] = reste
                    
                    reste_total += reste
                    
                    sommes_totales.append(dic)
            else:
                dic = {}
                dic["total"] = 0
                dic["total_restant"] = 0
                sommes_totales.append(dic)
        else:
            
            dic = {}
            # Somme total que les étudiants ont payé par mois dans chaque salle
            total_all_sall = summ_total_payment_month_all_sall(anneeacademique_id, month)
            dic["total"] = total_all_sall
            # Somme total que les étudiants doivent payer dans chaque salle
            total_a_payer_all_sall =  summ_total_a_payer_month_all_sall(anneeacademique_id, month)
            reste = float(total_a_payer_all_sall) - float(total_all_sall)
            dic["total_restant"] = reste     
            
            reste_total += reste    
            sommes_totales.append(dic)
        
                
        
    context = {
        "setting": setting,
        "salles": salles,
        "total": total,
        "reste_total": reste_total,
        "sommes_totales": sommes_totales,
        "months": months,
        "total_inscris": total_inscris
    }
    return render(request, "comptabilite_payment.html", context=context)

@unauthenticated_customer
def dossier_financier(request):
    anneeacademique_id = request.session.get('anneeacademique_id')
    student_id = request.session.get('student_id')
    setting = get_setting(anneeacademique_id)
    if setting is None:
        return redirect("settings/maintenance")
    
    inscription = Inscription.objects.filter(anneeacademique_id=anneeacademique_id, student_id=student_id).first()
    payments = Payment.objects.filter(anneeacademique_id=anneeacademique_id, student_id=student_id).order_by("id")
    
    for payment in payments:
        # Mise à jour du statut pour marquer la lecture du paiement
        payment.status = True
        payment.save()
        
    # Récuperer tous les mois de l'année académique
    months = periode_annee_scolaire(anneeacademique_id)
    date_actuel = date.today() # date actuelle
    month_actuel = date_actuel.strftime("%m") # Mois actuel
    month_actuel = format_month(month_actuel)
    # Récuperer tous les mois du début de la rentrée jusqu'au mois actuel
    tabMonths = []
    for month in months:
        if month == month_actuel:
            tabMonths.append(month)
            break
        else:
            tabMonths.append(month)
            
    # Récuperer tous les paiements de l'étudiant du début de la rentrée jusqu'à ce jour
    tabMonthPaye = []
    montant_restant = 0
    for month in tabMonths:
        dic = {}
        dic["month"] = month
        # Verifier s'il est autoriser à payer ce mois ou pas
        autorisation = AutorisationPayment.objects.filter(salle_id=inscription.salle.id, student_id=student_id, month=month, anneeacademique_id=anneeacademique_id)
        # Verifier si les élèves de cette salles sont autorisés à payer ce mois
        query_autorisation_salle = AutorisationPayment.objects.filter(salle_id=inscription.salle.id, month=month, anneeacademique_id=anneeacademique_id)
        if autorisation.exists() or query_autorisation_salle.exists():
            dic["status"] = "Ne paye pas"
        else:
            payment = Payment.objects.filter(salle_id=inscription.salle.id, student_id=student_id, month=month, anneeacademique_id=anneeacademique_id)
            if payment.exists():
                paye = payment.first()
                if paye.amount < inscription.salle.price:
                    dic["status"] = "Avance"
                    montant_restant += (inscription.salle.price - paye.amount)
                else:
                    dic["status"] = "Payé"
            else:
                dic["status"] = "Impayé"
                montant_restant += inscription.salle.price
                
        tabMonthPaye.append(dic)
    
    context = {
        "setting": setting,
        "inscription": inscription,
        "payments": payments,
        "months": tabMonthPaye,
        "montant_restant": montant_restant
    }
    return render(request, "dossier_financier.html", context=context)

@unauthenticated_customer
def dossier_financier_parent(request):
    anneeacademique_id = request.session.get('anneeacademique_id')
    parent_id = request.session.get('parent_id')
    setting = get_setting(anneeacademique_id)
    if setting is None:
        return redirect("settings/maintenance")
    
    # Récuperer les enfants du parent
    students = Student.objects.filter(parent_id=parent_id) 
    # Selectionner les enfants du parent qui sont inscris cette année
    tabinscription = []
    for student in students:
        query = Inscription.objects.filter(anneeacademique_id=anneeacademique_id, student_id=student.id)
        if query.exists():
            # Récuperer l'inscription
            inscription = query.first()
            tabinscription.append(inscription)
    
    dette_totale = 0
    liste_payments = []
    for i in tabinscription:
        dic = {}
        inscription = Inscription.objects.filter(anneeacademique_id=anneeacademique_id, student_id=i.student.id).first()
        dic["inscription"] = inscription
        payments = Payment.objects.filter(anneeacademique_id=anneeacademique_id, student_id=i.student.id).order_by("id")
        dic["nombre_payes"] = payments.count()
        tabPayments = []
        i = 0
        for payment in payments:
            i += 1
            new_dic = {}
            new_dic["i"] = i
            new_dic["payment"] = payment
            
            tabPayments.append(new_dic)
            # Mise à jour du statut pour marquer la lecture du paiement
            payment.status_parent = True
            payment.save()
            
        dic["payments"] = tabPayments
        
        # Récuperer tous les mois de l'année académique
        months = periode_annee_scolaire(anneeacademique_id)
        date_actuel = date.today() # date actuelle
        month_actuel = date_actuel.strftime("%m") # Mois actuel
        month_actuel = format_month(month_actuel)
        # Récuperer tous les mois du début de la rentrée jusqu'au mois actuel
        tabMonths = []
        for month in months:
            if month == month_actuel:
                tabMonths.append(month)
                break
            else:
                tabMonths.append(month)
                
        # Récuperer tous les paiements de l'étudiant du début de la rentrée jusqu'à ce jour
        montant_restant = 0
        for month in tabMonths:
            # Verifier s'il est autoriser à payer ce mois ou pas
            autorisation = AutorisationPayment.objects.filter(salle_id=inscription.salle.id, student_id=inscription.student.id, month=month, anneeacademique_id=anneeacademique_id)
            # Verifier si les étudiants de cette salle ne sont pas autorisés à payer ce mois
            query_autorisation = AutorisationPaymentSalle.objects.filter(salle_id=inscription.salle.id, month=month, anneeacademique_id=anneeacademique_id)
            if autorisation.exists() or query_autorisation.exists():
                pass
            else:
                payment = Payment.objects.filter(salle_id=inscription.salle.id, student_id=inscription.student.id, month=month, anneeacademique_id=anneeacademique_id)
                if payment.exists():
                    paye = payment.first()
                    if paye.amount < inscription.salle.price:
                        montant_restant += (inscription.salle.price - paye.amount)
                else:
                    montant_restant += inscription.salle.price
            
        dic["montant_restant"] = montant_restant
        
        liste_payments.append(dic)
        
        dette_totale += montant_restant
    
    context = {
        "setting": setting,
        "inscription": inscription,
        "payments": liste_payments,
        "dette_totale": dette_totale
    }
    return render(request, "dossier_financier_parent.html", context)

def recu_paye(request, id):
    anneeacademique_id = request.session.get('anneeacademique_id')
    setting = get_setting(anneeacademique_id)
    paiement = Payment.objects.get(id=id)
    user = None
    users = User.objects.all()
    for user in users:
        if user.groups.exists():
            groups = user.groups.all()
            for group in groups:
                    if group.name in ["Gestionnaire"]:                       
                            user = user
                            
    anneeacademique  = AnneeCademique.objects.get(id=anneeacademique_id)
    
    # Chemin vers notre image
    image_path = setting.logo

    # Lire l'image en mode binaire et encoder en Base64
    base64_string = base64.b64encode(image_path.read()).decode('utf-8')
    # Date actuelle
    date_actuelle = date.today()
    
    context = {
        "user": user,
        "paiement": paiement,      
        "base64_image": base64_string, 
        "setting": setting,
        "anneeacademique": anneeacademique,
        "date_actuelle": date_actuelle
    }
    template = get_template("recu_paye.html")
    html = template.render(context)
    options = {
        'page-size': 'Letter',
        'encoding': "UTF-8",
    }
    pdf = pdfkit.from_string(html, False, options)
    reponse = HttpResponse(pdf, content_type='application/pdf')
    reponse['Content-Disposition'] = f"attachment; filename=Recu_{ paiement.student.lastname }_{ paiement.student.firstname }.pdf"
    return reponse 
        

def echeancier(request, student_id):
    anneeacademique_id = request.session.get('anneeacademique_id')
    setting = get_setting(anneeacademique_id)
    
    inscription = Inscription.objects.filter(student_id=student_id, anneeacademique_id=anneeacademique_id).first()
    anneeacademique  = AnneeCademique.objects.get(id=anneeacademique_id)
    
    # Chemin vers notre image
    image_path = setting.logo

    # Lire l'image en mode binaire et encoder en Base64
    base64_string = base64.b64encode(image_path.read()).decode('utf-8')
    # Date actuelle
    date_actuelle = date.today()
    
    paiements = Payment.objects.filter(student_id=student_id, anneeacademique_id=anneeacademique_id)
    
    montant_total = (Payment.objects.filter(student_id=student_id, anneeacademique_id=anneeacademique_id)
                     .aggregate(Sum("amount"))["amount__sum"]) or 0
    
    total = float(montant_total) + float(inscription.amount)
          
    context = {
        "paiements": paiements,
        "inscription": inscription,
        "base64_image": base64_string,
        "total": total,
        "setting": setting,
        "anneeacademique": anneeacademique,
        "date_actuelle": date_actuelle
    }
    template = get_template("echeancier.html")
    html = template.render(context)
    options = {
        'page-size': 'Letter',
        'encoding': "UTF-8",
    }
    pdf = pdfkit.from_string(html, False, options)
    reponse = HttpResponse(pdf, content_type='application/pdf')
    reponse['Content-Disposition'] = f"attachment; filename=Echeancier_{ inscription.student.lastname }_{ inscription.student.firstname }.pdf"
    return reponse

def status_paye_parent(request, student_id):
    anneeacademique_id = request.session.get('anneeacademique_id')
    setting = get_setting(anneeacademique_id)
    # Recuperer la salle
    inscription = Inscription.objects.filter(student_id=student_id, anneeacademique_id=anneeacademique_id).first()
    # Récuperer tous les mois de l'année académique
    months = periode_annee_scolaire(anneeacademique_id)
    date_actuel = date.today() # date actuelle
    month_actuel = date_actuel.strftime("%m") # Mois actuel
    month_actuel = format_month(month_actuel)
    # Récuperer tous les mois du début de la rentrée jusqu'au mois actuel
    tabMonths = []
    for month in months:
        if month == month_actuel:
            tabMonths.append(month)
            break
        else:
            tabMonths.append(month)
            
    # Récuperer tous les paiements de l'étudiant du début de la rentrée jusqu'à ce jour
    tabMonthPaye = []
    montant_restant = 0
    for month in tabMonths:
        dic = {}
        dic["month"] = month
        # Verifier s'il est autoriser à payer ce mois ou pas
        autorisation = AutorisationPayment.objects.filter(salle_id=inscription.salle.id, student_id=student_id, month=month, anneeacademique_id=anneeacademique_id)
        # Verifier si les élèves de cette salles sont autorisés à payer ce mois
        query_autorisation_salle = AutorisationPayment.objects.filter(salle_id=inscription.salle.id, month=month, anneeacademique_id=anneeacademique_id)
        if autorisation.exists() or query_autorisation_salle.exists():
            dic["status"] = "Ne paye pas"
        else:
            payment = Payment.objects.filter(salle_id=inscription.salle.id, student_id=student_id, month=month, anneeacademique_id=anneeacademique_id)
            if payment.exists():
                paye = payment.first()
                if paye.amount < inscription.salle.price:
                    dic["status"] = "Avance"
                    montant_restant += (inscription.salle.price - paye.amount)
                else:
                    dic["status"] = "Payé"
            else:
                dic["status"] = "Impayé"
                montant_restant += inscription.salle.price
                
        tabMonthPaye.append(dic)
        
    context = {
       "setting": setting,
       "months": tabMonthPaye,
       "montant_restant": montant_restant
    }
    return render(request, "status_paye_parent.html", context)

@login_required(login_url='connection/login') 
@allowed_users(allowed_roles=permission_gestionnaire)
def dette_parents(request):
    anneeacademique_id = request.session.get('anneeacademique_id')
    setting = get_setting(anneeacademique_id)
    if setting is None:
        return redirect("settings/maintenance")
    
    parents = Parent.objects.all()
    tabparents = []
    total = 0
    for parent in parents:
        dic_parent = {}
        # Récuperer les enfants du parent
        students = Student.objects.filter(parent_id=parent.id)
        tabstudents = [] # Liste des enfants du parent qui sont inscris cette année
        dette_totale = 0
        for student in students:
            query = Inscription.objects.filter(student_id=student.id, anneeacademique_id=anneeacademique_id)
            if query.exists():
                dic_student = {}
                
                inscription = query.first()
                # Récuperer tous les mois de l'année académique
                months = periode_annee_scolaire(anneeacademique_id)
                date_actuel = date.today() # date actuelle
                month_actuel = date_actuel.strftime("%m") # Mois actuel
                month_actuel = format_month(month_actuel)
                # Récuperer tous les mois du début de la rentrée jusqu'au mois actuel
                tabMonths = []
                for month in months:
                    if month == month_actuel:
                        tabMonths.append(month)
                        break
                    else:
                        tabMonths.append(month)
                        
                # Récuperer tous les paiements de l'étudiant du début de la rentrée jusqu'à ce jour
                montant_restant = 0
                for month in tabMonths:
                    # Verifier s'il est autoriser à payer ce mois ou pas
                    autorisation = AutorisationPayment.objects.filter(salle_id=inscription.salle.id, student_id=inscription.student.id, month=month, anneeacademique_id=anneeacademique_id)
                    # Verifier si les étudiants de cette salle ne sont pas autorisés à payer ce mois
                    query_autorisation = AutorisationPaymentSalle.objects.filter(salle_id=inscription.salle.id, month=month, anneeacademique_id=anneeacademique_id)
                    if autorisation.exists() or query_autorisation.exists():
                        pass
                    else:
                        payment = Payment.objects.filter(salle_id=inscription.salle.id, student_id=inscription.student.id, month=month, anneeacademique_id=anneeacademique_id)
                        if payment.exists():
                            paye = payment.first()
                            if paye.amount < inscription.salle.price:
                                montant_restant += (inscription.salle.price - paye.amount)
                        else:
                            montant_restant += inscription.salle.price
                            
                if montant_restant:
                    dic_student["student"] = student
                    dic_student["dette"] = montant_restant
                    
                    tabstudents.append(dic_student)
                     
                dette_totale += montant_restant
                
        if dette_totale:  
            dic_parent["parent"] = parent
            dic_parent["students"] = tabstudents
            dic_parent["nombre_enfants"] = len(tabstudents)
            dic_parent["dette"] = dette_totale
            
            date_actuel = date.today() # date actuelle
            month_actuel = date_actuel.strftime("%m") # Mois actuel
            month_actuel = format_month(month_actuel)
            if Notification.objects.filter(parent_id=parent.id, month=month_actuel, anneeacademique_id=anneeacademique_id).exists():
                dic_parent["status"] = True
            else:
                dic_parent["status"] = False
                
            tabparents.append(dic_parent)
            
            total += dette_totale 
            
        
    context = {
       "setting": setting,
       "parents": tabparents,
       "total": total
    }
    return render(request, "dette_parents.html", context)

@login_required(login_url='connection/login') 
@allowed_users(allowed_roles=permission_gestionnaire)
def add_notification(request, parent_id, montant):
    
    anneeacademique_id = request.session.get('anneeacademique_id')
    user_id = request.user.id
    date_actuel = date.today() # date actuelle
    month_actuel = date_actuel.strftime("%m") # Mois actuel
    month_actuel = format_month(month_actuel)
    mont = int(montant)
    notif = Notification(parent_id=parent_id, user_id=user_id, amount=mont, month=month_actuel, anneeacademique_id=anneeacademique_id)
    
    # Nombre de notifications avant l'ajout
    count0 = Notification.objects.all().count()
    notif.save()
    # Nombre de notifications après l'ajout
    count1 = Notification.objects.all().count()
    # On verifie si l'insertion a eu lieu ou pas.
    context = {}
    if count0 < count1:
        context = { "status": "success"}
    else:
        context = { "status": "error"}
    return render(request, "add_notification.html", context)

@unauthenticated_customer   
def notification_parent(request):
    anneeacademique_id = request.session.get('anneeacademique_id')
    parent_id = request.session.get('parent_id')
    setting = get_setting(anneeacademique_id)
    if setting is None:
        return redirect("settings/maintenance")
    
    notifications = Notification.objects.filter(parent_id=parent_id, anneeacademique_id=anneeacademique_id)
    for notification in notifications:
        notification.status = True
        notification.save()
        
    context = {
        "setting": setting,
        "notifications": notifications
    }
    return render(request, "notification_parent.html", context)