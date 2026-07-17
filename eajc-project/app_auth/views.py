# Importation des modules tiers
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.db.models import Count
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.views import View
from django.db import transaction
from django.http import JsonResponse
# Importation des modules locaux
from .forms import*
from eab.utils import send_email_with_html_body
from eab.views import nbnew_answer, nbnew_message, new_message, parametre
from eajc.utils.crypto import dechiffrer_param, chiffrer_param
from eab.models import*
from forum.models import*
from .decorator import*
from .tokens import account_activation_token
# Importation des modules standards
import datetime
import bleach
import os
import re
import base64

def userPriority():
    users = User.objects.all()
    #Memebre prioritaire
    tabUserPriority = []
    count = 0
    for user in users:
        try:
            if user.profile and user.profile.priority==1:
                if count <=2:
                    tabUserPriority.append(user)
                    count += 1
        except:
            pass
    return tabUserPriority

#Activation du compte
def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Activation effectuée avec succès. Vous pouvez alors vous connecter.")
        return redirect("connection/connexion")
    else:
         messages.error(request, "Le lien d'activation est invalide")

    return redirect("connection/connexion")


# Méthode de création des groupes
def create_default_group(request):
    types = ["admin", "customer", "Sup admin"]

    for name in types:
        if not Group.objects.filter(name=name).exists():
            group = Group(name=name)
            group.save()

#=========== Gestion des groupes ======================
@login_required(login_url='connection/login')
@allowed_users(allowed_roles=['admin'])
def groupes(request):
    date = datetime.datetime.now()
    groupes = Group.objects.all()
    context={
        "groupes":groupes,
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request),
        "parametre":parametre(),
        "date":date
    }
    return render(request, "group/groups.html", context)


@login_required(login_url='connection/login')
@allowed_users(allowed_roles=['admin'])
def add_user_group(request,id):
    date = datetime.datetime.now()
    user = User.objects.get(id=id)
    groups = Group.objects.all()
    context={
        "groups":groups,
        "user":user,
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request),
        "parametre":parametre(),
        "date":date
    }
    return render(request, "users/add_user_group.html", context)

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=['admin'])
def  add_ug(request):
    if request.method == "POST":
        id = request.POST["id"]
        name = request.POST["name"]
        user = User.objects.get(id=id)
        group = Group.objects.get(name=name)
        # Associer un utilisateur à un groupe
        user.groups.add(group)
        if user.groups.exists():
            return JsonResponse({'status':'Save'})
        else:
            return JsonResponse({'status':2})

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=['admin'])
def user_groups(request, id):
    date = datetime.datetime.now()
    
    user_id = dechiffrer_param(str(id))
    user = User.objects.get(id=user_id)
    groups = Group.objects.all()
    tabGroup = []
    for g in user.groups.all():
        tabGroup.append(g)
    context = {
        "user":user,
        "groups":groups,
        "tabGroup":tabGroup,
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request),
        "parametre":parametre(),
        "date":date
    }
    return render(request, "users/user_group.html", context)

def ajax_delete_user_group(request, id, name):
    user = User.objects.get(id=id)
    context = {
        "user": user,
        "name": name
    }
    return render(request, "ajax_delete_user_group.html", context) 

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=['admin'])
def add_user_to_group(request):
    
    if request.method == "POST":
        id = request.POST["id"]
        name = request.POST["name"]
        group = Group.objects.get(name=name)
        user = User.objects.get(id=id)
        # Supprimer les groupes actuels de l'utilisateur
        user.groups.clear()
        # Ajouter le nouveau groupe à l'utilisateur
        user.groups.add(group)

        return redirect("users/user_groups", id=chiffrer_param(str(id)))

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=['admin'])
def del_user_to_group(request, id, name):
    user_id = dechiffrer_param(str(id))
    group_name = dechiffrer_param(str(name))
    group = Group.objects.get(name=group_name)
    user = User.objects.get(id=user_id)
    
    groups = Group.objects.all()
    tabGroup = []
    for g in user.groups.all():
        tabGroup.append(g)
    if len(tabGroup) > 1:
        user.groups.remove(group)

    return redirect("users/user_groups", id=id)
    
