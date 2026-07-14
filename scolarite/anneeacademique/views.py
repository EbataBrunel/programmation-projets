# Importation des modules standards
import bleach
# Importation des modules tiers
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
# Importation des modules locaux 
from .models import*
from school.views import get_setting
from app_auth.decorator import allowed_users
from school.models import Setting
from classe.models import Classe
from serie.models import Serie
from salle.models import Salle
from programme.models import Programme
from enseignement.models import Enseigner
from matiere.models import Matiere
from paiement.models import AutorisationPayment, AutorisationPaymentSalle, Payment
from calendrier.models import Trimestre
from inscription.models import Inscription
from composition.models import Composer, Deliberation
from absence.models import Absence, AbsenceAdmin
from renumeration.models import Contrat, Renumeration, RenumerationAdmin
from emargement.models import Emargement
from publication.models import Publication
from activity.models import Activity
from emploi_temps.models import EmploiTemps


permission_promoteur_DG = ['Promoteur', 'Directeur Général']

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=permission_promoteur_DG)
def anneeacademiques(request):
    anneeacademique_id = request.session.get('anneeacademique_id')
    setting = get_setting(anneeacademique_id)
    if setting is None:
        return redirect("settings/maintenance")
    
    anneeacademiques = AnneeCademique.objects.all().order_by("-id")
    context = {
        "setting":setting,
        "anneeacademiques":anneeacademiques
    }
    return render(request, "annee_academiques.html", context)

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=permission_promoteur_DG)
def add_anneeacademique(request):
    anneeacademique_id = request.session.get('anneeacademique_id')
    setting = get_setting(anneeacademique_id)
    if setting is None:
        return redirect("settings/maintenance")
    
    if request.method == "POST":
        annee_debut = bleach.clean(request.POST["annee_debut"].strip())
        annee_fin = bleach.clean(request.POST["annee_fin"].strip())
        separateur = request.POST["separateur"]
        start_date = bleach.clean(request.POST["start_date"].strip())
        end_date = bleach.clean(request.POST["end_date"].strip())
        # Difference entre les deux années
        diff_annee = int(annee_debut) - int(annee_fin)
        query = AnneeCademique.objects.filter(annee_debut=annee_debut, annee_fin=annee_fin)
        if query.exists():
            return JsonResponse({
                    "status": "error",
                    "message": "Cette année scolaire existe déjà."})
        elif diff_annee >= 0:
            return JsonResponse({
                    "status": "error",
                    "message": "L'année du début doit être supérieure à l'année de fin."})
        elif  diff_annee != -1:
            return JsonResponse({
                    "status": "error",
                    "message": "L'année de fin doit être supérieure à l'année de début de 1 an."})
        else:
            anneeacademique = AnneeCademique(
                annee_debut=annee_debut, 
                annee_fin=annee_fin, 
                separateur=separateur,
                start_date=start_date,
                end_date=end_date)
            # Nombre d'années académiques avant l'ajout
            count0 = AnneeCademique.objects.all().count()
            anneeacademique.save()
            # Nombre d'années académiques après l'ajout
            count1 = AnneeCademique.objects.all().count()
            # On verifie si l'insertion a eu lieu ou pas.
            if count0 < count1:
                # Enregister le paramètre de cette année scolaire
                setting = Setting.objects.all().order_by("-id").first()
                if setting:
                    sett = Setting(
                        appname = setting.appname,
                        appeditor = setting.appeditor,
                        version = setting.version,
                        theme = setting.theme,
                        text_color = setting.text_color,
                        devise = setting.devise,
                        address = setting.address,
                        email = setting.email,
                        phone = setting.phone,
                        logo = setting.logo,
                        width_logo = setting.width_logo,
                        height_logo = setting.height_logo,
                        anneeacademique_id =  anneeacademique.id
                    )
                    # Nombre de paramètre avant l'ajout
                    count2 = Setting.objects.all().count()
                    sett.save()  
                    # Nombre de paramètre après l'ajout
                    count3 = Setting.objects.all().count()
                    # On verifie si l'insertion a eu lieu ou pas. 
                    if count2 < count3:              
                        return JsonResponse({
                            "status": "success",
                            "message": "Année scolaire et paramètre enregistrées avec succès."})
                    else:
                        return JsonResponse({
                            "status": "error",
                            "message": "L'insertion a échouée."})
                else:
                    return JsonResponse({
                        "status": "success",
                        "message": "Année scolaire enregistrée avec succès."})
            else:
                return JsonResponse({
                    "status": "error",
                    "message": "L'insertion a échouée."}) 
            
    context = {
        "setting": setting,
    }
    return render(request, "add_anneeacademique.html", context)

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=permission_promoteur_DG)
def edit_anneeacademique(request,id):
    anneeacademique_id = request.session.get('anneeacademique_id')
    setting = get_setting(anneeacademique_id)
    if setting is None:
        return redirect("settings/maintenance")
    
    anneeacademique = AnneeCademique.objects.get(id=id)
    context = {
        "setting": setting,
        "anneeacademique": anneeacademique
    }
    return render(request, "edit_anneeacademique.html", context)

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=permission_promoteur_DG)
def edit_anneeac(request):    
    if request.method == "POST":
        id = int(request.POST["id"])
        try:
            anneeacademique = AnneeCademique.objects.get(id=id)
        except:
            anneeacademique = None

        if anneeacademique is None:
            return JsonResponse({
                    "status": "error",
                    "message": "Identifiant inexistant."})
        else:
            annee_debut = bleach.clean(request.POST["annee_debut"].strip())
            annee_fin = bleach.clean(request.POST["annee_fin"].strip())
            separateur = request.POST["separateur"]
            start_date = bleach.clean(request.POST["start_date"].strip())
            end_date = bleach.clean(request.POST["end_date"].strip())
            # Difference entre les deux années
            diff_annee = int(annee_debut) - int(annee_fin)
            
            #On verifie si cette année a déjà été enregistrée
            anneeacademiques = AnneeCademique.objects.exclude(id=id)
            tabAnneeAcademique = []
            for annee in anneeacademiques:   
                dic = {}  
                dic["annee_debut"] = annee.annee_debut
                dic["annee_fin"] = annee.annee_fin
                tabAnneeAcademique.append(dic)
                
            #On verifie si cette année existe déjà
            new_dic = {}
            new_dic["annee_debut"] = int(annee_debut)
            new_dic["annee_fin"] = int(annee_fin)
            
            if new_dic in tabAnneeAcademique:
                return JsonResponse({
                    "status": "error",
                    "message": "Cette année scolaire existe déjà."})
            
            if  diff_annee >= 0:
                return JsonResponse({
                    "status": "error",
                    "message": "L'année du début doit être supérieure à la date de fin."})
            elif  diff_annee != -1:
                return JsonResponse({
                    "status": "error",
                    "message": "L'année de fin doit être supérieure à l'année de début de 1 an."})
            else:
                anneeacademique.annee_debut = annee_debut
                anneeacademique.annee_fin = annee_fin
                anneeacademique.separateur = separateur
                anneeacademique.start_date = start_date
                anneeacademique.end_date = end_date
                anneeacademique.save()
                return JsonResponse({
                    "status": "success",
                    "message": "Année scolaire modifiée avec succès."})
                
