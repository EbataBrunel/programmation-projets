# Importation des modules tiers
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.db.models import Count, Prefetch, Q
from django.views import View
from django.http import JsonResponse
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.db import transaction
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Prefetch
# from django.views.decorators.cache import cache_page
# Importation des modules locaux
from .models import*
from .forms import*
from .utils import send_email_with_html_body
from forum.models import*
from document.models import*
from annonce.models import*
from reference.models import*
from lettre_mot.models import*
from experience.models import*
from competence.models import*
from parcours.models import*
from baccalaureat.models import*
from chat.models import MessageStatus
from competence.models import TypeCompetence
from app_auth.decorator import*
from portfolio.models import ContactPortfolio, Project, These
from eajc.utils.crypto import dechiffrer_param
# Imporation des modules standards
import datetime
import re
import pdfkit
import bleach
import base64

from django.contrib.sessions.models import Session
from django.utils import timezone
from django.core import serializers

# https://www.youtube.com/watch?v=zok40RypRpo (Message en temps réel)

def parametre():
    try:
        parametre = Parametre.objects.all()[0]
    except Exception as e:
        parametre=None
    
    if parametre == None :
        return redirect("maintenance")
    else:
        return parametre
    
def userPriority():
    users = User.objects.all()
    #Memebre prioritaire
    tabUserPriority = []
    count = 0
    for user in users:
        try:
            if user.profile and user.profile.priority == 1:
                if count <= 2:
                    tabUserPriority.append(user)
                    count+=1
        except:
            pass
    return tabUserPriority

def new_message( request):
    #Lecture des messages reçus
    contacts = Contact.objects.filter(statut=0, status=1).order_by("-id")
    tabUsers = []
    tabIdUser = []
    for contact in contacts:
        #Convertion d'un string en dictionnaire
        diccode = eval(contact.codes)
        #On verifie s'il est le recepteur du message
        if diccode["user1"] == request.user.id:
            dic = {}
            tabIdUser.append(diccode["user2"])

            us = User.objects.get(id=diccode["user2"])

            dic["id"] = us.id
            dic["lastname"] = us.last_name
            dic["firstname"] = us.first_name
            dic["message"] = contact.message
            dic["date"] = contact.datecontact
            dic["photo"] = us.profile.photo
            tabUsers.append(dic)

    #On elemine des identifiants qui se dupliquent
    tab = []
    for i in tabIdUser:
        if i not in tab:
            tab.append(i)
    #On compte le nombre de messages envoyés par chaque membre
    dic = {}
    for i in tab:
        nombre = 0
        for k in tabIdUser:
            if i == k:
                nombre = nombre+1
        dic[i] = nombre

    tabMessages = []
    tabs = []
    for k,v in dic.items():
        for cont in tabUsers:
            if cont["id"] == i:
                if i not in tabs:
                    cont["nombre"] = v
                    tabMessages.append(cont)
                    tabs.append(i)
    return tabMessages

def nbnew_message(request):
    #On compte le nombre total de message reçus
    contacts = Contact.objects.filter(statut=0, status=1).order_by("-id")
    count = 0
    for contact in contacts:
        #Convertion d'un string en dictionnaire
        diccode = eval(contact.codes)
        if int(diccode["user1"]) == request.user.id:
            count = count + 1 
    return count

#On determine le nombre des reponses non lu des questions du membre connecté
def nbnew_answer(request):
    questions = Question.objects.filter(user_id=request.user.id)
    number = 0
    for question in questions:
        answers = Answer.objects.filter(question_id=question.id, status=0)
        #On exlu les reponses de ce membre qui a posé la question
        for answer in answers:
            if answer.user_id != request.user.id:
                number += 1
    return number

# Méthode de création des compétences par defaut Langue, Loisir et Certification
def create_default_type_competence(request):
    types = ["Langue", "Loisir", "Centres d'intérêt", "Certification"]

    for name in types:
        if not TypeCompetence.objects.filter(name=name, user_id=request.user.id).exists():
            TypeCompetence.objects.create(name=name, user_id=request.user.id)

def home(request):

    if request.method == "POST":
        name = request.POST["name"]
        users = User.objects.filter(last_name__icontains=name)
        tabUsers=[]
        if len(users) > 0:
            for user in users:
                try:
                    if user.profile and user.profile.status == 1:
                        tabUsers.append(user)
                except:
                    pass
        else:
            list_users = User.objects.filter(first_name__icontains=name)
            for user in list_users:
                try:
                    if user.profile and user.profile.status == 1:
                        tabUsers.append(user)
                except:
                    pass

        paginator = Paginator(tabUsers, 10)
        num_page = request.GET.get('page')
        try:
            tabUsers = paginator.get_page(num_page)
        except PageNotAnInteger:
            tabUsers = paginator.get_page(1)
        except EmptyPage:
            tabUsers = paginator.get_page(paginator.num_page)

        context = {
            "users":tabUsers,
            "userpriorities":userPriority(),
            "parametre":parametre,
            "countanswer":nbnew_answer(request),
            "count":nbnew_message(request),
            "newusers":new_message(request)
        }
        return render(request, "index.html",context)
    
    tabUsers=[]
    users=User.objects.all()
    for user in users:
        try:
            if user.profile and user.profile.status==1:
                tabUsers.append(user)
        except Exception as e:
            pass

    paginator = Paginator(tabUsers, 10)
    num_page=request.GET.get('page')
    tabUsers=paginator.get_page(num_page)
    
    context={
        "users":tabUsers,
        "userpriorities":userPriority(),
        "parametre":parametre(),
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "newusers":new_message(request)
    }
    return render(request, "index.html",context)

def authorization(request):
    date = datetime.datetime.now()
    context = {
        "parametre": parametre(),
        "date":date,
    }
    return render(request, "authorization.html", context)

def step_cv(request):
    date = datetime.datetime.now()
    # Création des compétences par defaut Langue, Loisir et Certification car elles sont obligatoires
    create_default_type_competence(request)
    
    context = {
        "parametre": parametre(),
        "date": date,
        "parametre":parametre(),
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "newusers":new_message(request)
        
    }
    return render(request, "cv/step_cv.html", context)

#Obtenir la liste des utilisateurs actuellement connectés
def get_online_users():
    # Obtenir toutes les sessions actives
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    user_ids = []

    # Parcourir les sessions pour extraire les utilisateurs connectés
    for session in sessions:
        data = session.get_decoded()
        user_id = data.get('_auth_user_id', None)
        if user_id:
            user_ids.append(user_id)

    # Renvoyer les utilisateurs correspondants
    return User.objects.filter(id__in=user_ids)

