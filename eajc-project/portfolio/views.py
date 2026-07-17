# Importation des modules standard
from datetime import datetime
import bleach
import re
import hashlib
import os
# Importation des modules tiers
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from django.contrib.sites.shortcuts import get_current_site
# Imporation des modules locaux
from eab.views import nbnew_answer, nbnew_message, new_message, parametre
from eab.utils import send_email_with_html_body
from .models import*
from .forms import ContactPortfolioForm
from eajc.utils.crypto import dechiffrer_param

def get_file_hash(file):
    hash_md5 = hashlib.md5() # Cette objet de MD5 servira de stocker et calculer l'empreinte MD5.
    for chunk in file.chunks(): # Parcourir le fichier par morceau pour ne pas surcherger la memoire
        hash_md5.update(chunk) # Ajout de chaque morceau au calcul de hash et en mettant en même à jour le hash
    return hash_md5.hexdigest() # retourner l'empreinte MD5 sous forme de chaîne hexadécimale


@login_required(login_url='connection/login')
@csrf_exempt
def portfolio(request):
    date = datetime.now()
    user_id = request.user.id
    
    user = User.objects.get(id=user_id)
    
    user_split = re.split(r'[ -]', user.last_name)
    f_name = user_split[0].lower()
    
    param = f_name+"-"+str(user_id)
    
    nb_projects = Project.objects.filter(user_id=user_id).count()
    nb_theses = These.objects.filter(auteur_id=user_id).count()
    nb_articles = Article.objects.filter(auteur_id=user_id).count()
    
    nb_totals = nb_projects + nb_theses + nb_articles
    
    context = {       
        "nb_projects": nb_projects,  
        "nb_articles": nb_articles,  
        "nb_theses": nb_theses,   
        "nb_totals": nb_totals,
        "param": param,
        "domain":get_current_site(request).domain,
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request),
        "parametre":parametre(),
        "date":date
    }
    return render(request, 'portfolio.html', context)

@login_required(login_url='connection/login')
@csrf_exempt
def list_portfolio(request):
    date = datetime.now()
    
    users = User.objects.all()
    tabUsers = []
    for user in users:
        nb_projects = Project.objects.filter(user_id=user.id).count()
        nb_theses = These.objects.filter(auteur_id=user.id).count()
        nb_ptf = nb_projects + nb_theses
        if nb_ptf > 0:
            tabUsers.append(user)
    
    list_users = []
    for us in tabUsers:
        dic = {}
        dic["user"] = us
        
        user_split = re.split(r'[ -]', us.last_name)
        f_name = user_split[0].lower()
    
        param = f_name+"-"+str(us.id)
        dic["param"] = param
        
        list_users.append(dic)
        
    context = {       
        "list_users": list_users,
        "domain":get_current_site(request).domain,
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request),
        "parametre":parametre(),
        "date":date
    }
    return render(request, 'list_portfolio.html', context)

def mon_portfolio(request, param):
    
    user_id = param.split("-")[1]
    
    user = User.objects.get(id=user_id)
    projects = Project.objects.filter(user_id=user_id)
    
    these_articles = (Article.objects.values("these_id")
                       .filter(auteur_id=user_id)
                       .annotate(nb_article=Count("these_id")))
    tabThese = []
    n = 0
    for ta in these_articles:
        n += 1
        dic = {}
        these = These.objects.get(id=ta["these_id"])
        dic["n"] = n
        dic["these"] = these   
        articles = Article.objects.filter(these_id=ta["these_id"])
        dic["articles"] = articles
        dic["nb_articles"] = articles.count()
        tabThese.append(dic)
        
    articles = Article.objects.filter(auteur_id=user_id)
    
    form = ContactPortfolioForm()
    context = {
        "form": form,
        "user": user,
        "projects": projects,
        "articles": articles,
        "theses": tabThese,
        "parametre":parametre(),
    }
    return render(request, 'mon_portfolio.html', context)

