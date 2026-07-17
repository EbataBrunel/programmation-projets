# Importation des modules tiers
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Imporation des modules locaux
from eab.views import*
from eab.models import*
from eab.views import nbnew_answer, nbnew_message, new_message, parametre
from app_auth.decorator import*
from .models import*
from .forms import*
from eajc.utils.crypto import dechiffrer_param, chiffrer_param
# Importation des modules standards
import datetime
import bleach

#=================== Gestion de discipline ======================
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def disciplines(request):
    date = datetime.datetime.now()

    disciplines = Discipline.objects.all()
    context = {
        "disciplines":disciplines,
        "parametre":parametre(),
        "date":date,
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request)
    }
    return render(request, "discipline/disciplines.html", context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def add_disc(request):
    date = datetime.datetime.now()
    if request.method == "POST":
        libelle = bleach.clean(request.POST["libelle"].strip())
        query = Discipline.objects.filter(libelle=libelle)
        # Verifier l'existence de la discipline
        if query.exists():
            return JsonResponse({
                    "status": "error",
                    "message": "Cette discipline existe déjà."})
        else:
            discipline = Discipline(libelle=libelle)
            count0 = Discipline.objects.all().count()
            discipline.save()
            count1 = Discipline.objects.all().count()
            if count0 < count1:
                return JsonResponse({
                    "status": "success",
                    "message": "Discipline enregistrée avec succès."})
            else:
                return JsonResponse({
                    "status": "error",
                    "message": "L'insertion a échouée."})
    context = {
        "parametre":parametre(), 
        "date":date,
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request)
        }
    return render(request, "discipline/add_disc.html", context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def edit_disc(request, id):
    date = datetime.datetime.now()
    discipline_id = dechiffrer_param(str(id))
    discipline = Discipline.objects.get(id=discipline_id)
    context = {
        "discipline":discipline,
        "parametre":parametre(),
        "date":date,
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request)
    }
    return render(request, "discipline/edit_disc.html", context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
@csrf_exempt
def edit_dis(request):
    
    if request.method == "POST":
        id = int(request.POST["id"])
        try:
            discipline = Discipline.objects.get(id=id)
        except:
            discipline = None

        if discipline == None:
            return JsonResponse({
                    "status": "error",
                    "message": "Identifiant inexistant."})
        else:
            libelle = bleach.clean(request.POST["libelle"].strip())
            #On verifie si cette année a déjà été enregistrée
            disciplines = Discipline.objects.exclude(id=id)
            tabDiscipline = []
            for disc in disciplines:          
                tabDiscipline.append(disc.libelle)
            #On verifie si cette année existe déjà
            if libelle in tabDiscipline:
                return JsonResponse({
                    "status": "error",
                    "message": "Cette discipline existe déjà."})
            else:
                discipline.libelle = libelle
                discipline.save()
                return JsonResponse({
                    "status": "success",
                    "message": "Discipline modifiée avec succès."})
            
def ajax_delete_discipline(request, id):
    discipline = Discipline.objects.get(id=id)
    context = {
        "discipline": discipline
    }
    return render(request, "ajax_delete_discipline.html", context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def del_disc(request,id):
    try:
        discipline_id = dechiffrer_param(str(id))
        discipline = Discipline.objects.get(id=discipline_id)
    except:
        discipline = None
    
    if discipline:
        discipline.delete()
    return redirect("discipline/disciplines")

#=================== Gestion du composant ======================
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def composants(request):
    date = datetime.datetime.now()

    tabComposants = []
    #On regroupe des composant par disciplines
    composants = Composant.objects.values("discipline_id").annotate(effectif=Count("discipline_id"))
    for composant in composants:
    	#On recupère la discipline
        discipline = Discipline.objects.get(id=composant["discipline_id"])
        dic = {}
        dic["id"] = discipline.id
        dic["libelle"] = discipline.libelle
        dic["effectif"] = composant["effectif"]

        tabComposants.append(dic)
    context = {
        "composants":tabComposants,
        "parametre":parametre(),
        "date":date,
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request)
    }
    return render(request, "composant/composants.html", context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def details_cmp(request,id):
    date = datetime.datetime.now()
    discipline_id = dechiffrer_param(str(id))
    discipline = Discipline.objects.get(id=discipline_id)
    composants = Composant.objects.filter(discipline_id=discipline_id)
    context = {
    	"discipline":discipline,
        "composants":composants,
        "parametre":parametre(),
        "date":date,
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request)
    }
    return render(request, "composant/details_cmp.html", context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
@csrf_exempt
def add_cmp(request):
    date = datetime.datetime.now()
    if request.method == "POST":
        libelle = bleach.clean(request.POST["libelle"].strip())
        discipline = request.POST["discipline"]
        query = Composant.objects.filter(libelle=libelle)
        # Verifier l'existence de la composition
        if query.exists():
            return JsonResponse({
                    "status": "error",
                    "message": "Ce composant existe déjà."})
        else:
            composant = Composant(libelle=libelle, discipline_id=discipline)
            count0 = Composant.objects.all().count()
            composant.save()
            count1 = Composant.objects.all().count()
            if count0 < count1:
                return JsonResponse({
                    "status": "success",
                    "message": "Composant enregistré avec succès."})
            else:
                return JsonResponse({
                    "status": "error",
                    "message": "L'insertion a échouée."})
            
    disciplines = Discipline.objects.all()
    context = {
        "disciplines":disciplines, 
        "parametre":parametre(), 
        "date":date,
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request)
    }
    return render(request, "composant/add_cmp.html", context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def edit_cmp(request,id):
    date = datetime.datetime.now()
    composant_id = dechiffrer_param(str(id))
    composant = Composant.objects.get(id=composant_id)
    disciplines = Discipline.objects.all().exclude(id=composant.discipline.id)
    context = {
        "composant":composant,
        "disciplines":disciplines,
        "parametre":parametre(),
        "date":date,
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request)
    }
    return render(request, "composant/edit_cmp.html", context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
@csrf_exempt
def edit_com(request):
    if request.method == "POST":
        id = int(request.POST["id"])
        try:
            composant = Composant.objects.get(id=id)
        except:
            composant = None

        if composant == None:
            return JsonResponse({
                    "status": "error",
                    "message": "Identifiant inexistant."})
        else:
            libelle = bleach.clean(request.POST["libelle"].strip())
            discipline = request.POST["discipline"]
            #On verifie si cette année a déjà été enregistrée
            composants = Composant.objects.exclude(id=id)
            tabComposant = []
            for comp in composants:          
                tabComposant.append(comp.libelle)
            #On verifie si cette année existe déjà
            if libelle in tabComposant:
                return JsonResponse({
                    "status": "error",
                    "message": "Ce composant existe déjà."})
            else:
                composant.libelle = libelle
                composant.discipline_id = discipline
                composant.save()
                return JsonResponse({
                    "status": "success",
                    "message": "Composant modifié avec succès."})
                
def ajax_delete_multiple_composant(request, id):
    discipline = Discipline.objects.get(id=id)
    context = {
        "discipline": discipline
    }
    return render(request, "ajax_delete_multiple_composant.html", context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def del_multiple_cmp(request,id):
    try:
        discipline_id = dechiffrer_param(str(id))
        discipline = Discipline.objects.get(id=discipline_id)
    except:
        discipline = None
        
    if discipline:
        composants = Composant.objects.filter(discipline_id=discipline_id)
        for composant in composants:
            composant.delete()
    return redirect("composant/composants")
            
def ajax_delete_composant(request, id):
    composant = Composant.objects.get(id=id)
    context = {
        "composant": composant
    }
    return render(request, "ajax_delete_composant.html", context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def del_cmp(request,id):
    try:
        composant_id = dechiffrer_param(str(id))
        composant = Composant.objects.get(id=composant_id)
    except:
        composant = None
        
    if composant:
        composant.delete()
    return redirect("composant/details_cmp", id=chiffrer_param(str(composant.discipline_id)))


#======================== Questions & Reponses===================
@login_required(login_url='login')
def postquestion(request):
    date = datetime.datetime.now()

    if request.method == "POST":        
        form = QuestionForm(request.POST)
        if form.is_valid():
            user = request.user.id
            discipline = request.POST["discipline"]
            composant = request.POST["composant"]
            subject = bleach.clean(request.POST["subject"].strip())
            content = form.cleaned_data["content"]

            question = Question(
            	subject=subject, 
            	content=content, 
            	date=date, 
            	composant_id=composant, 
            	discipline_id=discipline, 
            	user_id=user)
            question.save()

            #messages.error(request, "Message envoyé avec succès.")
            return redirect("question/questions")
        else:
            form = QuestionForm()

    disciplines = Discipline.objects.all()
    form = QuestionForm()
    context = {
    	"disciplines":disciplines,
    	"form":form,
    	"parametre":parametre(),
    	"date":date,
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request)
    }
    return render(request, "question/postquestion.html", context)

class getCompDiscipline(View):
    def get(self, request, id, *args, **kwargs):
        
        composants = Composant.objects.filter(discipline_id=id)

        context = {
            "composants":composants
        }
        return render(request, "ajaxCompDisc.html", context)
    
@login_required(login_url='login')
def questions(request):
    date = datetime.datetime.now()

    questions = Question.objects.all().order_by("-id")
    tabQuestion = []
    
    for ques in questions:
        status = 0
        #On determine le nombre de likes de chaque question
        countlikes = Likes.objects.filter(question_id=ques.id).count()
        #On verifie le membre connecté a déjà liké ou pas
        q = Likes.objects.filter(question_id=ques.id,user_id=request.user.id)
        if q.exists():
            status += 1

        quests = Answer.objects.values("question_id").filter(question_id=ques.id).annotate(effectif=Count("question_id"))
        if quests.exists():
            for quest in quests:
                question = Question.objects.get(id=quest["question_id"])
                #Verifier si cette question a été signalé ou pas par l'utilisateur
                query = SignalerQuestion.objects.filter(user_id=request.user.id, question_id=quest["question_id"])
                report = False
                if query.exists():
                   report = True 
                   
                dic = {}
                dic["id"] = quest["question_id"]
                dic["subject"] = question.subject
                dic["content"] = question.content
                dic["date"] = question.date
                dic["user"] = question.user
                dic["user_id"] = question.user.id
                try:
                    dic["photo"] = question.user.profile.photo
                except:
                    dic["photo"] = None
                dic["composant"] = question.composant.libelle
                dic["effectif"] = quest["effectif"]
                dic["countlikes"] = countlikes
                dic["status"] = status
                dic["report"] = report
                tabQuestion.append(dic)
        else:
            #Verifier si cette question a été signalé ou pas par l'utilisateur
            query = SignalerQuestion.objects.filter(user_id=request.user.id, question_id=ques.id)
            report = False
            if query.exists():
                report = True 
                
            dic = {}
            dic["id"] = ques.id
            dic["subject"] = ques.subject
            dic["content"] = ques.content
            dic["date"] = ques.date
            dic["user"] = ques.user
            dic["user_id"] = ques.user.id
            try:
                dic["photo"] = ques.user.profile.photo
            except:
                dic["photo"] = None
            dic["composant"] = ques.composant.libelle
            dic["effectif"] = 0
            dic["countlikes"] = countlikes
            dic["status"] = status
            dic["report"] = report
            tabQuestion.append(dic)

    paginator = Paginator(tabQuestion, 10)
    num_page = request.GET.get('page')
    tabQuestion = paginator.get_page(num_page)
    
    context = {
    	"questions":tabQuestion,
    	"parametre":parametre(),
    	"date":date,
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request)
        }
    return render(request, "question/questions.html", context)

@login_required(login_url='login')
def my_questions(request):
    date = datetime.datetime.now()
    #On change de statut pour marquer la reception de notification sur des nouvelles reponses aux questions de ce memebre
    quest = Question.objects.filter(user_id=request.user.id).order_by("-id")
    for question in quest:
        answers = Answer.objects.filter(question_id=question.id, status=0)
        for answer in answers:
            answ = answer
            answ.status = 1
            answ.save()

    questions = Question.objects.filter(user_id=request.user.id).order_by("-id")
    tabQuestion = []
    for ques in questions:

        status = 0
        #On determine le nombre de likes de chaque question
        countlikes = Likes.objects.filter(question_id=ques.id).count()
        #On verifie le membre connecté a déjà liké ou pas
        q = Likes.objects.filter(question_id=ques.id,user_id=request.user.id)
        if q.exists():
            status += 1

        quests = Answer.objects.values("question_id").filter(question_id=ques.id).annotate(effectif=Count("question_id"))
        if quests.exists():
            for quest in quests:
                #On compte le nombre de reponses non lus
                list_answers = Answer.objects.filter(question_id=ques.id, status=1)
                #On exlu les reponses de ce membre qui a posé la question
                countanswer = 0
                for answer in list_answers:
                    if answer.user_id != request.user.id:
                        countanswer += 1

                question = Question.objects.get(id=quest["question_id"])
                dic = {}
                dic["id"] = quest["question_id"]
                dic["q"] = question
                dic["subject"] = question.subject
                dic["content"] = question.content
                dic["date"] = question.date
                dic["user"] = question.user
                dic["user_id"] = ques.user.id
                try:
                    dic["photo"] = ques.user.profile.photo
                except:
                    dic["photo"] = None
                dic["effectif"] = quest["effectif"]
                dic["countanswer"] = countanswer
                dic["countlikes"] = countlikes
                dic["status"] = status
                tabQuestion.append(dic)
        else:
            dic = {}
            dic["id"] = ques.id
            dic["q"] = question
            dic["subject"] = ques.subject
            dic["content"] = ques.content
            dic["date"] = ques.date
            dic["user"] = ques.user
            dic["user_id"] = ques.user.id
            try:
                dic["photo"] = ques.user.profile.photo
            except:
                dic["photo"] = None
            dic["effectif"] = 0
            dic["countanswer"] = 0
            dic["countlikes"] = countlikes
            dic["status"] = status
            tabQuestion.append(dic)

    paginator = Paginator(tabQuestion, 10)
    num_page = request.GET.get('page')
    tabQuestion = paginator.get_page(num_page)
    
    context = {
    	"questions":tabQuestion,
    	"parametre":parametre(),
    	"date":date,
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request)
    }
    return render(request, "question/my_questions.html", context)

@login_required(login_url='login')
def answer(request,id):
    date = datetime.datetime.now()
    question_id = dechiffrer_param(str(id))
    #On recupère la question
    question = Question.objects.get(id=question_id)
    #On change le statut de cette question pour marquer quen toutes ses reponses ont été lu
    answers = Answer.objects.filter(question_id=question_id, status=1)
    for answer in answers:
            answ = answer
            answ.status = 2
            answ.save()
    
    if request.method == "POST":        
        form = AnswerForm(request.POST)
        if form.is_valid():
            user = request.user.id
            content = form.cleaned_data["content"]

            answer = Answer(
            	content = content, 
            	date = date, 
            	question_id = question_id,
            	user_id = user)
            answer.save()

            #messages.error(request, "Message envoyé avec succès.")
            return redirect("question/answer", id=chiffrer_param(str(id)))
        else:
            form=AnswerForm()

    answers = Answer.objects.filter(question_id=question_id).order_by("-id")
    #On determine l'ordre de chaque question
    tabanswer = []
    count = 0
    for answer in answers:

        status = 0
        #On determine le nombre de likes de chaque réponse
        countlikes = Likeanswer.objects.filter(answer_id=answer.id).count()
        #On verifie si le membre connecté a déjà liké ou pas chaque réponse
        q = Likeanswer.objects.filter(answer_id=answer.id,user_id=request.user.id)
        if q.exists():
            status += 1

        count += 1
        
        #Verifier si cette réponse a été signalé ou pas par l'utilisateur
        query = SignalerAnswer.objects.filter(user_id=request.user.id, answer_id=answer.id)
        report = False
        if query.exists():
            report = True 
            
        dic = {}
        dic["id"] = answer.id
        try:
            dic["photo"] = answer.user.profile.photo
        except:
            dic["photo"] = None
        dic["content"]=answer.content
        dic["user_id"] = answer.user.id
        dic["user"] = answer.user
        dic["date"] = answer.date
        dic["nameauthor"] = answer.question.user
        dic["composant"] = answer.question.composant.libelle
        dic["count"] = count
        dic["countlikes"] = countlikes
        dic["status"] = status
        dic["report"] = report
        tabanswer.append(dic)

    totalanswer = Answer.objects.filter(question_id=question_id).count()

    form = AnswerForm()
    context = {
        "totalanswer":totalanswer,
        "question":question,
    	"answers":tabanswer,
    	"form":form,
    	"parametre":parametre(),
    	"date":date,
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request)
    }
    return render(request, "question/answer.html", context)