def ajax_delete_group(request, id):
    group = Group.objects.get(id=id)
    context = {
        "group": group
    }
    return render(request, "ajax_delete_group.html", context)   

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=['admin'])
def del_group(request,id):
    try:
        group_id = dechiffrer_param(str(id))
        group = Group.objects.get(id=group_id)
    except:
        group = None
        
    if group:
        group.delete()
    return redirect("group/groups")

@transaction.atomic
def register(request):
    date = datetime.datetime.now()
    form = UserForm()

    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            #On verifie si l'adresse e-mail correspond bien
            regexp = r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$"
            if not re.search(regexp, email):
                messages.error(request, "Le format de l'adresse e-mail ne correspond pas.")
            else:
                query = User.objects.filter(email=email)
                if query.exists():
                    messages.error(request, "L'adresse e-mail renseignée existe déjà.") 
                else:
                    count0 = User.objects.all().count()
                    user = form.save() 
                    
                    group = Group.objects.get(name="customer")
                    user.groups.add(group)
                    #On desactive l'accès du membre
                    user.is_active = False
                    user.save()
                    #On recupere nombre total des membres après la création du compte
                    count1 = User.objects.all().count()
                    #On envoie l'e-mail au membre pour activer son compte
                    subject = "Activation de compte"
                    template = "email/emailactivation.html"
                    receivers = [email]
                    
                    # Chemin vers le fichier logo local
                    """with open(parametre().logo, "rb") as image_file:
                        logo_base64 = base64.b64encode(image_file.read()).decode('utf-8')"""
                    
                    context = {
                            'domain':get_current_site(request).domain,
                            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                            'token':account_activation_token.make_token(user),
                            'protocol': 'https' if request.is_secure() else 'http',
                            'user':user,
                            "countanswer":nbnew_answer(request),
                            "count":nbnew_message(request),
                            "users":new_message(request),
                            "parametre":parametre(),
                            "date":date
                    }
                    has_send = send_email_with_html_body(
                        subjet = subject,
                        receivers = receivers,
                        template = template,
                        context = context
                    )
                    
                    if count0 < count1 and has_send == True:
                        return redirect("users/success-account",id=user.id)
                    else:
                        messages.error(request, "Inscription a échouée.")
                        context={
                            "form":form,
                            "userpriorities":userPriority(),
                            "parametre":parametre()
                        }
                        return render(request, "users/register.html", context) 
        else:
            messages.error(request, form.errors)
            context = {
                "form":form,
                "userpriorities":userPriority(),
                "parametre":parametre()
            }
            return render(request, "users/register.html", context)

    context = {"form":form,"userpriorities":userPriority(),"parametre":parametre,"date":date}
    return render(request, "users/register.html", context)

def success_account(request, id):
    date = datetime.datetime.now()
    user = User.objects.get(id=id)
    context = {
        "user":user,
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request),
        "parametre":parametre(),
        "date":date
    }
    return render(request,"users/success-account.html", context)

def login_user(request):
    #Destruction de la session
    logout(request)
    date = datetime.datetime.now()
    
    if request.method == "POST":
        # Création des groupes s'ils n'existent pas
        create_default_group(request)
        
        form = LoginForm(request.POST)
        if form.is_valid():
            username = bleach.clean(form.cleaned_data["username"].strip())
            password = bleach.clean(form.cleaned_data["password"].strip())
            user = authenticate(username=username, password=password)
            if user is not None:
                group = user.groups.all()
                for g in group:    
                    if g.name == "admin":
                        if user.is_staff:
                            login(request, user)
                            return redirect("dashboard")
                        else:
                            messages.error(request, "Vous n'avez pas de permission")
                            return render(request, "connection/login.html", {"form":form,"parametre":parametre(),"date":date})

            messages.error(request, "Erreur d'authentification")
            return render(request, "connection/login.html", {"form":form,"parametre":parametre(),"date":date})
        else:
            for field in form.errors:
                form[field].field.widget.attrs['class']+='is-invalid'
            return render(request, "connection/login.html", {"form":form,"parametre":parametre(),"date":date})
    else:
        form = LoginForm()
        return render(request, "connection/login.html",{"form":form,"parametre":parametre(),"date":date})