@login_required(login_url='connection/login')
#@cache_page(60 * 15)  # Cache la vue pendant 15 minutes
def dashboard(request):
    nombre_users = 0
    nombre_customers = 0
    nombre_contacts=Contact.objects.filter(statut=0,status=0).count()

    users = User.objects.all()
    for user in users:
        try:
            if user.groups.exists():
                group = user.groups.all()[0].name
                if group == "customer":
                    nombre_customers += 1
                if group == "admin":
                    nombre_users += 1
        except Exception as e:
            pass

    #On verifie si le membre a crée son profil
    try:
        profil = Profile.objects.get(user=request.user)
    except:
        profil = None
    #Nombre de pays des membres
    nombre_pays=Profile.objects.values("country").annotate(effectif=Count("country")).count()
    #On compte le nombre de cours
    countcoursencours=Cours.objects.filter(status="Traitement en cours").count()
    countcourspublie=Cours.objects.filter(status="Cours publié").count()
    countcoursnonpublie=Cours.objects.filter(status="Cours non retenu").count()

    countcourstotal=countcoursencours + countcourspublie +  countcoursnonpublie

    #On compte le nombre des nouveaux achats et nouvelles commandes
    modes=ModePaiement.objects.all()
    countachats=0
    countcmd=0
    for mode in modes:
        if mode.typepaiement == "Mobile":
            #Commandes ou achats validé
            countachats+=Commande.objects.filter(modepaiement_id=mode.id, validation='Commande validée').count()
            #Commandes en cours
            countcmd+=Commande.objects.filter(modepaiement_id=mode.id, validation='Commande en cours de traitement').count()
        else:
            countachats+=Commande.objects.filter(modepaiement_id=mode.id).count()

    #On compte le nombre des nouveaux achats et nouvelles commandes
    countachatsmember=0
    countcommandemember=0
    for mode in modes:
        if mode.typepaiement == "Mobile":
            #On selection des commandes qui ont été validées
            countachatsmember+=Commande.objects.filter(user_id=request.user.id,modepaiement_id=mode.id,validation='Commande validée').count()
            #On selection des commandes qui n'ont été validées et qui ont en cours de traitement
            countcommandemember+=Commande.objects.filter(user_id=request.user.id,modepaiement_id=mode.id,validation__in=['Commande en cours de traitement','Commande non validée']).count()           
        else:
            countachatsmember+=Commande.objects.filter(user_id=request.user.id,modepaiement_id=mode.id).count()

    #Memebre prioritaire
    tabUserPriority=[]
    count=0
    for user in users:
        try:
            if user.profile and user.profile.priority==1:
                if count <=2:
                    tabUserPriority.append(user)
                    count+=1
        except:
            pass

    #Compter le nombre de toutes les questions qui ont été posées après la dernière connexion du membre
    questions=Question.objects.filter(date__gt=request.user.last_login)
    countquestion=0
    for question in questions:
        if question.user_id != request.user.id:
            countquestion+=1

    #On compte le nombre de nouvelles notifications
    countnotif=Cours.objects.filter(user_id=request.user.id,st=1).count()
    #On recupère tous les documents vendus par mmenbre
    countachat = 0
    cours = Cours.objects.filter(user_id=request.user.id)
    for c in cours:
        #On selectionne les achats de chaque document
        commandes = Commande.objects.filter(statusachat=0)
        for commande in commandes:
            doc = eval(commande.ucours)
            for k,v in doc.items():
                #On selectionne uniquement les documents du membre qui ont été acheté 
                if k == c.id:
                    countachat += 1
                    
    # Recuperer tous les documents vendus de tous les mmenbres
    countallachat = 0
    cours = Cours.objects.all()
    for c in cours:
        #On selectionne les achats de chaque document
        commandes = Commande.objects.filter(statusachat=0)
        for commande in commandes:
            doc = eval(commande.ucours)
            for k,v in doc.items():
                #On selectionne uniquement les documents du membre qui ont été acheté 
                if k == c.id:
                    countallachat += 1

    #On compte le nombre de commande
    annonces=Annonce.objects.all()
    #On recupère la dernière annonce
    annonce=annonces[len(annonces)-1]

    #On compte le nombre de nouvelles lettres de motivation
    countlms = Lettre_mot.objects.filter(statut=0).count()
    
    # Compter le nombre de nouveaux chats non lus
    countnewchat = MessageStatus.objects.filter(user_id=request.user.id, read=0).count()
    
    # Nombre des utilisateurs actuellement en lignes
    countuseronline = get_online_users().count()
    
    #Compter le nombre de signalement des question et réponse du forum
    countreportquestion = SignalerQuestion.objects.all().count()
    countreportanswer = SignalerAnswer.objects.all().count()
    countreport = countreportanswer + countreportquestion
    
    #Nombre de demande de suppression de compte d'utilisateur
    countdmddeleteaccount = Profile.objects.filter(status_deleteaccount=1).count()
    
    #Nombre de contacts portfolio
    countcontactportfolio = ContactPortfolio.objects.filter(user_id=request.user.id, status=0).count()
    
    #Nombre de portfolio
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
        dic["user"] = user
        
        user_split = re.split(r'[ -]', us.last_name)
        f_name = user_split[0].lower()
    
        param = f_name+"-"+str(us.id)
        dic["param"] = param
        
        list_users.append(dic)
    
    date = datetime.datetime.now()
    context = {
        "fresh_dashbord": True,
        "profil": profil,
        "annonce": annonce,
        "userspriorities": tabUserPriority,
        "countachat":countachat,
        "countallachat": countallachat,
        "countachats": countachats,
        "countcmd": countcmd,
        "countnotif": countnotif,
        "countcoursencours": countcoursencours,
        "countcourspublie": countcourspublie,
        "countcoursnonpublie": countcoursnonpublie,
        "countcourstotal": countcourstotal,
        "nb_portfolios": len(tabUsers),
        "countanswer": nbnew_answer(request),
        "count": nbnew_message(request),
        "users": new_message(request),
        "parametre": parametre(),
        "date": date,
        "countusers": nombre_users,
        "count_country": nombre_pays,
        "countcustomers": nombre_customers,
        "countmembers": users.count(),
        "nombre_contact": nombre_contacts,
        "countquestion": countquestion,
        "countachatsmember": countachatsmember,
        "countcommandemember": countcommandemember,
        "countlms": countlms,
        "countnewchat": countnewchat,
        "countuseronline": countuseronline,
        "users_line": get_online_users(),
        "countreport": countreport,
        "countdmddeleteaccount": countdmddeleteaccount,
        "countcontactportfolio": countcontactportfolio
        
    }
    return render(request, "dashboard.html",context)

#================== Fonctions d'erreurs ====================
def handler404(request, exception):
    context={}
    return render(request, "400.html", context)

def handler500(request):
    context={}
    return render(request, "500.html", context)

def maintenance(request):
    context={}
    return render(request, "maintenance.html", context)