@login_required(login_url='login')
def f_answer(request,id):
    date = datetime.datetime.now()
    question_id = dechiffrer_param(str(id))
    #On recupère la question
    question = Question.objects.get(id=question_id)
    #On change le statut de cette question pour marquer quen toutes ses reponses ont été lu
    answers = Answer.objects.filter(question_id=question_id, status=1)
    for answer in answers:
            answ = answer
            answ.status = 2
            answ.save()
    
    if request.method == "POST":        
        form = AnswerForm(request.POST)
        if form.is_valid():
            user = request.user.id
            content = form.cleaned_data["content"]

            answer = Answer(
            	content=content, 
            	date=date, 
            	question_id=question_id,
            	user_id=user)
            answer.save()

            #messages.error(request, "Message envoyé avec succès.")
            return redirect("question/f-answer", id=chiffrer_param(str(id)))
        else:
            form = AnswerForm()

    answers = Answer.objects.filter(question_id=question_id).order_by("-id")
    #On determine l'ordre de chaque question
    tabanswer = []
    count = 0
    for answer in answers:

        status = 0
        #On determine le nombre de likes de chaque réponse
        countlikes = Likeanswer.objects.filter(answer_id=answer.id).count()
        #On verifie si le membre connecté a déjà liké ou pas chaque réponse
        q = Likeanswer.objects.filter(answer_id=answer.id,user_id=request.user.id)
        if q.exists():
            status += 1
            
        #Verifier si cette réponse a été signalé ou pas par l'utilisateur
        query = SignalerAnswer.objects.filter(user_id=request.user.id, answer_id=answer.id)
        report = False
        if query.exists():
            report = True 

        count += 1
        dic = {}
        dic["id"] = answer.id
        try:
            dic["photo"] = answer.user.profile.photo
        except:
            dic["photo"] = None
        dic["content"] = answer.content
        dic["user_id"] = answer.user.id
        dic["user"] = answer.user
        dic["date"] = answer.date
        dic["author"] = answer.question.user
        dic["composant"] = answer.question.composant.libelle
        dic["count"] = count
        dic["countlikes"] = countlikes
        dic["status"] = status
        dic["report"] = report
        tabanswer.append(dic)

    totalanswer = Answer.objects.filter(question_id=question_id).count()

    form = AnswerForm()
    context = {
        "totalanswer":totalanswer,
        "question":question,
    	"answers":tabanswer,
    	"form":form,
    	"parametre":parametre(),
    	"date":date,
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request)
    }
    return render(request, "question/f-answer.html", context)