def login_customer(request):
    #Destruction de la session
    logout(request)
    date = datetime.datetime.now()
    if request.method == "POST":
        # Création des groupes s'ils n'existent pas
        create_default_group(request)
        form = LoginForm(request.POST)
        context = {
            "form":form,
            "userpriorities":userPriority(),
            "parametre":parametre(),
            "date":date
        }
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                group = user.groups.all()
                for g in group:    
                    if g.name == "customer":
                        login(request, user)
                        return redirect("dashboard")
               
            messages.error(request, "Erreur d'authentification")
            return render(request, "connection/connexion.html", context)
        else:
            for field in form.errors:
                form[field].field.widget.attrs['class']+='is-invalid'
            return render(request, "connection/connexion.html", context)
    else:
        form = LoginForm()
        context = {
            "form":form,
            "userpriorities":userPriority(),
            "countanswer":nbnew_answer(request),
            "count":nbnew_message(request),
            "users":new_message(request),
            "parametre":parametre(),
            "date":date
        }
        return render(request, "connection/connexion.html",context)

 
@login_required(login_url='connection/login')
@allowed_users(allowed_roles=['admin'])
def users(request):
    date = datetime.datetime.now()

    tabusers = []
    users = User.objects.all()
    for user in users:
        if user.groups.exists():
            group = user.groups.all()[0].name
            if group == "admin":
                tabusers.append(user)
    context = {
        "tabusers":tabusers,
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request),
        "parametre":parametre(),
        "date":date
        
    }
    return render(request, "users/users.html", context)

def ajax_delete_user(request, id):
    user = User.objects.get(id=id)
    context = {
        "user": user
    }
    return render(request, "ajax_delete_user.html", context)

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=['admin'])
def detail_user(request,id):
    date = datetime.datetime.now()
    user_id = dechiffrer_param(str(id))
    user = User.objects.get(id=user_id)
    context = {
        "user":user,
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request),
        "parametre":parametre(),
        "date":date
    }
    return render(request, "users/detail_user.html", context)

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=['admin'])
def del_user(request,id):
    try:
        user_id = dechiffrer_param(str(id))
        user = User.objects.get(id=user_id)
    except:
        user = None
        
    if user:
        if Profile.objects.filter(user = user).exists():
            # Vérifier si l'utilisateur a une photo associée et que le fichier existe réellement
            if user.profile.photo and hasattr(user.profile.photo, 'path'):
                photo_path = user.profile.photo.path
                # Verifier l'existence du fichier
                if os.path.exists(photo_path):
                    os.remove(photo_path)    
        user.delete()
    return redirect("users/users")

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=['admin'])
def customers(request):
    date = datetime.datetime.now()

    tabusers = []
    users = User.objects.all()
    for user in users:
        if user.groups.exists():
            group = user.groups.all()[0].name
            if group == "customer":
                tabusers.append(user)
    context = {
        "tabusers":tabusers,
        "date":date,
        "parametre":parametre(),
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request)
    }
    return render(request, "users/customers.html", context)

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=['admin'])
def details_cus(request,id):
    date = datetime.datetime.now()
    user_id = dechiffrer_param(str(id))
    user = User.objects.get(id=user_id)
    context = {
        "user":user,
        "date":date,
        "parametre":parametre(),
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request)
    }
    return render(request, "users/details_cus.html", context)

def ajax_delete_customer(request, id):
    user = User.objects.get(id=id)
    context = {
        "user": user
    }
    return render(request, "ajax_delete_customer.html", context)

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=['admin'])
def del_customer(request,id):
    try:
        user_id = dechiffrer_param(str(id))
        user = User.objects.get(id=user_id)
    except:
        user = None
    
    if user:
        if Profile.objects.filter(user = user).exists():
            # Vérifier si l'utilisateur a une photo associée et que le fichier existe réellement
            if user.profile.photo and hasattr(user.profile.photo, 'path'):
                photo_path = user.profile.photo.path
                # Verifier l'existence du fichier
                if os.path.exists(photo_path):
                    os.remove(photo_path)    
        user.delete()
    return redirect("users/customers")

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=['admin'])
def delaccount_user(request,id):
    try:
        user = User.objects.get(id=id)
    except:
        user = None
        
    if user:
        if Profile.objects.filter(user = user).exists():
            # Vérifier si l'utilisateur a une photo associée et que le fichier existe réellement
            if user.profile.photo and hasattr(user.profile.photo, 'path'):
                photo_path = user.profile.photo.path
                # Verifier l'existence du fichier
                if os.path.exists(photo_path):
                    os.remove(photo_path)    
        user.delete()
    return redirect("users/users")

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=['admin'])
def members(request):
    date = datetime.datetime.now()
    users = User.objects.all()

    paginator = Paginator(users, 10)
    num_page=request.GET.get('page')
    try:
        users = paginator.get_page(num_page)
    except PageNotAnInteger:
        users = paginator.get_page(1)
    except EmptyPage:
        users = paginator.get_page(paginator.num_page)
        
    context = {
        "members":users,
        "date":date,
        "parametre":parametre(),
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request)
    }
    return render(request, "users/members.html", context)