#=================== Gestion de contact ======================
@transaction.atomic
@csrf_exempt
def contact(request):
    if request.method=="POST":    
        date = datetime.datetime.now()    
        form = ContactForm(request.POST)
        if form.is_valid():
            name = bleach.clean(form.cleaned_data["name"])
            email = form.cleaned_data["email"]
            subject = bleach.clean(form.cleaned_data["subject"])
            message = bleach.clean(form.cleaned_data["message"])
            #On verifie si l'adresse e-mail correspond bien
            regexp = r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$"
            if not re.search(regexp, email):
                return JsonResponse({'status':0})
            else:
                contact = Contact(name=name, email=email, subject=subject, message=message, statut=0, codes=None,status=False)
                count0 = Contact.objects.all().count()
                contact.save()
                count1 = Contact.objects.all().count()

                subject = "Confirmation"
                template = "email/emailcontact.html"
                receivers = [email]
                
                context = {
                    'email':email,
                    'date': date,
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
            form = ContactForm()

    form = ContactForm()
    date = datetime.datetime.now()
    context = {
        "form":form,
        "parametre":parametre(),
        "userpriorities":userPriority(),
        "date":date
    }
    return render(request, "contact/contact.html", context)

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=['admin'])
def contacts(request):
    liste_contacts=Contact.objects.filter(statut=0,status=0)
    for stat in liste_contacts:
        status=stat
        status.statut=1
        status.save()

    cont = Contact.objects.values("email").filter(statut=1,status=0).annotate(effectif = Count("email"))
    tabContacts = []
    for contact in cont:
        tab = {}
        #On recupère le dernier message de chaque e-mail
        c = Contact.objects.filter(email=contact["email"], status=0).order_by("-id")[:1]
        con = c[0]
        tab["id"] = con.id
        tab["email"] = con.email
        tab["name"] = con.name
        tab["subject"] = con.subject
        tab["datecontact"] = con.datecontact
        tab["message"] = con.message
        tab["effectif"] = contact["effectif"]

        tabContacts.append(tab)

    tabemail = []
    for contact in cont:
        tabemail.append(contact["email"])

    tabContacts2 = []
    cont1 = Contact.objects.values("email").filter(status=0).annotate(effectif=Count("email"))
    for contact1 in cont1:
            if contact1["email"] not in tabemail :
                
                tab1 = {}
                c1 = Contact.objects.filter(email=contact1["email"], status=0).order_by("-id")[:1]
                #On recupère le contact, le résultat est un tableau
                con1 = c1[0]
                tab1["id"] = con1.id
                tab1["email"] = con1.email
                tab1["name"] = con1.name
                tab1["subject"] = con1.subject
                tab1["datecontact"] = con1.datecontact
                tab1["message"] = con1.message
                tab1["effectif"] = contact1["effectif"]

                tabContacts2.append(tab1)

    date = datetime.datetime.now()

    context = {
        "listeContact":tabContacts, 
        "listeContact2":tabContacts2,
        "parametre":parametre(),
        "date":date,
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request)
        }
    return render(request, "contact/contacts.html", context)

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=['admin'])
def details_contact(request, id):
    contacts = Contact.objects.filter(email=id, status=0).order_by('-id')
    #Changement de statut
    for stat in contacts:
        status = stat
        status.statut = 2
        status.save()

    listeContact=[]
    for contact in contacts:
        dic = {}
        dic["id"] = contact.id
        dic["name"] = contact.name
        dic["subject"] = contact.subject
        dic["message"] = contact.message
        dic["datecontact"] = contact.datecontact
        listeContact.append(dic)

    date=datetime.datetime.now()

    context={
        "listeContact":listeContact,
        "email":id,
        "parametre":parametre(),
        "date":date,
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request)
    }
    return render(request, "contact/details_contact.html", context)

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=['admin'])
def del_contact(request, id):
    contact = Contact.objects.get(id=id)
    contact.delete()
    #On verifie s'il existe encore des contacts de cette adresse
    try:
        c=Contact.objects.filter(id=id).count()
    except Exception as e:
        return redirect("contact/contacts")

    return redirect("contact/details_contact", id=contact.email)

def  delete_messages(request, id):
    contacts = Contact.objects.all()
    for contact in contacts:
        if contact.codes:
            code = eval(contact.codes)
            if (code["user2"] == request.user.id and code["user1"] == id):
                contact.delete()
            if (code["user1"] == request.user.id and code["user2"] == id):
                contact.delete()
    return JsonResponse({'status':1})

class del_message(View):
    def get(self, request, id, *args, **kwargs):
        contact=Contact.objects.get(id=id)
        diccod=eval(contact.codes)
        #On verifie si le membre connecté est l'emetteur 
        if diccod["user2"] == request.user.id:
            #On verifie si le recepteur à supprimer ou pas le message de son côté.
            if contact.statutdel == 2:
                #On supprime deffinitivement le message
                contact.delete()
                return JsonResponse({'status':1})
            else:
                #On fait une misse à jour le message
                contact.statutdel = 1
                contact.save()
                return JsonResponse({'status':1})
        else:
            #On verifie si l'emetteur à supprimer ou pas le message de son côté.
            if contact.statutdel == 1:
                #On supprime deffinitivement le message
                contact.delete()
                return JsonResponse({'status':1})
            else:
                #On fait une misse à jour le message
                contact.statutdel = 2
                contact.save()
                return JsonResponse({'status':1})

@login_required(login_url='connection/login')
@allowed_users(allowed_roles = ['admin'])
def delete_contact(request, id):
    cont = Contact.objects.get(id=id)
    contacts = Contact.objects.filter(email=cont.email)
    for contact in contacts:
        contact.delete()
    return redirect("contact/contacts")

def contactuser(request,id):
    date = datetime.datetime.now() 
    user_id = dechiffrer_param(str(id))  
    user = User.objects.get(id=user_id)
    context={
            "user":user,
            "parametre":parametre(),
            "date":date,
            "userpriorities":userPriority(),
            "countanswer":nbnew_answer(request),
            "count":nbnew_message(request),
            "users":new_message(request)
    }
    return render(request, "contact/contactuser.html", context)


@login_required(login_url='connection/login')
def contuser(request):
    if request.method=="POST":
        id = request.POST["user"]
        subject = request.POST["subject"]
        content = request.POST["content"]
        dic = {}
        #Identdifier du recepteur
        dic["user1"] = int(id)
        #Identifiant du l'emeteur
        dic["user2"] = request.user.id

        contact = Contact(
            name="",
            email="",
            subject=subject,
            statut=0,
            status=1,
            message=content,
            codes=dic
        )
        count0 = Contact.objects.all().count()
        contact.save()
        count1 = Contact.objects.all().count()
        if count0 < count1:
             return JsonResponse({
                    "status": "success",
                    "message": "Message envoyé avec succès."})
        else:
             return JsonResponse({
                    "status": "error",
                    "message": "L'envoie du message a échoué."})

def services(request):

    context={
        "userpriorities":userPriority(),
        "parametre":parametre()
    }
    return render(request, "contact/services.html", context)

def apropos(request):
    context={
        "userpriorities":userPriority(),
        "parametre":parametre()
    }
    return render(request, "contact/apropos.html", context)