@login_required(login_url='login')
def my_answer(request,id):
    date = datetime.datetime.now()
    question_id = dechiffrer_param(str(id))
    #On recupère la question
    question = Question.objects.get(id=question_id)
    #On change le statut de cette question pour marquer quen toutes ses reponses ont été lu
    answers = Answer.objects.filter(question_id=question_id, status=1)
    for answer in answers:
            answ=answer
            answ.status=2
            answ.save()
    
    if request.method == "POST":        
        form = AnswerForm(request.POST)
        if form.is_valid():
            user = request.user.id
            content = form.cleaned_data["content"]

            answer = Answer(
            	content=content, 
            	date=date, 
            	question_id=question_id,
            	user_id=user)
            answer.save()

            #messages.error(request, "Message envoyé avec succès.")
            return redirect("question/my-answer", id=chiffrer_param(str(id)))
        else:
            form = AnswerForm()

    answers = Answer.objects.filter(question_id=question_id).order_by("-id")
    #On determine l'ordre de chaque question
    tabanswer = []
    count = 0
    for answer in answers:

        status = 0
        #On determine le nombre de likes de chaque réponse
        countlikes = Likeanswer.objects.filter(answer_id=answer.id).count()
        #On verifie si le membre connecté a déjà liké ou pas chaque réponse
        q = Likeanswer.objects.filter(answer_id=answer.id, user_id=request.user.id)
        if q.exists():
            status += 1

        count += 1
        dic = {}
        dic["id"] = answer.id
        try:
            dic["photo"] = answer.user.profile.photo
        except:
            dic["photo"] = None
        dic["content"] = answer.content
        dic["user_id"] = answer.user.id
        dic["user"] = answer.user
        dic["date"] = answer.date
        dic["author"] = answer.question.user
        dic["composant"] = answer.question.composant.libelle
        dic["count"] = count
        dic["countlikes"] = countlikes
        dic["status"] = status
        tabanswer.append(dic)

    totalanswer = Answer.objects.filter(question_id=question_id).count()

    form = AnswerForm()
    context = {
        "totalanswer":totalanswer,
        "question":question,
    	"answers":tabanswer,
    	"form":form,
    	"parametre":parametre(),
    	"date":date,
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request)
    }
    return render(request, "question/my-answer.html", context)