def contact_portfolio(request):
    
    if request.method == "POST":     
        form = ContactPortfolioForm(request.POST)
        if form.is_valid():
            user_id = request.POST["user_id"]
            name = bleach.clean(form.cleaned_data["name"])
            email = form.cleaned_data["email"]
            message = bleach.clean(form.cleaned_data["message"])
            #On verifie si l'adresse e-mail correspond bien
            regexp = r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$"
            if not re.search(regexp, email):
                return JsonResponse({'status':0})
            else:
                contact = ContactPortfolio(name=name, email=email, message=message, user_id=user_id)
                count0 = ContactPortfolio.objects.all().count()
                contact.save()
                count1 = ContactPortfolio.objects.all().count()

                subject = "Confirmation"
                template = "email/emailcontactportfolio.html"
                receivers = [email]
                
                context = {
                    'email':email,
                    'user': User.objects.get(id=user_id),
                    'date': datetime.now(),
                    'parametre': parametre()
                }
                has_send = send_email_with_html_body(
                    subjet=subject,
                    receivers=receivers,
                    template=template,
                    context=context
                )
                #On verifie si le message a bien été envoyé
                if count0 < count1 and has_send == True:
                    return JsonResponse({'status':'Save'})
                else:
                    return JsonResponse({'status':1})
        else:
            form = ContactPortfolioForm()
            

@login_required(login_url='connection/login')
@csrf_exempt
def projects(request):
    date = datetime.now()
    user_id = request.user.id
    
    projects = Project.objects.filter(user_id=user_id)
    context = {
        "projects": projects,
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request),
        "parametre":parametre(),
        "date":date
    }
    return render(request, 'projet/projects.html', context)


@login_required(login_url='connection/login')
@csrf_exempt
def add_project(request):
    date = datetime.now()
    user_id = request.user.id
    
    if request.method == "POST":
        title = bleach.clean(request.POST["title"].strip())
        description = bleach.clean(request.POST["description"].strip())
        link = bleach.clean(request.POST["link"].strip())

        query = Project.objects.filter(title=title, user_id=user_id)
        if query.exists():
            return JsonResponse({
                "status": "error",
                "message": "Ce projet existe déjà."})
        else:
            project = Project(title=title, description=description, link=link, user_id=user_id)
            # Nombre de projets avant l'ajout
            count0 = Project.objects.all().count()
            project.save()
            # Nombre de projets après l'ajout
            count1 = Project.objects.all().count()
            # On verifie si l'insertion a eu lieu ou pas.
            if count0 < count1:
                return JsonResponse({
                    "status": "success",
                    "message": "Projet enregistré avec succès."})
            else:
               return JsonResponse({
                    "status": "error",
                    "message": "L'insertion a échouée."})

    context = {
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request),
        "parametre":parametre(),
        "date":date
    }
    return render(request, "projet/add_project.html", context)

@login_required(login_url='connection/login')
def edit_project(request,id):
    date = datetime.now()
    project_id = dechiffrer_param(str(id))
    project = Project.objects.get(id=project_id)
    #On vérifie si ce membre est authorisé à acceder à cette page ou pas.
    query = Project.objects.filter(id=project_id, user_id=request.user.id)
    if query.exists():
        context = {
            "project": project,
            "countanswer": nbnew_answer(request),
            "count": nbnew_message(request),
            "users": new_message(request),
            "parametre": parametre(),
            "date": date
        }
        return render(request, "projet/edit_project.html", context)
    else:
        return redirect("authorization")

@login_required(login_url='connection/login')
@csrf_exempt
def edit_proj(request):
    if request.method == "POST":
        id = int(request.POST["id"])
        try:
            project = Project.objects.get(id=id)
        except:
            project = None
        
        if project is None:
            return JsonResponse({
                "status": "error",
                "message": "L'identifiant inexistant."})
        else:
            # Se proteger de l'attaque XSS(Injection du code javascript)
            title = bleach.clean(request.POST["title"].strip())
            description = bleach.clean(request.POST["description"].strip())
            link = bleach.clean(request.POST["link"].strip())
            #On exclut le projet que l'on veut modifier
            projects = Project.objects.exclude(id=id)
            tabProjets = []
            for proj in projects:
                try:
                    if project.user.id == request.user.id:
                        tabProjets.append(proj.title)
                except Exception as e:
                    pass
            #On verifie si ce projet existe déjà
            if title in tabProjets:
                return JsonResponse({
                "status": "error",
                "message": "Ce projet existe déjà."})
            else:
                project.title = title
                project.description = description
                project.link = link
                project.save()
                return JsonResponse({
                    "status": "success",
                    "message": "Projet modifié avec succès."})