@login_required(login_url='connection/login')
def profile(request):
    date = datetime.datetime.now()
    try:
        profile = Profile.objects.get(user=request.user)
    except Exception as e:
        profile = None

    if request.method == "POST":
        
        if profile:
            photo = None
            if request.POST.get('photo', True):
                photo = request.FILES["photo"]
            if photo is not None :
                # Vérifier si l'utilisateur a une photo associée et que le fichier existe réellement
                if profile.photo and hasattr(profile.photo, 'path'):
                    photo_path = profile.photo.path  # Récupérer le chemin de la photo

                    if os.path.exists(photo_path):  # Vérifier si le fichier existe
                        os.remove(photo_path)  # Supprimer le fichier  
                    profile.photo = photo
                    profile.save() 
                else:
                    profile.photo = photo
                    profile.save()           
            return redirect("users/profile")
        else:
            messages.error(request, "Commencez par mettre à jour votre profil, puis vous pourrez ajouter une photo.")
    
    context = {
        "profile":profile,
        "date":date,
        "parametre":parametre(),
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request)
    }
    return render(request,"users/profile.html",context)

@login_required(login_url='connection/login')
@transaction.atomic
def edit_profile(request):
    date = datetime.datetime.now()
    try:
        profile = Profile.objects.get(user=request.user)
    except Exception as e:
        profile = None
     
    if request.method == "POST":
        #On verifie si le profile n'existe pour le créer sinon on le modifie.
        if profile == None:
            nom = bleach.clean(request.POST["nom"].strip())
            prenom = bleach.clean(request.POST["prenom"].strip())
            gender = bleach.clean(request.POST["gender"].strip())
            email = request.POST["email"].strip()
            adresse = bleach.clean(request.POST["adresse"].strip())
            phone = bleach.clean(request.POST["phone"].strip())
            profession = bleach.clean(request.POST["profession"].strip())
            country = bleach.clean(request.POST["country"].strip())
            linkedin = bleach.clean(request.POST["linkedin"].strip())
            portfolio = bleach.clean(request.POST["portfolio"].strip())
            github = bleach.clean(request.POST["github"].strip())

            request.user.last_name = nom
            request.user.first_name = prenom
            request.user.email = email

            with transaction.atomic():
                request.user.save()
                profil = Profile(
                    phone=phone, 
                    address=adresse, 
                    user=request.user, 
                    gender=gender,
                    profession=profession,
                    country=country,
                    linkedin=linkedin,
                    portfolio=portfolio,
                    github=github)
                profil.save()
                return redirect("users/profile")
        else:
            nom = bleach.clean(request.POST["nom"].strip())
            prenom = bleach.clean(request.POST["prenom"].strip())
            gender = bleach.clean(request.POST["gender"].strip())
            email = request.POST["email"].strip()
            adresse = bleach.clean(request.POST["adresse"].strip())
            phone = bleach.clean(request.POST["phone"].strip())
            profession = bleach.clean(request.POST["profession"].strip())
            country = bleach.clean(request.POST["country"].strip())
            linkedin = bleach.clean(request.POST["linkedin"].strip())
            portfolio = bleach.clean(request.POST["portfolio"].strip())
            github = bleach.clean(request.POST["github"].strip())

            user = profile.user
            user.last_name = nom
            user.first_name = prenom
            user.email = email
            # Utiliser la transaction pour valider que si toutes les opérations ont été bien effectuées
            with transaction.atomic():
                user.save()
                profile.gender = gender
                profile.phone = phone
                profile.address = adresse
                profile.profession = profession
                profile.country = country
                profile.linkedin = linkedin
                profile.portfolio = portfolio
                profile.portfolio = github
                profile.save()
                return redirect("users/profile")
            
    countries = [
                'Afrique du Sud',
                'Afghanistan',
                'Albanie',
                'Allemagne',
                'Andorre',
                'Angola',
                'Antigua-et-Barbuda',
                'Arabie Saoudite',
                'Argentine',
                'Arménie',
                'Australie',
                'Autriche',
                'Azerbaïdjan',
                'Bahamas',
                'Bahreïn',
                'Bangladesh',
                'Barbade',
                'Belgique',
                'Belize',
                'Bénin',
                'Bhoutan',
                'Biélorussie',
                'Birmanie',
                'Bolivie',
                'Bosnie-Herzégovine',
                'Botswana',
                'Brésil',
                'Brunei',
                'Bulgarie',
                'Burkina Faso',
                'Burundi',
                'Cambodge',
                'Cameroun',
                'Canada',
                'Cap-Vert',
                'Chili',
                'Chine',
                'Chypre',
                'Colombie',
                'Comores',
                'Congo-Brazzaville',
                'Corée du Nord',
                'Corée du Sud',
                'Costa Rica	San',
                'Côte d’Ivoire',
                'Croatie',
                'Cuba',
                'Danemark',
                'Djibouti',
                'Dominique',
                'Égypte',
                'Émirats arabes unis',
                'Équateur',
                'Érythrée',
                'Espagne',
                'Eswatini',
                'Estonie',
                'États-Unis',
                'Éthiopie',
                'Fidji',
                'Finlande',
                'France',
                'Gabon',
                'Gambie',
                'Géorgie',
                'Ghana',
                'Grèce',
                'Grenade',
                'Guatemala',
                'Guinée',
                'Guinée équatoriale',
                'Guinée-Bissau',
                'Guyana',
                'Haïti',
                'Honduras',
                'Hongrie',
                'Îles Cook',
                'Îles Marshall',
                'Inde',
                'Indonésie',
                'Irak',
                'Iran',
                'Irlande',
                'Islande',
                'Israël',
                'Italie',
                'Jamaïque',
                'Japon',
                'Jordanie',
                'Kazakhstan',
                'Kenya',
                'Kirghizistan',
                'Kiribati',
                'Koweït',
                'Laos',
                'Lesotho',
                'Lettonie',
                'Liban',
                'Liberia',
                'Libye',
                'Liechtenstein',
                'Lituanie',
                'Luxembourg',
                'Macédoine',
                'Madagascar',
                'Malaisie',
                'Malawi',
                'Maldives',
                'Mali',
                'Malte',
                'Maroc',
                'Maurice',
                'Mauritanie',
                'Mexique',
                'Micronésie',
                'Moldavie',
                'Monaco',
                'Mongolie',
                'Monténégro',
                'Mozambique',
                'Namibie',
                'Nauru',
                'Népal',
                'Nicaragua',
                'Niger',
                'Nigeria',
                'Niue',
                'Norvège',
                'Nouvelle-Zélande',
                'Oman',
                'Ouganda',
                'Ouzbékistan',
                'Pakistan',
                'Palaos',
                'Palestine',
                'Panama',
                'Papouasie-Nouvelle-Guinée',
                'Paraguay',
                'Pays-Bas',
                'Pérou',
                'Philippines',
                'Pologne',
                'Portugal',
                'Qatar',
                'République centrafricaine',
                'République démocratique du Congo',
                'République Dominicaine',
                'République tchèque',
                'Roumanie',
                'Royaume-Uni',
                'Russie',
                'Rwanda',
                'Saint-Kitts-et-Nevis',
                'Saint-Vincent-et-les-Grenadines',
                'Sainte-Lucie',
                'Saint-Marin',
                'Salomon',
                'Salvador',
                'Samoa',
                'São Tomé-et-Principe',
                'Sénégal',
                'Serbie',
                'Seychelles',
                'Sierra Leone',
                'Singapour',
                'Slovaquie',
                'Slovénie',
                'Somalie',
                'Soudan',
                'Soudan du Sud',
                'Sri Lanka',
                'Suède',
                'Suisse',
                'Suriname',
                'Syrie',
                'Tadjikistan',
                'Tanzanie',
                'Tchad',
                'Thaïlande',
                'Timor oriental',
                'Togo',
                'Tonga',
                'Trinité-et-Tobago',
                'Tunisie',
                'Turkménistan',
                'Turquie',
                'Tuvalu',
                'Ukraine',
                'Uruguay',
                'Vanuatu',
                'Vatican',
                'Venezuela',
                'Viêt Nam',
                'Yémen',
                'Zambie',
                'Zimbabwe'
    ]

    context = {
        "countries":countries,
        "profile":profile,
        "date":date,
        "parametre":parametre(),
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request)
    }
    return render(request, "users/edit_profile.html", context)