@login_required(login_url='login')
def listforum(request):
    date = datetime.datetime.now()

    disciplines = Discipline.objects.all()
    tabDicsipline = []
    for discipline in disciplines:
        dicDisc = {}
        effect = 0
        composants = Composant.objects.filter(discipline_id=discipline.id)
        tabComposants = []
        for composant in composants:
            query = Question.objects.values("composant_id").filter(composant_id=composant.id).annotate(effectif=Count("composant_id"))
            if query.exists():
                for comp in query:
                    effect += comp["effectif"]
                    dic = {}
                    dic["id"] = composant.id
                    dic["libelle"] = composant.libelle
                    dic["effectif"] = comp["effectif"]
                    tabComposants.append(dic)
            else:
                dic = {}
                dic["id"] = composant.id
                dic["libelle"] = composant.libelle
                dic["effectif"] = 0
                tabComposants.append(dic)

        dicDisc["id"] = discipline.id
        dicDisc["libelle"] = discipline.libelle
        dicDisc["effectif"] = effect
        dicDisc["composants"] = tabComposants
        tabDicsipline.append(dicDisc)

    paginator = Paginator(tabDicsipline, 10)
    num_page = request.GET.get('page')
    tabDicsipline = paginator.get_page(num_page)

    context = {
        "disciplines":tabDicsipline,
        "parametre":parametre(),
        "date":date,
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request)
    }
    return render(request, "question/listforum.html", context)