@login_required(login_url='connection/login')
@allowed_users(allowed_roles=permission_promoteur_DG)
def delete_anneeacademique(request,id):
    anneeacademique_id = request.session.get('anneeacademique_id')
    setting = get_setting(anneeacademique_id)
    if setting is None:
        return redirect("settings/maintenance")
    
    anneeacademique = AnneeCademique.objects.get(id=id)
    nombre = {}
    nombre["nombre_classes"] = Classe.objects.filter(anneeacademique_id=anneeacademique.id).count()
    nombre["nombre_series"] = Serie.objects.filter(anneeacademique_id=anneeacademique.id).count()
    nombre["nombre_salles"] = Salle.objects.filter(anneeacademique_id=anneeacademique.id).count()
    nombre["nombre_programmes"] = Programme.objects.filter(anneeacademique_id=anneeacademique.id).count()
    nombre["nombre_matieres"] = Matiere.objects.filter(anneeacademique_id=anneeacademique.id).count()
    nombre["nombre_enseignements"] = Enseigner.objects.filter(anneeacademique_id=anneeacademique.id).count()
    nombre["nombre_calendriers"] = Trimestre.objects.filter(anneeacademique_id=anneeacademique.id).count()
    nombre["nombre_autorisation_payements_students"] = AutorisationPayment.objects.filter(anneeacademique_id=anneeacademique.id).count()
    nombre["nombre_autorisation_payements_salles"] = AutorisationPaymentSalle.objects.filter(anneeacademique_id=anneeacademique.id).count()
    nombre["nombre_payments"] = Payment.objects.filter(anneeacademique_id=anneeacademique.id).count()
    nombre["nombre_inscriptions"] = Inscription.objects.filter(anneeacademique_id=anneeacademique.id).count()
    nombre["nombre_contrats"] = Contrat.objects.filter(anneeacademique_id=anneeacademique.id).count()
    nombre["nombre_renumerations_enseignants"] = Renumeration.objects.filter(anneeacademique_id=anneeacademique.id).count()
    nombre["nombre_renumerations_admin"] = RenumerationAdmin.objects.filter(anneeacademique_id=anneeacademique.id).count()
    nombre["nombre_absences_enseignants"] = Absence.objects.filter(anneeacademique_id=anneeacademique.id).count()
    nombre["nombre_absences_personnels"] = AbsenceAdmin.objects.filter(anneeacademique_id=anneeacademique.id).count()
    nombre["nombre_emargements"] = Emargement.objects.filter(anneeacademique_id=anneeacademique.id).count()
    nombre["nombre_publications"] = Publication.objects.filter(anneeacademique_id=anneeacademique.id).count()
    nombre["nombre_activites"] = Activity.objects.filter(anneeacademique_id=anneeacademique.id).count()
    nombre["nombre_emploitemps"] = EmploiTemps.objects.filter(anneeacademique_id=anneeacademique.id).count()
    nombre["nombre_compositions"] = Composer.objects.filter(anneeacademique_id=anneeacademique.id).count()
    nombre["nombre_deliberations"] = Deliberation.objects.filter(anneeacademique_id=anneeacademique.id).count()
    nombre["nombre_settings"] = Setting.objects.filter(anneeacademique_id=anneeacademique.id).count()
    
    nombre_total = 0
    for valeur in nombre.values():
        if valeur != 0:
            nombre_total += valeur
            
    context = {
        "setting": setting,
        "anneeacademique": anneeacademique,
        "nombre_total": nombre_total,
        "nombre": nombre
    }
    return render(request, "delete_anneeacademique.html", context)

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=permission_promoteur_DG)
def del_anneeacademique(request,id):
    try:
        anneeacademique = AnneeCademique.objects.get(id=id)
    except:
        anneeacademique = None
    
    if anneeacademique :
        # Nombre d'années académiques avant la suppression
        count0 = AnneeCademique.objects.all().count()
        anneeacademique.delete()
        # Nombre d'années académiques après la suppression
        count1 = AnneeCademique.objects.all().count()
        if count1 < count0: 
            messages.success(request, "Elément supprimé avec succès.")
        else:
            messages.error(request, "La suppression a échouée.")
        
    return redirect("annee_academiques")

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=permission_promoteur_DG)
def cloture_anneeacademique(request, id):
    anneeacademique_id = request.session.get('anneeacademique_id')
    setting = get_setting(anneeacademique_id)
    if setting is None:
        return redirect("settings/maintenance")
    anneeacademique = AnneeCademique.objects.get(id=id)

    context = {
        "setting": setting,
        "anneeacademique": anneeacademique
    }
    return render(request, "cloture_anneeacademique.html", context)


def clot_anneeacademique(request):
    if request.method == "POST":
        id = int(request.POST["id"])
        try:
            anneeacademique = AnneeCademique.objects.get(id=id)
        except:
            anneeacademique = None
        
        if anneeacademique is None:
            return JsonResponse({
                        "status": "error",
                        "message": "Identifiant inexistant."})
        else: 
            password = bleach.clean(request.POST["password"].strip())
            user = User.objects.get(id=request.user.id)
            if user.check_password(password):
                anneeacademique.status_cloture = True
                anneeacademique.save()
                
                return JsonResponse({
                            "status": "success",
                            "status_cloture": anneeacademique.status_cloture,
                            "message": "Année académique cloturée avec succès."})
            else:
                return JsonResponse({
                            "status": "error",
                            "message": "Mot de passe incorrect."})
                