def demande_delete_account(request):
    
    try:
        profile = Profile.objects.get(user=request.user)
    except Exception as e:
        profile = None
    
    if profile:
        if request.method == "POST":
            just_costumer = bleach.clean(request.POST["just_costumer"].strip())
            
            profile.just_costumer = just_costumer
            profile.status_deleteaccount = 1
            
            profile.save()
            
            return JsonResponse({'status':'Save'})
    else:
        return JsonResponse({"status":0})
        
def answer_del_account(request, id):
    date = datetime.datetime.now()
    user = User.objects.get(id=id)
    context = {
        "user":user,
        "date":date,
        "parametre":parametre(),
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request)
    }
    return render(request, "users/answer_del_account.html", context)   


@login_required(login_url='connection/login')
@allowed_users(allowed_roles=['admin'])
@transaction.atomic
@csrf_exempt
def answer_delete_account(request):
    if request.method == "POST":
        id = request.POST["user"]
        subject = bleach.clean(request.POST["subject"].strip())
        content = bleach.clean(request.POST["content"].strip())
        dic = {}
        #Idendifiant du recepteur
        dic["user1"] = int(id)
        #Identifiant de l'emeteur
        dic["user2"] = request.user.id

        contact = Contact(
            name = "",
            email = "",
            subject = subject,
            statut = 0,
            status = 1,
            message = content,
            codes = dic
        )
        count0 = Contact.objects.all().count()
        contact.save()
        count1 = Contact.objects.all().count()
        if count0 < count1:
            #Mise à jour du profile
            try:
                #Recuperer l'utilisateur
                user = User.objects.get(id=id)
                profile = Profile.objects.get(user=user)
            except Exception as e:
                profile=None
            if profile:
                profile.status_deleteaccount = 0
                profile.just_costumer = ""
                
                profile.save()
            return JsonResponse({'status':"Save"})
        else:
            return JsonResponse({'status':0})
    