@login_required(login_url='login')
def detforum(request,id):
    date = datetime.datetime.now()
    composant_id = dechiffrer_param(str(id))
    composant = Composant.objects.get(id=composant_id)
    questions = Question.objects.filter(composant_id=composant_id).order_by("-id")
    tabQuestion = []
    for ques in questions:
        status = 0
        #On determine le nombre de likes de chaque question
        countlikes = Likes.objects.filter(question_id=ques.id).count()
        #On verifie le membre connecté a déjà liké ou pas
        q = Likes.objects.filter(question_id=ques.id,user_id=request.user.id)
        if q.exists():
            status+=1

        quests = Answer.objects.values("question_id").filter(question_id=ques.id).annotate(effectif=Count("question_id"))
        if quests.exists():
            for quest in quests:
                #Recuperer la question
                question = Question.objects.get(id=quest["question_id"])
                #Verifier si cette question a été signalé ou pas par l'utilisateur
                query = SignalerQuestion.objects.filter(user_id=request.user.id, question_id=quest["question_id"])
                report = False
                if query.exists():
                   report = True 
                   
                dic = {}
                dic["q"] = question
                dic["id"] = quest["question_id"]
                dic["subject"] = question.subject
                dic["content"] = question.content
                dic["date"] = question.date
                dic["user"] = question.user
                dic["user_id"] = question.user.id
                try:
                    dic["photo"] = question.user.profile.photo
                except:
                    dic["photo"] = None
                dic["effectif"] = quest["effectif"]
                dic["countlikes"] = countlikes
                dic["status"] = status
                dic["report"] = report
                tabQuestion.append(dic)
        else:
            #Verifier si cette question a été signalé ou pas par l'utilisateur
            query = SignalerQuestion.objects.filter(user_id=request.user.id, question_id=ques.id)
            report = False
            if query.exists():
                report = True 
                
            dic = {}
            dic["q"] = ques
            dic["id"] = ques.id
            dic["subject"] = ques.subject
            dic["content"] = ques.content
            dic["date"] = ques.date
            dic["user"] = ques.user
            dic["user_id"] = ques.user.id
            try:
                dic["photo"] = ques.user.profile.photo
            except:
                dic["photo"] = None
            dic["effectif"] = 0
            dic["countlikes"] = countlikes
            dic["status"] = status
            dic["report"] = report
            tabQuestion.append(dic)

    paginator = Paginator(tabQuestion, 10)
    num_page = request.GET.get('page')
    tabQuestion = paginator.get_page(num_page)
    
    context = {
        "composant": composant,
    	"questions": tabQuestion,
    	"parametre": parametre(),
    	"date": date,
        "countanswer": nbnew_answer(request),
        "count": nbnew_message(request),
        "users": new_message(request)
    }
    return render(request, "question/detfurom.html", context)