@login_required(login_url='connection/login')
def messag(request):
    date = datetime.datetime.now()

    liste_contacts = Contact.objects.filter(statut=0, status=1)
    for contact in liste_contacts:
        diccode = eval(contact.codes)
        #On verifie si le membre connecté est le recepteur 
        if diccode["user1"]==request.user.id:
            cont = contact
            cont.statut=1
            cont.save()

    contacts = Contact.objects.filter(status=1).order_by("-id")
    tabMessage = []
    tabIdUser = []
    for contact in contacts:
        
        if contact.statut==1:
            diccod = eval(contact.codes)
            #On verifie si le membre connecté est le recepteur 
            if diccod["user1"]==request.user.id:
                #On verifie si ce message a été supprimé ou pas
                if contact.statutdel == 0 or contact.statutdel == 1:
                    dic={}
                    try:
                        user=User.objects.get(id=diccod["user2"])
                    except:
                        user=None
                    
                    if user is not None:
                        dic["id"] = user.id
                        dic["user"] = user
                        dic["message"] = contact.message
                        dic["datecontact"] = contact.datecontact
                        dic["statut"] = contact.statut
                        dic["status"] = 1
                        tabIdUser.append(user.id)
                        tabMessage.append(dic)

            #On verifie si le membre connecté est l'emeteur   
            if diccod["user2"]==request.user.id:
                if contact.statutdel == 0 or contact.statutdel == 2:
                    dic={}
                    try:
                        user=User.objects.get(id=diccod["user1"])
                    except:
                        user=None
                    
                    if user is not None:
                        dic["id"]=user.id
                        dic["user"]=user
                        dic["message"]=contact.message
                        dic["datecontact"]=contact.datecontact
                        dic["statut"]=contact.statut
                        # on marque ou pas le nouveau message
                        dic["status"]=0
                        tabIdUser.append(user.id)    
                        tabMessage.append(dic)

        #On verifie si le membre connecté est l'emeteur  
        if contact.statut==0: 
            diccod=eval(contact.codes)
            if diccod["user2"]==request.user.id:
                if contact.statutdel == 0 or contact.statutdel == 2:
                    dic={}
                    try:
                        user=User.objects.get(id=diccod["user1"])
                    except:
                        user=None
                    
                    if user is not None:
                        dic["id"]=user.id
                        dic["user"]=user
                        dic["message"]=contact.message
                        dic["datecontact"]=contact.datecontact
                        dic["statut"]=contact.statut
                        # on marque ou pas le nouveau message
                        dic["status"]=0
                        tabIdUser.append(user.id)    
                        tabMessage.append(dic)
                
    #On supprime l'identifiant des membres qui se reproduisent
    tab=[]
    for i in tabIdUser:
        if i not in tab:
            tab.append(i)

    #On compte le nombre de messages envoyés par chaque membre
    dic={}
    for i in tab:
        nombre=0
        for k in tabIdUser:
            if i==k:
                nombre=nombre+1
        dic[i]=nombre

    tabMessages=[]
    tabs=[]
    for i,v in dic.items():
        for cont in tabMessage:
            if cont["id"]==i:
                if i not in tabs:
                    tabMessages.append(cont)
                    cont["nombre"]=v
                    tabs.append(i)


    #On garde un seul affichage d'un membre
    liste_contacts=Contact.objects.filter(statut=2, status=1).order_by("-id")
    tabMessage2=[]
    tabIdUser2=[]
    for contact in liste_contacts:
        diccode=eval(contact.codes)

        
        #On verifie si le membre connecté est le recepteur 
        if diccode["user1"]==request.user.id:
            if contact.statutdel == 0 or contact.statutdel == 1:
                dic={}
                try:
                    user=User.objects.get(id=diccode["user2"])
                except:
                    user=None

                if user is not None:
                    dic["id"]=user.id
                    dic["user"]=user
                    dic["message"]=contact.message
                    dic["datecontact"]=contact.datecontact
                    dic["statut"]=contact.statut
                    # on marque ou pas le nouveau message
                    dic["status"]=1
                    tabIdUser2.append(user.id)
                    tabMessage2.append(dic)

        #On verifie si le membre connecté est l'emeteur   
        if diccode["user2"]==request.user.id:
            if contact.statutdel == 0 or contact.statutdel == 2:
                dic={}
                try:
                    user=User.objects.get(id=diccode["user1"])
                except:
                    user=None

                if user is not None:
                    dic["id"]=user.id
                    dic["user"]=user
                    dic["message"]=contact.message
                    dic["datecontact"]=contact.datecontact
                    dic["statut"]=contact.statut
                    # on marque ou pas le nouveau message
                    dic["status"]=0
                    tabIdUser2.append(user.id)    
                    tabMessage2.append(dic)

    #On supprime l'identifiant des membres qui se reproduisent
    tab2=[]
    for i in tabIdUser2:
        if i not in tab2:
            tab2.append(i)

    #On affiche une seule fois le nom de l'emeteur
    tb=[]
    for mes in tabMessages:
        tb.append(mes["id"])
    tab0=[]
    for k in tab2:
        if k not in tb:
           tab0.append(k) 

    tabMessages2=[]
    tabs2=[]
    for i in tab0:
        for cont in tabMessage2:
            if cont["id"]==i:
                if i not in tabs2:
                    tabMessages2.append(cont)
                    tabs2.append(i)

    #On trie les messages par ordre d'arrivé
    """tabMessageOrdonnee=[] 
    for message in tabMessages:
        tabMessageOrdonnee.append(message)

    for message in tabMessages2:
        tabMessageOrdonnee.append(message)"""

    context={
        "contacts":tabMessages,
        "contacts2":tabMessages2,
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request),
        "parametre":parametre(),
        "date":date
    }
    return render(request, "contact/messages.html", context)

#Détails des messages 
@login_required(login_url='connection/login')
def detmes(request,id):
    date=datetime.datetime.now()
    user=User.objects.get(id=id)

    contacts=Contact.objects.filter(statut=0, status=1)
    for contact in contacts:
        diccode=eval(contact.codes)
        #On verifie si le membre connecté est le recepteur 
        if diccode["user1"]==request.user.id:
            cont=contact
            cont.statut=2
            cont.save()

    list_contacts=Contact.objects.filter(statut=1, status=1)
    for contact in list_contacts:
        diccode=eval(contact.codes)
        #On verifie également si le membre connecté est le recepteur 
        if diccode["user1"]==request.user.id:
            cont=contact
            cont.statut=2
            cont.save()
        
    if request.method=="POST":
        subject=request.POST["subject"]
        content=request.POST["content"]
        dic={}

        dic["user1"]=id
        dic["user2"]=request.user.id

        contact=Contact(
            name="",
            email="",
            subject=subject,
            datecontact= date,
            statut=0,
            status=1,
            message=content,
            codes=dic
        )
        contact.save()
        return redirect("contact/detmes",id=id)

    tabMessage=[]
    contacts=Contact.objects.filter(statut__in=[0,1,2], status=1).order_by("-id")
    for contact in contacts:
        codes=eval(contact.codes)
        if codes["user1"]==request.user.id and codes["user2"]==id or codes["user1"]==id and codes["user2"]==request.user.id:
            
            dic={}
            #On verifie si le membre connecté est le recepteur
            if codes["user1"]==request.user.id:
                # On verifie si le message a été supprimé ou pas
                if contact.statutdel == 0 or contact.statutdel == 1:
                    user=User.objects.get(id=codes["user2"])
                    dic["code"]=contact.id
                    dic["status"]=0
                    dic["id"]=user.id
                    dic["lastname"]=user.last_name
                    dic["firstname"]=user.first_name
                    dic["subject"]=contact.subject
                    dic["message"]=contact.message
                    dic["datecontact"]=contact.datecontact
                    tabMessage.append(dic)
            else:
                # On verifie si le message a été supprimé ou pas
                if contact.statutdel == 0 or contact.statutdel == 2:
                    user=User.objects.get(id=codes["user1"])
                    dic["code"]=contact.id
                    dic["status"]=1
                    dic["id"]=user.id
                    dic["lastname"]="vous"
                    dic["subject"]=contact.subject
                    dic["message"]=contact.message
                    dic["datecontact"]=contact.datecontact
                    tabMessage.append(dic)

    context={
        "user":user,
        "contacts":tabMessage,
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request),
        "parametre":parametre(),
        "date":date
    }
    return render(request, "contact/detmes.html", context)

    
@login_required(login_url='connection/login') 
def statistique(request):
    date = datetime.datetime.now()

    questions = Question.objects.all()

    nbjanuary = 0
    nbfebruary = 0
    nbmarch = 0
    nbapril = 0
    nbmay = 0
    nbjune = 0
    nbjully = 0
    nbaugust = 0
    nbseptember = 0
    nboctober = 0
    nbnovember = 0
    nbdecember = 0
    tabmonth = []
    for question in questions:
        if question.date.year==date.year:
            if question.date.month == 1:
                nbjanuary+=1
            elif question.date.month == 2:
                nbfebruary+=1
            elif question.date.month == 3:
                nbmarch+=1
            elif question.date.month == 4:
                nbapril+=1
            elif question.date.month == 5:
                nbmay+=1
            elif question.date.month == 6:
                nbjune+=1
            elif question.date.month == 7:
                nbjully+=1
            elif question.date.month == 8:
                nbaugust+=1
            elif question.date.month == 9:
                nbseptember+=1
            elif question.date.month == 10:
                nboctober+=1
            elif question.date.month == 11:
                nbnovember+=1
            else:
                nbdecember+=1
    
    tabmonth.append(nbjanuary)
    tabmonth.append(nbfebruary)
    tabmonth.append(nbmarch)
    tabmonth.append(nbapril)
    tabmonth.append(nbmay)
    tabmonth.append(nbjune)
    tabmonth.append(nbjully)
    tabmonth.append(nbaugust)
    tabmonth.append(nbseptember)
    tabmonth.append(nboctober)
    tabmonth.append(nbnovember)
    tabmonth.append(nbdecember)

    #On compte le nombre de cours
    countcoursencours = Cours.objects.filter(status="Traitement en cours").count()
    countcourspublie = Cours.objects.filter(status="Cours publié").count()
    countcoursnonpublie = Cours.objects.filter(status="Cours non retenu").count()

    tabCours = []
    tabCours.append(countcoursencours)
    tabCours.append(countcourspublie)
    tabCours.append(countcoursnonpublie)

    context={
        "coursdata":tabCours,
        "months":tabmonth,
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request),
        "parametre":parametre(),
        "date":date
    }
    return render(request, "statistique.html",context)