@login_required(login_url='connection/login')
def del_project(request,id):
    try:    
        project_id = dechiffrer_param(str(id))
        project = Project.objects.get(id=project_id)
    except:
        project = None
        
    if project:
        project.delete()
    return redirect("projet/projects")

#========================== Gestion de la thèse ============================
@login_required(login_url='connection/login')
@csrf_exempt
def theses(request):
    date = datetime.now()
    user_id = request.user.id
    
    theses = These.objects.filter(auteur_id=user_id)
    context = {
        "theses": theses,
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request),
        "parametre":parametre(),
        "date":date
    }
    return render(request, 'these/theses.html', context)


@login_required(login_url='connection/login')
@csrf_exempt
def add_these(request):
    date = datetime.now()
    user_id = request.user.id
    
    if request.method == "POST":
        titre = bleach.clean(request.POST["titre"].strip())
        resume = bleach.clean(request.POST["resume"].strip())
        universite = bleach.clean(request.POST["universite"].strip())
        date_soutenance = bleach.clean(request.POST["date_soutenance"].strip())

        query = These.objects.filter(titre=titre, auteur_id=user_id)
        if query.exists():
            return JsonResponse({
                "status": "error",
                "message": "Cette thèse existe déjà."})
        else:
            these = These(
                titre=titre, 
                resume=resume, 
                universite=universite, 
                date_soutenance=date_soutenance,
                auteur_id=user_id
            )
            # Nombre de thèse avant l'ajout
            count0 = These.objects.all().count()
            these.save()
            # Nombre de thèses après l'ajout
            count1 = These.objects.all().count()
            # On verifie si l'insertion a eu lieu ou pas.
            if count0 < count1:
                return JsonResponse({
                    "status": "success",
                    "message": "Thèse enregistrée avec succès."})
            else:
               return JsonResponse({
                    "status": "error",
                    "message": "L'insertion a échouée."})

    context = {
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request),
        "parametre":parametre(),
        "date":date
    }
    return render(request, "these/add_these.html", context)

@login_required(login_url='connection/login')
def edit_these(request, id):
    date = datetime.now()
    these_id = dechiffrer_param(str(id))
    these = These.objects.get(id=these_id)
    #On vérifie si ce membre est authorisé à acceder à cette page ou pas.
    query = These.objects.filter(id=these_id, auteur_id=request.user.id)
    if query.exists():
        context = {
            "these": these,
            "countanswer": nbnew_answer(request),
            "count": nbnew_message(request),
            "users": new_message(request),
            "parametre": parametre(),
            "date": date
        }
        return render(request, "these/edit_these.html", context)
    else:
        return redirect("authorization")

@login_required(login_url='connection/login')
@csrf_exempt
def edit_th(request):
    if request.method == "POST":
        id = int(request.POST["id"])
        try:
            these = These.objects.get(id=id)
        except:
            these = None
        
        if these is None:
            return JsonResponse({
                "status": "error",
                "message": "Identifiant inexistant."})
        else:
            # Se proteger de l'attaque XSS(Injection du code javascript)
            titre = bleach.clean(request.POST["titre"].strip())
            resume = bleach.clean(request.POST["resume"].strip())
            universite = bleach.clean(request.POST["universite"].strip())
            date_soutenance = bleach.clean(request.POST["date_soutenance"].strip())
            #On exclut le projet que l'on veut modifier
            theses = These.objects.exclude(id=id)
            tabTheses = []
            for th in theses:
                try:
                    if th.auteur.id == request.user.id:
                        tabTheses.append(th.titre)
                except Exception as e:
                    pass
            #On verifie si ce projet existe déjà
            if titre in tabTheses:
                return JsonResponse({
                    "status": "error",
                    "message": "Cette thèse existe déjà."})
            else:
                these.titre = titre
                these.resume = resume
                these.universite = universite
                these.date_soutenance = date_soutenance
                these.save()
                return JsonResponse({
                    "status": "success",
                    "message": "Thèse modifiée avec succès."})


@login_required(login_url='connection/login')
def del_these(request, id):
    try:  
        these_id = dechiffrer_param(str(id))  
        these = These.objects.get(id=these_id)
    except:
        these = None
        
    if these:
        these.delete()
    return redirect("these/theses")