class ajaxlike(View):
    def get(self, request, id, *args, **kwargs):
        status = 0
        query = Likes.objects.filter(question_id=id,user_id=request.user.id)
        if query.exists():
            for like in query:
                like.delete()
        else:
            like = Likes(question_id=id, user_id=request.user.id)
            like.save()

            q = Likes.objects.filter(question_id=id,user_id=request.user.id)
            if q.exists():
                status += 1

        #On compte le nombre de likes
        countlikes = Likes.objects.filter(question_id=id).count()
        #Liste des membres qui ont likés cette question
        likes = Likes.objects.filter(question_id=id)

        context = {
            "id":id,
            "status":status,
            "countlikes":countlikes,
            "likes":likes
        }
        return render(request, "ajaxlike.html", context)
    
class ajaxlikes(View):
    def get(self, request, id, *args, **kwargs):
        #Liste des membres qui ont likés cette question
        likes = Likes.objects.filter(question_id=id).order_by("-id")
        countlikes = Likes.objects.filter(question_id=id).count()
        context = {
            "likes":likes,
            "countlikes":countlikes
        }
        return render(request, "ajaxlikes.html", context)
    
class ajaxlikeanswer(View):
    def get(self, request, id, *args, **kwargs):
        status = 0
        query = Likeanswer.objects.filter(answer_id=id,user_id=request.user.id)
        if query.exists():
            for likeanswer in query:
                likeanswer.delete()
        else:
            likeanswer = Likeanswer(answer_id=id, user_id=request.user.id)
            likeanswer.save()

            q = Likeanswer.objects.filter(answer_id=id,user_id=request.user.id)
            if q.exists():
                status += 1

        #On compte le nombre de likes
        countlikes = Likeanswer.objects.filter(answer_id=id).count()

        context = {
            "status":status,
            "countlikes":countlikes
        }
        return render(request, "ajaxlike.html", context)
    