@login_required(login_url='connection/login')
def recap(request):
    date = datetime.datetime.now()
    #======== Parcours ===============
    parcours = Parcours.objects.filter(user_id=request.user.id).select_related('etablissement','annee','formation').order_by("-annee_id")
    #======== Competence ==============
    competenceLangues = []
    competenceLoisirs = []
    competenceCentresInteret = []
    competenceCertifications = []
    
    #======================= Expérience professionnelle=====================
    listexperiences = Experience.objects.filter(user_id=request.user.id, status=1).order_by("-date_debut")
    #On convertit le statut(une chaine de caratère) en dictionnaire
    experiences = []
    experiencesProjetP = []
    experiencesProjetA = []
    for experience in listexperiences:
        if experience.type_exp in ["Employé(e)", "Stagiaire", "Alternance"]:
            dic={}
            dic["experience"] = experience
            dic["taches"] = eval(experience.tache)
            experiences.append(dic)
        elif experience.type_exp == "Projet":
            dic={}
            dic["experience"] = experience
            dic["taches"] = eval(experience.tache)
            experiencesProjetP.append(dic)
        else:
            dic={}
            dic["experience"] = experience
            dic["taches"] = eval(experience.tache)
            experiencesProjetA.append(dic)
            
    #======================= Référence ====================================
    references = Reference.objects.filter(user_id=request.user.id, status=1).select_related('entreprise')
    cpReference = Reference.objects.filter(user_id=request.user.id, status=1).count()

    #Recuperer le baccalaureat
    baccalaureat = Baccalaureat.objects.filter(user_id=request.user.id).first()

    type_competences = (
        TypeCompetence.objects
        .filter(user=request.user)
        .annotate(
            nb_competences=Count(
                'competence',
                filter=Q(competence__status=True) # Q permet d'ajouter une condition
            )
        )
        .filter(nb_competences__gt=0)
        .prefetch_related(
            Prefetch(
                'competence_set',
                queryset=Competence.objects.filter(status=True).order_by('name'),
            )
        )
        .order_by('name')
    )
            
    tabCompetences = []
    
    for t in type_competences:
        for competence in t.competence_set.filter(status=True):
            print(competence.status)
            if competence.status == True:
                if t.name == "Langue":
                    competenceLangues.append(competence)
                elif t.name == "Loisir":
                    competenceLoisirs.append(competence)
                elif t.name == "Centres d'intérêt":
                    competenceCentresInteret.append(competence)
                elif t.name == "Certification":
                    competenceCertifications.append(competence)
                else:
                    tabCompetences.append(competence)
            
    context = {
        "parcours": parcours,
        "experiences": experiences,
        "experiencesProjetP": experiencesProjetP,
        "experiencesProjetA": experiencesProjetA,
        "competenceLangues":competenceLangues,
        "cpLangue":len(competenceLangues),
        "competenceLoisirs":competenceLoisirs,
        "cpLoisir":len(competenceLoisirs),
        "competenceCentresInteret": competenceCentresInteret,
        "cpCentresInteret": len(competenceCentresInteret),
        "competenceCertifications": competenceCertifications,
        "cpCertification": len(competenceCertifications),
        "references": references,
        "cpReference": cpReference,
        "baccalaureat": baccalaureat,
        "competences": tabCompetences,
        "type_competences": type_competences,

        "countanswer": nbnew_answer(request),
        "count": nbnew_message(request),
        "users": new_message(request),
        "parametre": parametre(),
        "date": date,

    }
    return render(request, "cv/recap.html", context)

@login_required(login_url='connection/login')
def recap_1(request):
    date = datetime.datetime.now()
    #======== Parcours ===============
    parcours = Parcours.objects.filter(user_id=request.user.id, status=1).select_related('etablissement','annee','formation').order_by("-annee_id")
    countpar = Parcours.objects.filter(user_id=request.user.id, status=1).count()
    #======== Competence ==============
    competenceLangues = []
    competenceLoisirs = []
    competenceCentresInteret = []
    competenceCertifications = []
    tabCompetences = []
    countcomp = 0
    
    type_competences = (
        TypeCompetence.objects
        .filter(user=request.user)
        .annotate(
            nb_competences=Count(
                'competence',
                filter=Q(competence__status=True) # Q permet d'ajouter une condition
            )
        )
        .filter(nb_competences__gt=0)
        .prefetch_related(
            Prefetch(
                'competence_set',
                queryset=Competence.objects.filter(status=True).order_by('name'),
            )
        )
        .order_by('name')
    )
    
    tabCompetences = []
    
    for t in type_competences:
        for competence in t.competence_set.all():
            if competence.status == 1:
                if t.name == "Langue":
                    competenceLangues.append(competence)
                elif t.name == "Loisir":
                    competenceLoisirs.append(competence)
                elif t.name == "Centres d'intérêt":
                    competenceCentresInteret.append(competence)
                elif t.name == "Certification":
                    competenceCertifications.append(competence)
                else:
                    countcomp += 1
                    tabCompetences.append(competence)

    #======================= Référence ====================================
    references = Reference.objects.filter(user_id=request.user.id, status=1).select_related('entreprise')
    cpReference = Reference.objects.filter(user_id=request.user.id, status=1).count()

    #======================= Expérience professionnelle=====================
    listexperiences = Experience.objects.filter(user_id=request.user.id, status=1)
    countexp = Experience.objects.filter(user_id=request.user.id, status=1).count()

    #======================= Expérience professionnelle=====================
    listexperiences = Experience.objects.filter(user_id=request.user.id, status=1).order_by("-date_debut")
    #On convertit le statut(une chaine de caratère) en dictionnaire
    experiences = []
    experiencesProjetP = []
    experiencesProjetA = []
    for experience in listexperiences:
        if experience.type_exp in ["Employé(e)","Stagiaire","Alternance"]:
            dic={}
            dic["experience"] = experience
            dic["taches"] = eval(experience.tache)
            experiences.append(dic)
        elif experience.type_exp == "Projet":
            dic={}
            dic["experience"] = experience
            dic["taches"] = eval(experience.tache)
            experiencesProjetP.append(dic)
        else:
            dic={}
            dic["experience"] = experience
            dic["taches"] = eval(experience.tache)
            experiencesProjetA.append(dic)
            
        
    #Recuperer le baccalaureat
    baccalaureat = Baccalaureat.objects.filter(user_id=request.user.id).first()

    context = {
        "countpar":countpar,
        "countexp":countexp,
        "countcomp":countcomp,
        "baccalaureat":baccalaureat,
        "parcours":parcours,
        "experiences":experiences,
        "experiencesProjetP": experiencesProjetP,
        "experiencesProjetA": experiencesProjetA,
        "competenceLangues":competenceLangues,
        "cpLangue":len(competenceLangues),
        "competenceLoisirs":competenceLoisirs,
        "cpLoisir":len(competenceLoisirs),
        "competenceCentresInteret": competenceCentresInteret,
        "cpCentresInteret": len(competenceCentresInteret),
        "competences":tabCompetences,
        "references":references,
        "cpReference":cpReference,
        "competenceCertifications": competenceCertifications,
        "cpCertification": len(competenceCertifications),
        "countanswer": nbnew_answer(request),
        "count": nbnew_message(request),
        "users": new_message(request),
        "parametre": parametre(),
        "date": date
    }
    return render(request, "cv/recap-1.html", context)

