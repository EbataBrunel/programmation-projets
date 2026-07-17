# Imporation des modules standards
import datetime
import bleach
# Importation des modules tiers
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
# Importation des modules locaux
from eab.views import nbnew_answer, nbnew_message, new_message, parametre
from app_auth.decorator import*
from document.views import userPriority
from .models import*
from .forms import*
from eajc.utils.crypto import dechiffrer_param

def date_actuelle():
    date = datetime.datetime.now()
    return date

def annonces(request):
        
    annonces = Annonce.objects.all().order_by("-id")
    context = {
        "annonces":annonces,
        "parametre":parametre(),
        "date":date_actuelle(),
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request),
    }
    return render(request, "annonce/annonces.html", context)

def mes_annonce(request):
    
    annonces = Annonce.objects.filter(user_id=request.user.id).order_by("-id")
    context = {
        "annonces":annonces,
        "parametre":parametre(),
        "date":date_actuelle(),
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request),
    }
    return render(request, "annonce/mes-annonce.html", context)

def ajax_detail_annonce(request, id):
    annonce = Annonce.objects.get(id=id)
    context = {
        "annonce": annonce
    }
    return render(request, "ajax_detail_annonce.html", context)

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=['admin'])
@csrf_exempt
def add_annonce(request):
    if request.method == "POST":
        form = AnnonceForm(request.POST)
        if form.is_valid():
            title = bleach.clean(request.POST["title"].strip())
            company = bleach.clean(request.POST["company"].strip())
            content = request.POST["content"]
            
            annonce = Annonce(title=title,company=company,content=content,user_id=request.user.id)
            count0 = Annonce.objects.all().count()
            annonce.save()
            count1 = Annonce.objects.all().count()
            if count0 < count1:
                messages.success(request, "Annonce publiée avec succès.")
                return redirect("annonce/mes-annonce")
            else:
                messages.error(request, "Insertion a echouée.")
        else:
            messages.error(request, "Problème de formulaire.")
    form = AnnonceForm()       
    context = {
        "form":form,
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request),
        "parametre":parametre(),
        "date":date_actuelle()
    }
    return render(request, "annonce/add-annonce.html", context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def edit_annonce(request, id):
    annonce_id = dechiffrer_param(str(id))
    annonce = Annonce.objects.get(id=annonce_id)
    #Verifier si ce membre est authorisé à acceder à cette page ou pas.
    query = Annonce.objects.filter(id=annonce_id,user_id=request.user.id)
    if query.exists():
        if request.method == "POST":
            form = AnnonceForm(request.POST)
            if form.is_valid():
                try:
                    annonce = Annonce.objects.get(id=annonce_id)
                except:
                    annonce = None

                if annonce == None:
                    messages.error(request, "Identifiant inexistant.")
                else:
                    title = bleach.clean(request.POST["title"].strip())
                    company = bleach.clean(request.POST["company"].strip())
                    content = request.POST["content"]
                    
                    annonce.title = title
                    annonce.company = company
                    annonce.content = content
                    annonce.save()
                    messages.success(request, "Annonce modifiée avec succès.")
            else:
                messages.error(request, "Problème de formulaire.")
    else:
        return redirect("authorization")
    form = AnnonceForm()
    context = {
        "form":form,
        "annonce":annonce,
        "parametre":parametre(),
        "date":date_actuelle(),
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request)
    }
    return render(request, "annonce/edit-annonce.html", context)

def ajax_delete_annonce(request, id):
    annonce = Annonce.objects.get(id=id)
    context = {
        "annonce": annonce
    }
    return render(request, "ajax_delete_annonce.html", context)

def del_annonce(request, id):
    try:
        annonce_id = dechiffrer_param(str(id))
        annonce = Annonce.objects.get(id=annonce_id)
    except:
        annonce = None
        
    if annonce:
        annonce.delete()
    return redirect("annonce/annonces")

def ajax_delete_my_ad(request, id):
    annonce = Annonce.objects.get(id=id)
    context = {
        "annonce": annonce
    }
    return render(request, "ajax_delete_my_ad.html", context)

def delete_my_ad(request, id):
    try:
        annonce_id = dechiffrer_param(str(id))
        annonce = Annonce.objects.get(id=annonce_id)
    except:
        annonce = None
        
    if annonce:
        annonce.delete()
    return redirect("annonce/mes-annonce")

def delete_annonce(request, id):
    try:
        annonce_id = dechiffrer_param(str(id))
        annonce = Annonce.objects.get(id=annonce_id)
    except:
        annonce = None
        
    if annonce:
        annonce.delete()
    return redirect("annonce/annonce")

def annonce(request):

    annonces = Annonce.objects.filter(visibility=1).order_by("-id")

    paginator = Paginator(annonces, 12)
    num_page = request.GET.get('page')
    annonces = paginator.get_page(num_page)
    
    context = {
        "annonces":annonces,
        "userpriorities":userPriority(),
        "parametre":parametre(),
    }
    return render(request, "annonce/annonce.html", context)

def ajax_visibilite_annonce(request, id):
    annonce = Annonce.objects.get(id=id)
    context = {
        "annonce": annonce
    }
    return render(request, "ajax_visibilite_annonce.html", context)

def visibilite(request,id):
    annonce = Annonce.objects.get(id=id)
    if annonce.visibility == 1:
        annonce.visibility = 0
        annonce.save()
        return JsonResponse({'status':0})
    else:
        annonce.visibility = 1
        annonce.save()
        return JsonResponse({'status':1})

