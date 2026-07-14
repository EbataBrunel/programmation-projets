# Importation des modules standards
import bleach
import os
# Importation des modules tiers
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models.functions import ExtractMonth
# Importation des modules locaux
from .models import ResumeJournanlier
from anneeacademique.models import AnneeCademique
from renumeration.models import Contrat
from school.views import get_setting
from school.methods import format_month2, format_month3
from app_auth.decorator import allowed_users
from scolarite.utils.crypto import dechiffrer_param

permission = ["Promoteur", "Directeur Général", "Directeur des Etudes", "Gestionnaire"]


@login_required(login_url='connection/account')
@allowed_users(allowed_roles=permission)
def resumes(request):
    anneeacademique_id = request.session.get('anneeacademique_id')
    setting = get_setting(anneeacademique_id)
    if setting is None:
        return redirect("settings/maintenance")
    
    anneeacademique = AnneeCademique.objects.get(id=anneeacademique_id)
    # Requête pour grouper par mois
    absences_par_mois = (
        ResumeJournanlier.objects
        .filter(user=request.user.id, anneeacademique=anneeacademique)
        .annotate(month=ExtractMonth('date_resume'))
        .values('month')
        .annotate(total=Count('id'))
        .order_by('month')
    )
    tabResumes = []
    for am in absences_par_mois:
        dic = {}
        month = format_month2(am["month"])
        dic["month"] = month
        
        resumes = ResumeJournanlier.objects.filter(
            user=request.user.id, 
            date_resume__month=am["month"], 
            anneeacademique=anneeacademique
        ).order_by("-id")
        
        dic["nombre_resumes"] = resumes.count()
        dic["resumes"] = resumes
        tabResumes.append(dic)
        
    anneeacademique = AnneeCademique.objects.get(id=anneeacademique_id) 
    context = {
        "setting": setting,
        "resumes": tabResumes,
        "anneeacademique": anneeacademique
    }
    return render(request, "resumes.html", context)
    
@login_required(login_url='connection/account')
@allowed_users(allowed_roles=permission)
def add_resume(request):
    anneeacademique_id = request.session.get('anneeacademique_id')
    setting = get_setting(anneeacademique_id)
    if setting is None:
        return redirect("settings/maintenance")
    
    if request.method == "POST":
        user_id = request.user.id
        
        content = bleach.clean(request.POST["content"].strip()) 
        date_resume = bleach.clean(request.POST["date"].strip())      
        anneescolaire = AnneeCademique.objects.filter(status_cloture=False, id=anneeacademique_id)    
        
        if anneescolaire.exists(): # Verifier si on a déjà cloturé les opérations de cette année
                return JsonResponse({
                    "status": "error",
                    "message": "Les opérations de cette année académique ont déjà été clôturées."}) 
        if ResumeJournanlier.objects.filter(anneeacademique_id=anneeacademique_id, date_resume=date_resume).exists():
                return JsonResponse({
                    "status": "success",
                    "message": "Ce résumé journalier existe déjà."})
        else:
            resume = ResumeJournanlier(
                    content=content,
                    user_id=user_id,
                    anneeacademique_id=anneeacademique_id,
                    date_resume=date_resume
            )
                
            count0 = ResumeJournanlier.objects.all().count()
            resume.save()
            count1 = ResumeJournanlier.objects.all().count()
            # Verifier si l'ajout a été bien effectué ou pas
            if count0 < count1:
                return JsonResponse({
                        "status": "success",
                        "message": "Résumé enregistré avec succès."})
            else:
                return JsonResponse({
                        "status": "error",
                        "message": "L'insertion a échouée."})
                
    # Récuperer l'année académique
    anneeacademique = AnneeCademique.objects.get(id=anneeacademique_id)
    contrat = Contrat.objects.filter(
        user=request.user, 
        type_contrat="Administrateur scolaire",
        anneeacademique=anneeacademique
    ).order_by("-id").first()
    
    context = {
        "setting": setting,
        "contrat": contrat
    }
    return render(request, "add_resume.html", context)
                
                
@login_required(login_url='connection/account')
@allowed_users(allowed_roles=permission)
def edit_resume(request,id):
    anneeacademique_id = request.session.get('anneeacademique_id')
    setting = get_setting(anneeacademique_id)
    if setting is None:
        return redirect("settings/maintenance")
    
    resume_id = int(dechiffrer_param(str(id)))
    resume = ResumeJournanlier.objects.get(id=resume_id)  
   
    # Récuperer l'année académique
    anneeacademique = AnneeCademique.objects.get(id=anneeacademique_id)
    contrat = Contrat.objects.filter(
        user=request.user, 
        type_contrat="Administrateur scolaire",
        anneeacademique=anneeacademique
    ).order_by("-id").first() 
                
    context = {
        "setting": setting,
        "resume": resume,
        "contrat": contrat
    }
    return render(request, "edit_resume.html", context)