@login_required(login_url='connection/login')
def recap_2(request):
    date = datetime.datetime.now()
    #======== Parcours ===============
    parcours = Parcours.objects.filter(user_id=request.user.id).select_related('etablissement','annee','formation').order_by("-annee_id")
    #======== Competence ==============
    competenceLangues = []
    competenceLoisirs = []
    competenceCentresInteret = []
    competenceCertifications = []
    #======================= Expérience professionnelle=====================
    listexperiences = Experience.objects.filter(user_id=request.user.id, status=1).order_by("-date_debut")
    #On convertit le statut(une chaine de caratère) en dictionnaire
    experiences = []
    experiencesProjetP = []
    experiencesProjetA = []
    for experience in listexperiences:
        if experience.type_exp in ["Employé(e)","Stagiaire","Alternance"]:
            dic={}
            dic["experience"] = experience
            dic["taches"] = eval(experience.tache)
            experiences.append(dic)
        elif experience.type_exp == "Projet":
            dic={}
            dic["experience"] = experience
            dic["taches"] = eval(experience.tache)
            experiencesProjetP.append(dic)
        else:
            dic={}
            dic["experience"] = experience
            dic["taches"] = eval(experience.tache)
            experiencesProjetA.append(dic)
            
    #======================= Référence ====================================
    references = Reference.objects.filter(user_id=request.user.id, status=1).select_related('entreprise')
    cpReference = Reference.objects.filter(user_id=request.user.id, status=1).count()

    #Recuperer le baccalaureat
    baccalaureat = Baccalaureat.objects.filter(user_id=request.user.id).first()

            
    type_competences = (
        TypeCompetence.objects
        .filter(user=request.user)
        .annotate(
            nb_competences=Count(
                'competence',
                filter=Q(competence__status=True) # Q permet d'ajouter une condition
            )
        )
        .filter(nb_competences__gt=0)
        .prefetch_related(
            Prefetch(
                'competence_set',
                queryset=Competence.objects.filter(status=True).order_by('name'),
            )
        )
        .order_by('name')
    )
    
    tabCompetences = []
    
    for t in type_competences:
        for competence in t.competence_set.all():
            if competence.status == 1:
                if t.name == "Langue":
                    competenceLangues.append(competence)
                elif t.name == "Loisir":
                    competenceLoisirs.append(competence)
                elif t.name == "Centres d'intérêt":
                    competenceCentresInteret.append(competence)
                elif t.name == "Certification":
                    competenceCertifications.append(competence)
                else:
                    tabCompetences.append(competence)
    
    context = {
        "parcours": parcours,
        "experiences": experiences,
        "experiencesProjetP": experiencesProjetP,
        "experiencesProjetA": experiencesProjetA,
        "competenceLangues": competenceLangues,
        "cpLangue": len(competenceLangues),
        "competenceLoisirs": competenceLoisirs,
        "cpLoisir": len(competenceLoisirs),
        "competenceCentresInteret": competenceCentresInteret,
        "cpCentresInteret": len(competenceCentresInteret),
        "competenceCertifications": competenceCertifications,
        "cpCertification": len(competenceCertifications),
        "references": references,
        "cpReference": cpReference,
        "baccalaureat": baccalaureat,
        "type_competences": type_competences,
        "competences": tabCompetences,

        "countanswer": nbnew_answer(request),
        "count": nbnew_message(request),
        "users": new_message(request),
        "parametre": parametre(),
        "date": date,

    }
    return render(request, "cv/recap-2.html", context)


@login_required(login_url='connection/login')
def gencv(request):
    #======== Parcours ===============
    parcours = Parcours.objects.filter(user_id=request.user.id).select_related('etablissement','annee','formation').order_by("-annee_id")
    #======== Competence ==============
    competenceLangues = []
    competenceLoisirs = []
    competenceCentresInteret = []
    competenceCertifications = []
    #======================= Expérience professionnelle=====================
    listexperiences = Experience.objects.filter(user_id=request.user.id, status=1).order_by("-date_debut")
    #On convertit le statut(une chaine de caratère) en dictionnaire
    experiences = []
    experiencesProjetP = []
    experiencesProjetA = []
    for experience in listexperiences:
        if experience.type_exp in ["Employé(e)","Stagiaire","Alternance"]:
            dic={}
            dic["experience"] = experience
            dic["taches"] = eval(experience.tache)
            experiences.append(dic)
        elif experience.type_exp == "Projet":
            dic={}
            dic["experience"] = experience
            dic["taches"] = eval(experience.tache)
            experiencesProjetP.append(dic)
        else:
            dic={}
            dic["experience"] = experience
            dic["taches"] = eval(experience.tache)
            experiencesProjetA.append(dic)
            
    user = User.objects.get(id=request.user.id)

    #======================= Référence ====================================
    references = Reference.objects.filter(user_id=request.user.id, status=1).select_related('entreprise')
    cpReference = Reference.objects.filter(user_id=request.user.id, status=1).count()

    #Recuperer le baccalaureat
    baccalaureat = Baccalaureat.objects.filter(user_id=request.user.id).first()

            
    type_competences = (
        TypeCompetence.objects
        .filter(user=request.user)
        .annotate(
            nb_competences=Count(
                'competence',
                filter=Q(competence__status=True) # Q permet d'ajouter une condition
            )
        )
        .filter(nb_competences__gt=0)
        .prefetch_related(
            Prefetch(
                'competence_set',
                queryset=Competence.objects.filter(status=True).order_by('name'),
            )
        )
        .order_by('name')
    )
    
    tabCompetences = []
    
    for t in type_competences:
        for competence in t.competence_set.all():
            if competence.status == 1:
                if t.name == "Langue":
                    competenceLangues.append(competence)
                elif t.name == "Loisir":
                    competenceLoisirs.append(competence)
                elif t.name == "Centres d'intérêt":
                    competenceCentresInteret.append(competence)
                elif t.name == "Certification":
                    competenceCertifications.append(competence)
                else:
                    tabCompetences.append(competence)
                
    base64_string = ''
    if request.user.profile.photo:      
        # Chemin vers votre image
        image_path = request.user.profile.photo

        # Lire l'image en mode binaire et encoder en Base64
        base64_string = base64.b64encode(image_path.read()).decode('utf-8')

    context = {
        "base64_image": base64_string,
        "user":user,
        "parcours":parcours,
        "experiences":experiences,
        "baccalaureat":baccalaureat,
        "experiencesProjetP":experiencesProjetP,
        "experiencesProjetA":experiencesProjetA,
        
        "type_competences": type_competences,
        "competences": tabCompetences,
        "competenceLangues":competenceLangues,
        "cpLangue":len(competenceLangues),
        "competenceLoisirs":competenceLangues,
        "cpLoisir":len(competenceLoisirs),
        "competenceCentresInteret": competenceCentresInteret,
        "cpCentresInteret": len(competenceCentresInteret),
        "competenceCertifications": competenceCertifications,
        "cpCertification": len(competenceCertifications),
        
        "references":references,
        "cpReference":cpReference,
        
        "domain": get_current_site(request).domain

    }
    template = get_template("cv/gencv.html")
    html = template.render(context)
    options = {
        'page-size': 'Letter',
        'encoding': "UTF-8",
    }
    pdf = pdfkit.from_string(html, False, options)
    reponse = HttpResponse(pdf, content_type='application/pdf')
    reponse['Content-Disposition'] = f"attachment; filename=CV_{ user.last_name }_{ user.first_name }.pdf"
    return reponse