#========================== Gestion de l'article ============================
@login_required(login_url='connection/login')
def these_article(request):
    date = datetime.now()

    theses_articles = (Article.objects.values("these_id")
                   .filter(auteur_id=request.user.id)
                   .annotate(nb_articles=Count("these_id")))
    tabTheses = []
    for ta in theses_articles:
        dic = {}
        these = Article.objects.get(id=ta["these_id"])
        dic["these"] = these
        dic["nb_articles"] = ta["nb_articles"]
        tabTheses.append(dic)

    context = {
        "theses":tabTheses,
        "countanswer": nbnew_answer(request),
        "count": nbnew_message(request),
        "users": new_message(request),
        "parametre": parametre(),
        "date": date
    }
    return render(request, "article/these_article.html", context)

@login_required(login_url='connection/login')
def articles(request, id):
    date = datetime.now()
    these_id = dechiffrer_param(str(id))
    these = These.objects.get(id=these_id)
    
    articles = Article.objects.filter(auteur_id=request.user.id, these_id=these_id)
    context = {
        "these": these,
        "articles": articles,
        "countanswer": nbnew_answer(request),
        "count": nbnew_message(request),
        "users": new_message(request),
        "parametre": parametre(),
        "date": date
    }
    return render(request, 'article/articles.html', context)

@login_required(login_url='connection/login')
def detail_article(request, id):
    date = datetime.now()
    article_id = dechiffrer_param(str(id))
    article = Article.objects.get(id=article_id)
    context = {
        "article": article,
        "countanswer": nbnew_answer(request),
        "count": nbnew_message(request),
        "users": new_message(request),
        "parametre": parametre(),
        "date": date
    }
    return render(request, 'article/detail_article.html', context)


@login_required(login_url='connection/login')
def add_article(request):
    date = datetime.now()

    if request.method == "POST":
        titre = bleach.clean(request.POST["titre"].strip())
        resume = bleach.clean(request.POST["resume"].strip())        
        revue = bleach.clean(request.POST["revue"].strip())
        volume = bleach.clean(request.POST["volume"].strip())
        numero = bleach.clean(request.POST["numero"].strip())
        pages = bleach.clean(request.POST["pages"].strip())
        doi = bleach.clean(request.POST["doi"].strip())
        url = bleach.clean(request.POST["url"].strip())
        keyword = bleach.clean(request.POST["keyword"].strip())
        categorie = bleach.clean(request.POST["categorie"].strip())      
        date_publication = bleach.clean(request.POST["date_publication"].strip())
        these_id = request.POST["these"]
        file = request.FILES["file"]
            
        # Vérifier l'extension du fichier
        if not file.name.endswith('.pdf'):
            return JsonResponse({
                    "status": "error",
                    "message": "Seuls les fichiers PDF sont acceptés."})    
        elif file.size > 3 * 1024 * 1024: # Limiter la taille du fichier à 3 Mo
            return JsonResponse({
                "status": "error",
                "message": "La taille du fichier est limité à 3 Mo."})
        else:
            
            liste_article = Article.objects.all()
            liste_empreint_md5 = []
            for l in liste_article:
                liste_empreint_md5.append(get_file_hash(l.file))
                l.file.close()  # Fermer le fichier après le calcul du hash
                    
            if get_file_hash(file) in liste_empreint_md5:
                return JsonResponse({
                    "status": "error",
                    "message": "Cet article existe déjà."})
            else:
                article = Article(
                    file=file,
                    titre=titre,
                    resume=resume,
                    volume=volume,
                    date_publication=date_publication, 
                    revue=revue,
                    numero=numero,
                    pages=pages,
                    doi=doi,
                    keywords=keyword,
                    url=url,
                    categorie=categorie,
                    auteur_id=request.user.id,
                    these_id=these_id)
                count0 = Article.objects.all().count()
                article.save()
                count1 = Article.objects.all().count()
                # Verifier si l'ajout a été bien effectué ou pas
                if count0 < count1:
                    return JsonResponse({
                        "status": "success",
                        "message": "Article enregistré avec succès."})
                else:
                    return JsonResponse({
                        "status": "error",
                        "message": "L'insertion a échouée."})
        
    theses = These.objects.filter(auteur_id=request.user.id)
    
    context = {
        "theses": theses,
        "date": date,
        "parametre": parametre(),
        "countanswer": nbnew_answer(request),
        "count": nbnew_message(request),
        "users": new_message(request),
    }
    return render(request, "article/add_article.html", context)