@login_required(login_url='connection/login')
@transaction.atomic
def configuration(request):
    date = datetime.datetime.now()

    try:
        profile=Profile.objects.get(user=request.user)
    except Exception as e:
        profile = None
     
    if request.method == "POST":
        droitmes = request.POST.get("droitmes")
        status = request.POST.get("status")
        vp = request.POST.get("vp")
        apropos = bleach.clean(request.POST["apropos"].strip())
        nature_recherche = bleach.clean(request.POST["nature_recherche"].strip())
        formation = request.POST["formation"]
        competence = request.POST["competence"]
        experience = request.POST["experience"]
        reference = request.POST["reference"]
        autre = request.POST["autre"]
        #On verifie si le profil n'existe pas pour le créer sinon on le modifie.
        if profile == None:
            profil = Profile(
                phone="", 
                address="", 
                user=request.user, 
                gender="",
                apropos=apropos,
                nature_recherche=nature_recherche,
                droitmes=droitmes,
                status=status,
                vp=vp,
                vaform=autre,
                vcom=competence,
                vep=experience,
                vform=formation,
                vref=reference
            )
            profil.save()
            messages.success(request, "Configuration modifiée avec succès.")
            return redirect("users/configuration")
        else:
            profile.droitmes = droitmes
            profile.status = status
            profile.vp = vp
            profile.apropos = apropos
            profile.nature_recherche=nature_recherche
            profile.vform = formation
            profile.vcomp = competence
            profile.vep = experience
            profile.vaform = autre
            profile.save()
            messages.success(request, "Configuration modifiée avec succès.")
            return redirect("users/configuration")

    context={
        "profile":profile,
        "date":date,
        "parametre":parametre(),
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request)
    }
    return render(request, "users/configuration.html", context)

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=['admin'])
def upd_access(request, id):
    date=datetime.datetime.now()

    user = User.objects.get(id=id)
    if request.method == "POST":
        if user.is_staff == 1:
            user.is_staff = 0
            user.save()
            return redirect("users/users")
        else:
            user.is_staff = 1
            user.save()
            return redirect("users/users")
    context = {
        "user":user,
        "date":date,
        "parametre":parametre(),
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request)
    }
    return render(request, "users/upd_access.html",context)

