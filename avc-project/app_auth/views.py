# Importation des modules standards
import re
import os
import bleach
# Importation des modules tiers
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.decorators import login_required 
from eajcprojet.utils.crypto import dechiffrer_param
from django.db import transaction
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy


# Importation des modules locaux
from eajc.views import get_setting 
from .tokens import account_activation_token
from .utils import send_email_with_html_body
#from .decorator import*
from .models import *
from .forms import *
from eajc.views import get_setting 

@transaction.atomic
def register(request):
    
    setting = get_setting()
    if setting is None:
        redirect("settings/maintenance")
  
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
                    
                    """group = Group.objects.get(name="customer")
                    user.groups.add(group)"""
                    #On desactive l'accès du membre
                    user.is_active = False
                    user.save()
                    #On recupere nombre total des membres après la création du compte
                    count1 = User.objects.all().count()
                    #On envoie l'e-mail au membre pour activer son compte
                    subject = "Activation de compte"
                    template = "email/emailactivation.html"
                    receivers = [email]
                    
                    context = {
                        "domain":get_current_site(request).domain,
                        "uid":urlsafe_base64_encode(force_bytes(user.pk)),
                        "token":account_activation_token.make_token(user),
                        "protocol": 'https' if request.is_secure() else 'http',
                        "user":user,
                        "setting":setting,
                    }
                    has_send = send_email_with_html_body(
                        subjet = subject,
                        receivers = receivers,
                        template = template,
                        context = context
                    )
                    
                    if count0 < count1 and has_send == True:
                        return redirect("user/success-account", id=user.id)
                    else:
                        messages.error(request, "Inscription a échouée.")
                        context = {
                            "form": form,
                            "setting": setting
                        }
                        return render(request, "user/register.html", context) 
        else:
            # Personnalisation des erreurs
            for field, errors in form.errors.items():
                for error in errors:
                    # Si l'erreur concerne les mots de passe, afficher un message générique
                    if "Les deux mots de passe ne correspondent pas" in error:
                        messages.error(request, "Les deux mots de passe ne correspondent pas.")
                    else:
                        messages.error(request, error)
            context = {
                "form": form,
                "setting": setting
            }
            return render(request, "user/register.html", context)

    context = {
        "form": form,
        "setting": setting
    }
    return render(request, "user/register.html", context)

def success_account(request, id):
    setting = get_setting()
    if setting is None:
        redirect("settings/maintenance")
    else:
        try:
            user = User.objects.get(id=id)
        except:
            user = None
            
        if user:
            context = {
                "user": user,
                "setting": setting
            }
            return render(request, "user/success-account.html", context)
        else:
            return redirect("user/register")
    
#Activation du compte
def activate(request, uidb64, token):
    
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Activation effectuée avec succès. Vous pouvez alors vous connecter.")
        return redirect("connection/login")
    else:
         messages.error(request, "Le lien d'activation est invalide")

    return redirect("connection/login")

def login_user(request):
    setting = get_setting()
    if setting is None:
        redirect("settings/maintenance")
        
    #Destruction de toutes les sessions
    logout(request)
    request.session.clear()

    if request.method == "POST":
        form = LoginForm(request.POST)
        # Verifier la validité du formulaire
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                #Création des sessions
                login(request, user)
                #if user.is_superuser:
                return redirect("index")
                

            context = {
                "form": form,
                "setting": setting
            }
            messages.error(request, "Erreur d'authentification")
            return render(request, "connection/login.html", context)
        else:
            for field in form.errors:
                form[field].field.widget.attrs['class']+='is-invalid'
            
            context = {
                "form": form,
                "setting": setting
            }
            return render(request, "connection/login.html", context)
    else:
        form = LoginForm()
        context = {
            "form": form,
            "setting": setting
        }
        return render(request, "connection/login.html", context)
    
def logout_user(request):
    logout(request)
    return redirect("connection/login")


@login_required(login_url='connection/login')
def users(request):
    
    setting = get_setting()
    if setting is None:
        return redirect("settings/maintenance")
    else:
        users = User.objects.all()
        
        context = {
            "setting": setting,
            "users": users,
        }
        return render(request, "user/users.html", context)
    
def ajax_detail_user(request,id):
    user = User.objects.get(id=id)
    context = {
        "user": user
    }
    return render(request, "ajax_detail_user.html", context)
    
@login_required(login_url='connection/login')
@transaction.atomic
def profile(request):
    user = request.user
    setting = get_setting()
    if setting is None:
        return redirect("settings/maintenance")
    
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
            return redirect("user/profile")
        else:
            messages.error(request, "Commencez par mettre à jour votre profil, puis vous pourrez ajouter une photo.")
        
    context = {
        "setting": setting,
        "user": user,
        "profile": profile
    }
    return render(request, "user/profile.html", context)
        
    