@login_required(login_url='connection/login')
def edit_article(request, id):
    date = datetime.now()
    article_id = dechiffrer_param(str(id))
    article = Article.objects.get(id=article_id)
    #On vérifie si ce membre est authorisé à acceder à cette page ou pas.
    query = Article.objects.filter(id=article_id, auteur_id=request.user.id)
    if query.exists():
        context = {
            "article": article,
            "countanswer": nbnew_answer(request),
            "count": nbnew_message(request),
            "users": new_message(request),
            "parametre": parametre(),
            "date": date
        }
        return render(request, "article/edit_article.html", context)
    else:
        return redirect("authorization")

@login_required(login_url='connection/login')
def edit_art(request):
   
   if request.method == "POST":
        id = int(request.POST["id"])
        try:
            article = Article.objects.get(id=id)
        except:
            article = None
        
        if article:
            titre = bleach.clean(request.POST["titre"].strip())  
            resume = bleach.clean(request.POST["resume"].strip())        
            revue = request.POST["revue"]
            volume = request.POST["volume"]
            numero = request.POST["numero"]
            pages = request.POST["pages"]
            doi = request.POST["doi"]
            url = request.POST["url"]
            keyword = request.POST["keyword"]
            categorie = request.POST["categorie"]       
            date_publication = bleach.clean(request.POST["date_publication"].strip())
            these_id = request.POST["these"]

            file = None
            if request.POST.get('file', True):
                f = request.FILES["file"]
                # Vérifier l'extension du fichier
                if not f.name.endswith('.pdf'):
                    return JsonResponse({
                        "status": "error",
                        "message": "Seuls les fichiers PDF sont acceptés."})     
                elif f.size > 3 * 1024 * 1024: # Limiter la taille du fichier à 3 Mo
                    return JsonResponse({
                        "status": "error",
                        "message": "La taille du fichier est limitée à 3 Mo."})
                else:
                    file = f

            if file is not None:
                liste_article = Article.objects.all()
                liste_empreint_md5 = []
                for l in liste_article:
                    liste_empreint_md5.append(get_file_hash(l.file))
                    l.file.close()  # Fermer le fichier après le calcul du hash
                        
                if get_file_hash(file) in liste_empreint_md5:
                    return JsonResponse({
                        "status": "error",
                        "message": "Cet article existe déjà."})
                else:
                    # Vérifier si la lettre de motivation a un fichié associé et que le fichier existe réellement
                    if article.file and hasattr(article.file, 'path'):
                        #Suppression de la lettre de motivation et en même temps du fichier
                        # Chemin complet du fichier
                        file_path = article.file.path
                        # Verifier l'existence du fichier
                        if os.path.exists(file_path):
                            os.remove(file_path)
                        
                article.file = file
            article.titre = titre
            article.resume = resume
            article.date_publication = date_publication
            article.revue = revue
            article.volume = volume
            article.numero = numero
            article.pages = pages
            article.doi = doi
            article.url = url
            article.keywords = keyword
            article.categorie = categorie
            article.these_id = these_id

            article.save()
            return JsonResponse({
                "status": "success",
                "message": "Article modifié avec succès."})


@login_required(login_url='connection/login')
def del_article(request, id):
    try:   
        article_id = dechiffrer_param(str(id)) 
        article = Article.objects.get(id=article_id)
    except:
        article = None
        
    if article:
        article.delete()
    return redirect("article/articles", id=article.these.id)

@login_required(login_url='connection/login')
def contact_pf(request):
    date = datetime.now()
    contacts = ContactPortfolio.objects.filter(user_id=request.user.id)   
    
    for contact in contacts:
        contact.status = 1
        contact.save()
     
    context = {
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request),
        "parametre":parametre(),
        "date":date,
        "contacts": contacts
    }
    return render(request, "contact_pf.html", context)

@login_required(login_url='connection/login')
def delete_contact(request,id):
    try:
        contact = ContactPortfolio.objects.get(id=id)
    except:
        contact = None
        
    if contact:
        contact.delete()   
    return redirect("contact_pf")