@login_required(login_url='connection/login')
def generatecv_1(request):
    #======== Parcours ===============
    parcours = Parcours.objects.filter(user_id=request.user.id).select_related('etablissement','annee','formation').order_by("-annee_id")
    #======== Competence ==============
    competenceLangues = []
    competenceLoisirs = []
    competenceCentresInteret = []
    competenceCertifications = []
    tabCompetences = []
    competences = Competence.objects.filter(user_id=request.user.id, status=1)
    countcomp = 0
    for competence in competences:
        if competence.status == 1:
            if competence.type_competence.name == "Langue":
                competenceLangues.append(competence)
            elif competence.type_competence.name == "Loisir":
                competenceLoisirs.append(competence)
            elif competence.type_competence.name == "Certification":
                competenceCertifications.append(competence)
            else:
                countcomp += 1
                tabCompetences.append(competence)

    #======================= Expérience professionnelle=====================
    listexperiences = Experience.objects.filter(user_id=request.user.id, status=1).order_by("-date_debut")
    #On convertit le statut(une chaine de caratère) en dictionnaire
    experiences = []
    experiencesProjetP = []
    experiencesProjetA = []
    for experience in listexperiences:
        if experience.type_exp in ["Employé(e)","Stagiaire","Alternance"]:
            dic={}
            dic["experience"] = experience
            dic["taches"] = eval(experience.tache)
            experiences.append(dic)
        elif experience.type_exp == "Projet":
            dic={}
            dic["experience"] = experience
            dic["taches"] = eval(experience.tache)
            experiencesProjetP.append(dic)
        else:
            dic={}
            dic["experience"] = experience
            dic["taches"] = eval(experience.tache)
            experiencesProjetA.append(dic)
        
    #Recuperer le baccalaureat
    baccalaureat = Baccalaureat.objects.filter(user_id=request.user.id).first()

    user = User.objects.get(id=request.user.id)
    context = {
        "user":user,
        "baccalaureat":baccalaureat,
        "parcours":parcours,
        "experiences":experiences,
        "baccalaureat":baccalaureat,
        "experiencesProjetP":experiencesProjetP,
        "experiencesProjetA":experiencesProjetA,
        "competenceLangues":competenceLangues,
        "cpLangue":len(competenceLangues),
        "competenceLoisirs":competenceLoisirs,
        "cpLoisir":len(competenceLoisirs),
        "competenceCentresInteret": competenceCentresInteret,
        "cpCentresInteret": len(competenceCentresInteret),
        "competenceCertifications": competenceCertifications,
        "cpCertification":len(competenceCertifications),
        "competences":tabCompetences,
        "countcomp":countcomp,
        'domain':get_current_site(request).domain
    }
    template = get_template("cv/generatecv-1.html")
    html = template.render(context)
    options = {
        'page-size': 'Letter',
        'encoding': "UTF-8",
    }
    pdf = pdfkit.from_string(html, False, options)
    reponse = HttpResponse(pdf, content_type='application/pdf')
    reponse['Content-Disposition'] = f"attachment; filename=CV_{ user.last_name }_{ user.first_name }.pdf"
    return reponse

@login_required(login_url='connection/login')
def generatecv_2(request):
    #======== Parcours ===============
    parcours = Parcours.objects.filter(user_id=request.user.id).select_related('etablissement','annee','formation').order_by("-annee_id")
    #======== Competence ==============
    competenceLangues = []
    competenceLoisirs = []
    competenceCentresInteret = []
    competenceCertifications = []
    
    #======================= Expérience professionnelle=====================
    listexperiences = Experience.objects.filter(user_id=request.user.id, status=1).order_by("-date_debut")
    #On convertit le statut(une chaine de caratère) en dictionnaire
    experiences = []
    experiencesProjetP = []
    experiencesProjetA = []
    for experience in listexperiences:
        if experience.type_exp in ["Employé(e)","Stagiaire","Alternance"]:
            dic={}
            dic["experience"] = experience
            dic["taches"] = eval(experience.tache)
            experiences.append(dic)
        elif experience.type_exp == "Projet":
            dic={}
            dic["experience"] = experience
            dic["taches"] = eval(experience.tache)
            experiencesProjetP.append(dic)
        else:
            dic={}
            dic["experience"] = experience
            dic["taches"] = eval(experience.tache)
            experiencesProjetA.append(dic)
            
    user = User.objects.get(id=request.user.id)

    #======================= Référence ====================================
    references = Reference.objects.filter(user_id=request.user.id, status=1).select_related('entreprise')
    cpReference = Reference.objects.filter(user_id=request.user.id, status=1).count()

    #Recuperer le baccalaureat
    baccalaureat = Baccalaureat.objects.filter(user_id=request.user.id).first()

            
    type_competences = (
        TypeCompetence.objects
        .filter(user=request.user)
        .annotate(
            nb_competences=Count(
                'competence',
                filter=Q(competence__status=True) # Q permet d'ajouter une condition
            )
        )
        .filter(nb_competences__gt=0)
        .prefetch_related(
            Prefetch(
                'competence_set',
                queryset=Competence.objects.filter(status=True).order_by('name'),
            )
        )
        .order_by('name')
    )
    
    tabCompetences = []
    
    for t in type_competences:
        for competence in t.competence_set.all():
            if competence.status == 1:
                if t.name == "Langue":
                    competenceLangues.append(competence)
                elif t.name == "Loisir":
                    competenceLoisirs.append(competence)
                elif t.name == "Centres d'intérêt":
                    competenceCentresInteret.append(competence)
                elif t.name == "Certification":
                    competenceCertifications.append(competence)
                else:
                    tabCompetences.append(competence)
    
    context = {
        "user":user,
        "parcours":parcours,
        "experiences":experiences,
        "baccalaureat":baccalaureat,
        "experiencesProjetP":experiencesProjetP,
        "experiencesProjetA":experiencesProjetA,
        
        "type_competences": type_competences,
        "competences": tabCompetences,
        "competenceLangues":competenceLangues,
        "cpLangue":len(competenceLangues),
        "competenceLoisirs":competenceLoisirs,
        "cpLoisir":len(competenceLoisirs),
        "competenceCentresInteret": competenceCentresInteret,
        "cpCentresInteret": len(competenceCentresInteret),
        "competenceCertifications": competenceCertifications,
        "cpCertification": len(competenceCertifications),
        
        "references":references,
        "cpReference":cpReference,

    }
    template = get_template("cv/generatecv-2.html")
    html = template.render(context)
    options = {
        'page-size': 'Letter',
        'encoding': "UTF-8",
    }
    pdf = pdfkit.from_string(html, False, options)
    reponse = HttpResponse(pdf, content_type='application/pdf')
    reponse['Content-Disposition'] = f"attachment; filename=CV_{ user.last_name }_{ user.first_name }.pdf"
    return reponse