@login_required(login_url='connection/login')
@transaction.atomic
def edit_profile(request):
    setting = get_setting()
    if setting is None:
        return redirect("settings/maintenance")
    
    try:
        profile = Profile.objects.get(user=request.user)
    except Exception as e:
        profile = None
     
    if request.method == "POST":
        #On verifie si le profile n'existe pour le créer sinon on le modifie.
        if profile == None:
            last_name = bleach.clean(request.POST["last_name"].strip())
            first_name = bleach.clean(request.POST["first_name"].strip())
            gender = request.POST["gender"]
            email = request.POST["email"]
            address = bleach.clean(request.POST["address"].strip())
            phone = bleach.clean(request.POST["phone"].strip())
            profession = bleach.clean(request.POST["profession"].strip())
            country = request.POST["country"]

            request.user.last_name = last_name
            request.user.first_name = first_name
            request.user.email = email

            
            request.user.save()
            
            profil = Profile(
                phone = phone, 
                address = address, 
                user = request.user, 
                gender = gender,
                profession = profession, 
                country = country
            )
            profil.save()
            return redirect("user/profile")
        else:
            last_name = bleach.clean(request.POST["last_name"].strip())
            first_name = bleach.clean(request.POST["first_name"].strip())
            gender = request.POST["gender"]
            email = request.POST["email"]
            address = bleach.clean(request.POST["address"].strip())
            phone = bleach.clean(request.POST["phone"].strip())
            profession = bleach.clean(request.POST["profession"].strip())
            country = bleach.clean(request.POST["country"].strip())

            user = profile.user
            user.last_name = last_name
            user.first_name = first_name
            user.email = email

            user.save()
            profile.gender = gender
            profile.phone = phone
            profile.address = address
            profile.profession = profession
            profile.country = country
            
            profile.save()
            return redirect("user/profile")
            
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
        "countries": countries,
        "user": request.user,
        "profile": profile,
        "setting": get_setting(),
    }
    return render(request, "user/edit_profile.html", context)

@login_required(login_url='connection/login')
def delete_user(request, id):
    setting = get_setting()
    if setting is None:
        return redirect("settings/maintenance")
    
    try:
        user_id = dechiffrer_param(str(id))
        user = User.objects.get(id=user_id)
    except:
        user = None
    
    if user:
        user.delete()
    return redirect("user/users")

def ajax_delete_user(request, id):
    user = User.objects.get(id=id)
    context = {
        "user": user
    }
    return render(request, "ajax_delete_user.html", context)


def permission(request, user_id):
    setting = get_setting()
    if setting is None:
        redirect("settings/maintenance")
        
    id = int(dechiffrer_param(str(user_id)))
       
    user = User.objects.get(id=id)
    request.session["is_active"] = user.is_active
    request.session["is_staff"] = user.is_staff
    request.session["is_superuser"] = user.is_superuser
    context = {
        "setting": setting,
        "user": user
    }
    return render(request, "user/permission.html", context)

def update_permission(request):
    if request.method == "POST":
        id = int(request.POST["id"])
        try:
            user = User.objects.get(id=id)
        except:
            user = None

        if user == None:
            return JsonResponse({
                    "status": "error",
                    "message": "Identifiant inexistant."})
        else:            
            actif = request.POST.get('actif')
            staff = request.POST.get('staff')
            superuser = request.POST.get('superuser')
            if actif == "on":
                user.is_active = True
            else:
                user.is_active = False
                
            if staff == "on":
                user.is_staff = True
            else:
                user.is_staff = False
                
            if superuser == "on":
                user.is_superuser = True
            else:
                user.is_superuser = False
                
            user.save()
            return JsonResponse({
                "status": "success",
                "message": "Permission mise à jour avec succès."})   
            
def ajax_active_permission(request, actif):
    if actif == "on":
        request.session["is_active"] = True
    else:
        request.session["is_active"] = False
    context = {}
    return render(request, "ajax_active_permission.html", context)

def ajax_staff_permission(request, staff):
    if staff == "on":
        request.session["is_staff"] = True
    else:
        request.session["is_staff"] = False
    context = {}
    return render(request, "ajax_staff_permission.html", context)

def ajax_superuser_permission(request, superuser):
    if superuser == "on":
        request.session["is_superuser"] = True
    else:
        request.session["is_superuser"] = False
    context = {}
    return render(request, "ajax_superuser_permission.html", context)


class CustomPasswordChangeView(auth_views.PasswordChangeView):
    template_name = "password/password_change.html"
    success_url = reverse_lazy("password_change_done")
    form_class = PasswordChangingForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        setting = get_setting()
        context["setting"] = setting
        
        return context

class CustomPasswordChangeDoneView(auth_views.PasswordChangeDoneView):
    template_name = "password/password_change_success.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        setting = get_setting()
        context["setting"] = setting
        
        return context
    
    
class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name = "password/password_reset.html"
    success_url = reverse_lazy('password_reset_done')
    form_class = PasswordResForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        setting = get_setting()
        context["setting"] = setting
        
        return context
    
class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = "password/password_reset_sent.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        setting = get_setting()
        context["setting"] = setting
        
        return context
    
class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = "password/password_reset_form.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        setting = get_setting()
        context["setting"] = setting
        
        return context
    
class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = "password/password_reset_done.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        setting = get_setting()
        context["setting"] = setting
        
        return context