def logout_user(request):
    group = request.user.groups.all()
    for g in group:    
        if g.name == "admin":
            logout(request)
            for key in request.session.keys():
                del request.session[key]
            return redirect("connection/login")
        else:
            logout(request)
            for key in request.session.keys():
                del request.session[key]
            return redirect("connection/connexion")

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=['admin'])        
def user_dmd_delete_account(request):
    date = datetime.datetime.now()
    profil = Profile.objects.filter(status_deleteaccount=1)
    context = {
        "profil":profil,
        "date":date,
        "parametre":parametre(),
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request)
    }
    return render(request, "users/useraskdeleteaccount.html", context)

@login_required(login_url='connection/login')
@allowed_users(allowed_roles=['admin'])
def param(request):
    if request.method == "POST":
        id = request.POST["id"]
        if id != "":
            param = Parametre.objects.get(id=id)
            appname = bleach.clean(request.POST["appname"].strip())
            appeditor = bleach.clean(request.POST["appeditor"].strip())
            version = bleach.clean(request.POST["version"].strip())
            theme = request.POST["theme"].strip()
            devise = request.POST["devise"]
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

                param.appname = appname
                param.appeditor = appeditor
                param.version = version
                param.theme = theme
                param.devise = devise
                param.email = email
                param.phone = phone
                if logo is not None:
                    param.logo = logo
                param.width_logo = width
                param.height_logo = height

                param.save()
                messages.success(request, "Paramètre modifié avec succès.")
                return redirect("parametre")
        else:
            appname = bleach.clean(request.POST["appname"].strip())
            appeditor = bleach.clean(request.POST["appeditor"].strip())
            version = bleach.clean(request.POST["version"].strip())
            theme = request.POST["theme"]
            devise = bleach.clean(request.POST["devise"].strip())
            email = request.POST["email"]
            phone = bleach.clean(request.POST["phone"].strip())
            logo = request.FILES["logo"]
            width = bleach.clean(request.POST["width"].strip())
            height = bleach.clean(request.POST["height"].strip())

            param = Parametre(
                appname = appname,
                appeditor = appeditor,
                version = version,
                theme = theme,
                devise = devise,
                email = email,
                phone = phone,
                logo = logo,
                width_logo = width,
                height_logo = height)
            param.save()
            messages.success(request, "Paramètre modifié avec succès.")
            return redirect("parametre")

    date = datetime.datetime.now()

    context = {
        "date":date,
        "parametre":parametre(),
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request)
    }
    return render(request, "parametre.html",context)

class priority(View):
    def get(self, request, id, *args, **kwargs):
        user = User.objects.get(id=id)
        profile = Profile.objects.get(user=user)
        if profile.priority == 0:
            profile.priority = 1
        else:
            profile.priority = 0
        profile.save()

        if profile.priority == 1:
            return JsonResponse({'status':1})
        else:
            return JsonResponse({'status':0})

def m_countries(request):
    date = datetime.datetime.now()
    #Liste des pays des membres
    countries = Profile.objects.values("country").annotate(effectif=Count("country")).order_by("-effectif")
    id = 0
    tabCountries = []
    for c in countries:
        profils = Profile.objects.filter(country=c["country"])
        id += 1
        dic = {}
        dic["id"] = id
        dic["country"] = c
        dic["profils"] = profils
        tabCountries.append(dic)

    paginator = Paginator(countries, 12)
    num_page = request.GET.get('page')
    countries = paginator.get_page(num_page)
    context = {
        "tabCountries":tabCountries,
        "countries":countries,
        "date":date,
        "parametre":parametre(),
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request)
    }
    return render(request, "users/m-countries.html", context)

        