class ajaxlikeanswers(View):
    def get(self, request, id, *args, **kwargs):
        #Liste des membres qui ont likés cette question
        likes = Likeanswer.objects.filter(answer_id=id).order_by("-id")
        #On compte le nombre de likes
        countlikes = Likeanswer.objects.filter(answer_id=id).count()

        context = {
            "likes":likes,
            "countlikes":countlikes
        }
        return render(request, "ajaxlikes.html", context)
    
class delquestion(View):
    def get(self, request, id, *args, **kwargs):
        question = Question.objects.get(id=id)
        question.delete()
        return JsonResponse({'status':1})

class my_delques(View):
    def get(self, request, id, *args, **kwargs):
        question = Question.objects.get(id=id)
        question.delete()
        return JsonResponse({'status':1})

class f_delques(View):
    def get(self, request, id, *args, **kwargs):
        question = Question.objects.get(id=id)
        question.delete()
        return JsonResponse({'status':1})

class delanswer(View):
    def get(self, request, id, *args, **kwargs):
        answer = Answer.objects.get(id=id)
        answer.delete()
        return JsonResponse({'status':1})

class my_delanswer(View):
    def get(self, request, id, *args, **kwargs):
        answer = Answer.objects.get(id=id)
        answer.delete()
        return JsonResponse({'status':1})

class f_delanswer(View):
    def get(self, request, id, *args, **kwargs):
        answer = Answer.objects.get(id=id)
        answer.delete()
        return JsonResponse({'status':1})

@login_required(login_url='connection/login')
@csrf_exempt
def report_question(request, id):
    date = datetime.datetime.now()
    question = Question.objects.get(id=id)
    context = {
        "question":question,
        "parametre":parametre(),
        "date":date,
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request)
    }
    return render(request, "question/report_question.html", context)

#Signaler une question selection à partir du composant
@login_required(login_url='connection/login')
@csrf_exempt
def report_lq(request, id):
    date = datetime.datetime.now()
    question = Question.objects.get(id=id)
    context = {
        "question":question,
        "parametre":parametre(),
        "date":date,
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request)
    }
    return render(request, "question/report_lq.html", context)

#Signaler une réponse selectionnée à partir du composant
@login_required(login_url='connection/login')
@csrf_exempt
def report_la(request, id):
    date = datetime.datetime.now()
    answer = Answer.objects.get(id=id)
    context = {
        "answer":answer,
        "parametre":parametre(),
        "date":date,
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request)
    }
    return render(request, "question/report_la.html", context)

@login_required(login_url='connection/login')
@csrf_exempt
def report_answer(request, id):
    date = datetime.datetime.now()
    answer = Answer.objects.get(id=id)
    context = {
        "answer":answer,
        "parametre":parametre(),
        "date":date,
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request)
    }
    return render(request, "question/report_answer.html", context)

@login_required(login_url='connection/login')
@csrf_exempt
def report_quest(request):
    if request.method == "POST":
        questionId = request.POST["question"]
        justification = bleach.clean(request.POST["justification"].strip())
        userId = request.user.id
        query = SignalerQuestion.objects.filter(user_id=userId, question_id=questionId)
        if query.exists():
            return JsonResponse({'status':0})
        else:
            sq = SignalerQuestion(user_id=userId, question_id=questionId, justification=justification)
            sq.save()
            return JsonResponse({'status':'Save'})
        