@login_required(login_url='connection/account')
@allowed_users(allowed_roles=permission)
def edit_res(request):
   anneeacademique_id = request.session.get('anneeacademique_id') 
   if request.method == "POST":
        id = int(request.POST["id"])
        try:
            resume = ResumeJournanlier.objects.get(id=id)
        except:
            resume = None
        
        if resume:
            content = bleach.clean(request.POST["content"].strip())
            date_resume = bleach.clean(request.POST["date"].strip())
            # Récuperer la délibération pour verifier si ses activités ont été cloturées ou pas
            anneescolaire = AnneeCademique.objects.filter(status_cloture=False, id=anneeacademique_id)
            file = None
            if anneescolaire.exists(): # Verifier si on a déjà cloturé les opérations de cette année
                return JsonResponse({
                    "status": "error",
                    "message": "Les opérations de cette année académique ont déjà été clôturées."}) 
                
            if ResumeJournanlier.objects.filter(user_id=request.user.id, anneeacademique_id=anneeacademique_id, date_resume=date_resume).exclude(id=id).exists():
                return JsonResponse({
                    "status": "success",
                    "message": "Ce résumé journalier existe déjà."})
            else:
                resume.content = content
                resume.date_resume = date_resume

                resume.save()
                return JsonResponse({
                    "status": "success",
                    "message": "Résumé modifié avec succès."})

@login_required(login_url='connection/account')
@allowed_users(allowed_roles=permission)       
def del_resume(request,id):
    anneeacademique_id = request.session.get('anneeacademique_id')
    setting = get_setting(anneeacademique_id)
    if setting is None:
        return redirect("settings/maintenance")
    
    # Récuperer l'année académique
    anneeacademique = AnneeCademique.objects.get(id=anneeacademique_id)
    contrat = Contrat.objects.filter(user=request.user, anneeacademique=anneeacademique).first()
    if contrat and contrat.status_signature:
        resume_id = int(dechiffrer_param(str(id)))
        resume = ResumeJournanlier.objects.get(id=resume_id)
        # Nombre de résumés avant la suppression
        count0 = ResumeJournanlier.objects.all().count()
        resume.delete()
        # Nombre de résumés après la suppression
        count1 = ResumeJournanlier.objects.all().count()
        if count1 < count0: 
            messages.success(request, "Elément supprimé avec succès.")
        else:
            messages.error(request, "La suppression a échouée.")
        return redirect("resumes")
    else:
        messages.error(request, "Veuillez signer votre contrat avant de procéder à la suppression d’un programme.")
        return redirect("resumes")
    
def ajax_delete_resume(request, id):
    resume = ResumeJournanlier.objects.get(id=id)
    context = {
        "resume": resume
    }
    return render(request, "ajax_delete_resume.html", context)


@login_required(login_url='connection/account')
@allowed_users(allowed_roles=permission)
def resumes_su(request):
    anneeacademique_id = request.session.get('anneeacademique_id')
    setting = get_setting(anneeacademique_id)
    if setting is None:
        return redirect("settings/maintenance")
    
    anneeacademique = AnneeCademique.objects.get(id=anneeacademique_id)
    
    # Changement de statut de lecture
    for resume in ResumeJournanlier.objects.filter(anneeacademique=anneeacademique):
        resume.status = 1
        resume.save()
    
    tabResumes = []
    resume_users = (ResumeJournanlier.objects.filter(anneeacademique_id=anneeacademique_id)
                    .values("user_id")
                    .annotate(nombre_resumes=Count("user_id"))
    )
    for ru in resume_users:
        user = User.objects.get(id=ru["user_id"])
        dic = {}
        dic["user"] = user
        dic["nombre_resumes"] = ru["nombre_resumes"]
        # Requête pour grouper par mois
        absences_par_mois = (
            ResumeJournanlier.objects
            .filter(user=user, anneeacademique=anneeacademique)
            .annotate(month=ExtractMonth('date_resume'))
            .values('month')
            .annotate(total=Count('id'))
            .order_by('month')
        )
        tabMonths = []
        for am in absences_par_mois:
            dic_month = {}
            month = format_month2(am["month"])
            dic_month["month"] = month
            resumes = ResumeJournanlier.objects.filter(
                user=user, 
                date_resume__month=am["month"], 
                anneeacademique=anneeacademique
            ).order_by("-id")
            dic_month["nombre_resumes"] = resumes.count()
            dic_month["resumes"] = resumes
            tabMonths.append(dic_month)
            
        dic["months"] = tabMonths
        tabResumes.append(dic)
        
    anneeacademique = AnneeCademique.objects.get(id=anneeacademique_id) 
    context = {
        "setting": setting,
        "resumes": tabResumes,
        "anneeacademique": anneeacademique
    }
    return render(request, "resumes_su.html", context) 

def ajax_list_resume(request, month):
    anneeacademique_id = request.session.get('anneeacademique_id')
    # Récuperer l'année académique
    anneeacademique = AnneeCademique.objects.get(id=anneeacademique_id)
    m = format_month3(month)
    resumes = ResumeJournanlier.objects.filter(
            user=request.user.id, 
            date_resume__month=m, 
            anneeacademique=anneeacademique
    ).order_by("-id")
    
    context = {
        "month": month,
        "resumes": resumes,
        "anneeacademique": anneeacademique
    }
    return render(request, "ajax_list_resume.html", context) 