@login_required(login_url='connection/login')
def p_user(request, id):
    date = datetime.datetime.now()
    user_id = dechiffrer_param(str(id))
    #======== Parcours ===============
    parcours = Parcours.objects.filter(user_id=user_id).select_related('etablissement','annee','formation').order_by("-annee_id")
    #======== Competence ==============
    competenceLangues = []
    competenceLoisirs = []
    competenceCertifications = []
    
    #======================= Expérience professionnelle=====================
    listexperiences = Experience.objects.filter(user_id=user_id, status=1)
    #On convertit le statut(une chaine de caratère) en dictionnaire
    experiences = []
    experiencesProjetP = []
    experiencesProjetA = []
    for experience in listexperiences:
        if experience.type_exp in ["Employé(e)", "Stagiaire", "Alternance"]:
            dic={}
            dic["experience"] = experience
            dic["taches"] = eval(experience.tache)
            experiences.append(dic)
        elif experience.type_exp == "Projet":
            dic={}
            dic["experience"] = experience
            dic["taches"] = eval(experience.tache)
            dic_taches = eval(experience.tache)
            dic["dernieretache"] = dic_taches[len(dic_taches)-1]
            experiencesProjetP.append(dic)
        else:
            dic={}
            dic["experience"] = experience
            dic["taches"] = eval(experience.tache)
            dic_taches = eval(experience.tache)
            dic["dernieretache"] = dic_taches[len(dic_taches)-1]
            experiencesProjetA.append(dic)
            
    #======================= Référence ====================================
    references = Reference.objects.filter(user_id=user_id, status=1).select_related('entreprise')
    cpReference = Reference.objects.filter(user_id=user_id, status=1).count()

    #Recuperer le baccalaureat
    baccalaureat = Baccalaureat.objects.filter(user_id=user_id).first()

    #Récuperer l'user
    user = User.objects.get(id=user_id)
            
    type_competences = (
        TypeCompetence.objects
        .filter(user=request.user)
        .annotate(
            nb_competences=Count(
                'competence',
                filter=Q(competence__status=True) # Q permet d'ajouter une condition
            )
        )
        .filter(nb_competences__gt=0)
        .prefetch_related(
            Prefetch(
                'competence_set',
                queryset=Competence.objects.filter(status=True).order_by('name'),
            )
        )
        .order_by('name')
    )
    
    tabCompetences = []
    
    for t in type_competences:
        for competence in t.competence_set.all():
            if t.name == "Langue":
                competenceLangues.append(competence)
            elif t.name == "Loisir":
                competenceLoisirs.append(competence)
            elif t.name == "Certification":
                competenceCertifications.append(competence)
            else:
                tabCompetences.append(competence)
            
    
    context = {
        "user": user,
        "parcours": parcours,
        "experiences": experiences,
        "experiencesProjetP": experiencesProjetP,
        "experiencesProjetA": experiencesProjetA,
        "competenceLangues":competenceLangues,
        "cpLangue":len(competenceLangues),
        "competenceLoisirs":competenceLoisirs,
        "cpLoisir":len(competenceLoisirs),
        "competenceCertifications": competenceCertifications,
        "cpCertification": len(competenceCertifications),
        "references": references,
        "cpReference": cpReference,
        "baccalaureat": baccalaureat,
        "competences": tabCompetences,
        "type_competences": type_competences,

        "countanswer": nbnew_answer(request),
        "count": nbnew_message(request),
        "users": new_message(request),
        "parametre": parametre(),
        "date": date,

    }
    return render(request, "cv/profile_user.html", context)

@login_required(login_url='connection/login')
def profuser(request, id):
    date = datetime.datetime.now()
    user_id = dechiffrer_param(str(id))
    #======== Parcours ===============
    parcours = Parcours.objects.filter(user_id=user_id).select_related('etablissement','annee','formation').order_by("-annee_id")
    #======== Competence ==============
    competenceLangues = []
    competenceLoisirs = []
    competenceCertifications = []
    
    #======================= Expérience professionnelle=====================
    listexperiences = Experience.objects.filter(user_id=user_id, status=1)
    #On convertit le statut(une chaine de caratère) en dictionnaire
    experiences = []
    experiencesProjetP = []
    experiencesProjetA = []
    for experience in listexperiences:
        if experience.type_exp in ["Employé(e)", "Stagiaire", "Alternance"]:
            dic={}
            dic["experience"] = experience
            dic["taches"] = eval(experience.tache)
            experiences.append(dic)
        elif experience.type_exp == "Projet":
            dic={}
            dic["experience"] = experience
            dic["taches"] = eval(experience.tache)
            dic_taches = eval(experience.tache)
            dic["dernieretache"] = dic_taches[len(dic_taches)-1]
            experiencesProjetP.append(dic)
        else:
            dic={}
            dic["experience"] = experience
            dic["taches"] = eval(experience.tache)
            dic_taches = eval(experience.tache)
            dic["dernieretache"] = dic_taches[len(dic_taches)-1]
            experiencesProjetA.append(dic)
            
    #======================= Référence ====================================
    references = Reference.objects.filter(user_id=user_id, status=1).select_related('entreprise')
    cpReference = Reference.objects.filter(user_id=user_id, status=1).count()

    #Recuperer le baccalaureat
    baccalaureat = Baccalaureat.objects.filter(user_id=user_id).first()

    #Récuperer l'user
    user = User.objects.get(id=user_id)
            
    type_competences = (
        TypeCompetence.objects
        .filter(user=request.user)
        .annotate(
            nb_competences=Count(
                'competence',
                filter=Q(competence__status=True) # Q permet d'ajouter une condition
            )
        )
        .filter(nb_competences__gt=0)
        .prefetch_related(
            Prefetch(
                'competence_set',
                queryset=Competence.objects.filter(status=True).order_by('name'),
            )
        )
        .order_by('name')
    )
    
    tabCompetences = []
    
    for t in type_competences:
        for competence in t.competence_set.all():
            if t.name == "Langue":
                competenceLangues.append(competence)
            elif t.name == "Loisir":
                competenceLoisirs.append(competence)
            elif t.name == "Certification":
                competenceCertifications.append(competence)
            else:
                tabCompetences.append(competence)
            
    
    context = {
        "user": user,
        "parcours": parcours,
        "experiences": experiences,
        "experiencesProjetP": experiencesProjetP,
        "experiencesProjetA": experiencesProjetA,
        "competenceLangues":competenceLangues,
        "cpLangue":len(competenceLangues),
        "competenceLoisirs":competenceLoisirs,
        "cpLoisir":len(competenceLoisirs),
        "competenceCertifications": competenceCertifications,
        "cpCertification": len(competenceCertifications),
        "references": references,
        "cpReference": cpReference,
        "baccalaureat": baccalaureat,
        "competences": tabCompetences,
        "type_competences": type_competences,

        "countanswer": nbnew_answer(request),
        "count": nbnew_message(request),
        "users": new_message(request),
        "parametre": parametre(),
        "date": date,

    }
    return render(request, "cv/profuser.html", context)
    
@login_required(login_url='connection/login')
@allowed_users(allowed_roles=['admin'])
def del_membre(request,id):
    try:
        user = User.objects.get(id=id)
    except:
        user = None
    if user:
        user.delete()
    return redirect("home")


def count_new_chat(request):
    # Compter le nombre de nouveaux chats non lus
    countnewchat = MessageStatus.objects.filter(user_id=request.user.id, read=0).count()
    #Compter le nombre de toutes les questions qui ont été posées après la dernière connexion du membre
    questions = Question.objects.filter(date__gt=request.user.last_login)
    countquestion = 0
    for question in questions:
        if question.user_id != request.user.id:
            countquestion += 1
    #Compter le nombre de nouveaux contacts
    nombre_contacts = Contact.objects.filter(statut=0,status=0).count()
    
    #Compter le nombre de signalement des question et réponse du forum
    countreportquestion = SignalerQuestion.objects.all().count()
    countreportanswer = SignalerAnswer.objects.all().count()
    countreport = countreportanswer + countreportquestion
    
    #Nombre des utilisateurs actuellement connectés
    countuseractive = get_online_users().count()
    users = get_online_users()
    
    #Sérialiser une liste d'objets utilisateur (users) en JSON
    users_online = serializers.serialize('json', users, fields=('first_name', 'last_name'))
    
    #Nombre de demande de suppression de compte d'utilisateur
    countdmddeleteaccount = Profile.objects.filter(status_deleteaccount=1).count()
    return JsonResponse({
        'countnewchat':countnewchat, 
        'countquestion':countquestion,
        'countnewcontact':nombre_contacts,
        'countreport':countreport,
        'countuseractive':countuseractive,
        'users_online':users_online,
        'countdmddeleteaccount':countdmddeleteaccount
    })
    
def fresh_header(request):
        
    data = {
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request)
    }
    return JsonResponse(data)