#Annuler le signal
@login_required(login_url='connection/login')
@csrf_exempt
def cancel_quest_report(request,id):
    query = SignalerQuestion.objects.filter(user_id=request.user.id, question_id=id)
    if query.exists():
        qs = query.first()
        qs.delete()  
    return redirect("question/questions")
    
#Annuler le signal
@login_required(login_url='connection/login')
@csrf_exempt
def cancel_ques_report(request,id):
    question = Question.objects.get(id=id)
    query = SignalerQuestion.objects.filter(user_id=request.user.id, question_id=id)
    if query.exists():
        qs = query.first()
        qs.delete()  
    return redirect("question/detforum", id=question.composant.id)
    
@login_required(login_url='connection/login')
@csrf_exempt
def report_answ(request):
    if request.method == "POST":
        answerId = request.POST["answer"]
        justification = request.POST["justification"]
        userId = request.user.id
        query = SignalerAnswer.objects.filter(user_id=userId, answer_id=answerId)
        if query.exists():
            return JsonResponse({'status':0})
        else:
            sq = SignalerAnswer(user_id=userId, answer_id=answerId, justification=justification)
            sq.save()
            return JsonResponse({'status':'Save'})
        
#Annuler le signalement de la réponse
def cancel_answer_report(request,id):
    answer = Answer.objects.get(id=id)
    query = SignalerAnswer.objects.filter(user_id=request.user.id, answer_id=id)
    if query.exists():
        qs = query.first()
        qs.delete()  
    return redirect("question/answer", id=answer.question.id)
    
#Annuler le signal de la réponse
@login_required(login_url='connection/login')
@csrf_exempt
def cancel_answ_report(request,id):
    answer = Answer.objects.get(id=id)
    query = SignalerAnswer.objects.filter(user_id=request.user.id, answer_id=id)
    if query.exists():
        qs = query.first()
        qs.delete()  
    return redirect("question/f-answer", id=answer.question.id)
    
@login_required(login_url='connection/login')
@csrf_exempt
def count_report(request):
    date = datetime.datetime.now()
    countquestionreport = SignalerQuestion.objects.all().count
    countanswerreport = SignalerAnswer.objects.all().count
    context = {
        "countquestionreport":countquestionreport,
        "countanswerreport":countanswerreport,
        "parametre":parametre(),
        "date":date,
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request)
    }
    return render(request, "question/count_report.html", context)

def report_questions(request):
    date = datetime.datetime.now()
    # On regroupe les signales par questions
    reportquestions = SignalerQuestion.objects.values("question_id").annotate(effectif=Count("question_id"))
    tab_question_report=[]
    for rq in reportquestions:
        #Récuperer la question
        question = Question.objects.get(id=rq["question_id"])
        #Recupérer les utilisateurs
        reportquestion = SignalerQuestion.objects.filter(question_id=rq["question_id"])
        dic = {}
        dic["question"] = question 
        dic["effectif"] = rq["effectif"]
        dic["reportquestion"] = reportquestion
        tab_question_report.append(dic)
               
    context = {
        "tab_question_report":tab_question_report,
        "parametre":parametre(),
        "date":date,
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request)
    }
    return render(request, "question/report_questions.html", context)

def report_answers(request):
    date = datetime.datetime.now()
    # On regroupe les signales par réponses
    reportanswers = SignalerAnswer.objects.values("answer_id").annotate(effectif=Count("answer_id"))
    tab_answer_report=[]
    for rq in reportanswers:
        #Récuperer la réponse
        answer = Answer.objects.get(id=rq["answer_id"])
        #Recupérer les utilisateurs
        reportanswer = SignalerAnswer.objects.filter(answer_id=rq["answer_id"])
        dic = {}
        dic["answer"] = answer 
        dic["effectif"] = rq["effectif"]
        dic["reportanswer"] = reportanswer
        tab_answer_report.append(dic)
               
    context = {
        "tab_answer_report":tab_answer_report,
        "parametre":parametre(),
        "date":date,
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request)
    }
    return render(request, "question/report_answers.html", context)

#Supprimer la question signalée
class delete_rq(View):
    def get(self, request, id, *args, **kwargs):
        question = Question.objects.get(id=id)
        if question:
            question.delete()
            return JsonResponse({"status":1})
        else:
            return JsonResponse({"status":0})
        
#Supprimer la réponse signalée
class delete_ra(View):
    def get(self, request, id, *args, **kwargs):
        answer = Answer.objects.get(id=id)
        if answer:
            answer.delete()
            return JsonResponse({"status":1})
        else:
            return JsonResponse({"status":0})
        
