# Importation des modules tiers
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Importation des modules locaux
from eab.views import nbnew_answer, nbnew_message, new_message, parametre
from eab.models import*
from app_auth.decorator import*
from .models import*
from eajc.utils.crypto import dechiffrer_param, chiffrer_param
# Importation des modules standards
import datetime
import bleach


#=================== Gestion du composant ======================
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def rooms(request):
    date = datetime.datetime.now()

    tabRooms = []
    #On regroupe des composant par disciplines
    rooms = Room.objects.values("discipline_id").annotate(effectif=Count("discipline_id"))
    for room in rooms:
    	#On recupère la discipline
        discipline = Discipline.objects.get(id=room["discipline_id"])
        dic = {}
        dic["id"] = discipline.id
        dic["libelle"] = discipline.libelle
        dic["effectif"] = room["effectif"]

        tabRooms.append(dic)
    context = {
        "rooms":tabRooms,
        "parametre":parametre(),
        "date":date,
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request)
    }
    return render(request, "room/rooms.html", context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def details_room(request,id):
    date = datetime.datetime.now()
    discipline_id = dechiffrer_param(str(id))
    discipline = Discipline.objects.get(id=discipline_id)
    rooms = Room.objects.filter(discipline_id=discipline_id)
    context = {
    	"discipline":discipline,
        "rooms":rooms,
        "parametre":parametre(),
        "date":date,
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request)
    }
    return render(request, "room/details_room.html", context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
@csrf_exempt
def add_room(request):
    date = datetime.datetime.now()
    if request.method=="POST":
        name = bleach.clean(request.POST["name"].strip())
        discipline = request.POST["discipline"]
        
        query = Room.objects.filter(name=name, discipline=discipline)
        # Existence de la chambre
        if query.exists():
            return JsonResponse({
                    "status": "error",
                    "message": "Cette chambre existe déjà."})
        else:
            room = Room(name=name, discipline_id=discipline)
            count0 = Room.objects.all().count()
            room.save()
            count1 = Room.objects.all().count()
            if count0 < count1:
                return JsonResponse({
                    "status": "success",
                    "message": "Chambre enregistrée avec succès."})
            else:
                return JsonResponse({'status':1})
            
    disciplines = Discipline.objects.all()
    context = {
        "disciplines":disciplines, 
        "parametre":parametre(), 
        "date":date,
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request)
    }
    return render(request, "room/add_room.html", context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def edit_room(request,id):
    date = datetime.datetime.now()
    room_id = dechiffrer_param(str(id))
    room = Room.objects.get(id=room_id)
    disciplines = Discipline.objects.all().exclude(id=room.discipline.id)
    context = {
        "room":room,
        "disciplines":disciplines,
        "parametre":parametre(),
        "date":date,
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request)
    }
    return render(request, "room/edit_room.html", context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
@csrf_exempt
def edit_ro(request):
    if request.method == "POST":
        id = int(request.POST["id"])
        try:
            room = Room.objects.get(id=id)
        except:
            room = None

        if room == None:
            return JsonResponse({
                    "status": "error",
                    "message": "Identifiant inexistant."})
        else:
            name = bleach.clean(request.POST["name"].strip())
            discipline = request.POST["discipline"]
            #Recuperer toutes les chambres en excluant la chambre actuelle
            rooms = Room.objects.filter(discipline_id=discipline).exclude(id=id)
            print(rooms)
            tabRoom = []
            for r in rooms:   
                tabRoom.append(r.name)
            #On verifie si cette chambre existe déjà
            if name in tabRoom:
                return JsonResponse({
                    "status": "error",
                    "message": "Cette chambre existe déjà."})
            else:
                room.name = name
                room.discipline_id = discipline
                room.save()
                return JsonResponse({
                    "status": "success",
                    "message": "Chambre modifiée avec succès."})

def ajax_delete_multiple_room(request, id):
    discipline = Discipline.objects.get(id=id)
    context = {
        "discipline": discipline
    }
    return render(request, "ajax_delete_multiple_room.html", context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def del_multiple_room(request,id):
    try:
        discipline_id = dechiffrer_param(str(id))
        discipline = Discipline.objects.get(id=discipline_id)
    except:
        discipline = None
        
    if discipline:
        rooms = Room.objects.filter(discipline_id=discipline_id)
        for room in rooms:
            room.delete()
    return redirect("room/rooms")
             
                
def ajax_delete_room(request, id):
    room = Room.objects.get(id=id)
    context = {
        "room": room
    }
    return render(request, "ajax_delete_room.html", context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def del_room(request,id):
    try:
        room_id = dechiffrer_param(str(id))
        room = Room.objects.get(id=room_id)
    except:
        room = None
        
    if room:
        room.delete()
    return redirect("room/details_room", id=chiffrer_param(str(room.discipline_id)))

# Compter le nombre de nouveaux chats d'une discipline
def count_new_chat(user_id, discipline_id):
    count = 0
    mgs = MessageStatus.objects.filter(user_id=user_id, read=1)
    for mg in mgs:
        if mg.message.room.discipline.id == discipline_id:
            count = count + 1
    return count

#Determinier le nombre de chambres activées de chaque discipline
def count_number_activated_room(userId, disciplineId):
    rooms = Room.objects.filter(discipline_id=disciplineId)
    count_room_activated = 0
    for room in rooms:
        if RoomUser.objects.filter(user_id=userId, room_id=room.id).exists():
            count_room_activated += 1
    return count_room_activated

#Determinier le nombre de disciplines activées
def count_number_activated_d(userId):
    disciplines = Discipline.objects.all()
    count_actvated_discipline = 0
    for discipline in disciplines:
        rooms = Room.objects.filter(discipline_id=discipline.id)
        count_room_activated = 0
        for room in rooms:
            if RoomUser.objects.filter(user_id=userId, room_id=room.id).exists():
                count_room_activated = 1
        if count_room_activated > 0:
            count_actvated_discipline += 1
    return count_actvated_discipline
        
    
@login_required(login_url='login')
def disc_room(request):
    date = datetime.datetime.now()

    # Recuperer les chats non lus
    messagestatus = MessageStatus.objects.filter(user_id=request.user.id, read=0)
    for ms in messagestatus:
        #Changer leur status à 1, juste pour indiquer l'accès à à la page suivante.
        ms.read = 1
        ms.save() 
        
    tabRooms = []
    #On regroupe des chambres par disciplines
    rooms = Room.objects.values("discipline_id").annotate(effectif=Count("discipline_id"))
    
    for room in rooms:
    	#On recupère la discipline
        discipline = Discipline.objects.get(id=room["discipline_id"])
        dic = {}
        dic["id"] = discipline.id
        dic["libelle"] = discipline.libelle
        dic["effectif"] = room["effectif"]
        dic["count_new_chat"] = count_new_chat(request.user.id, discipline.id)
        dic["count_activated_room"] = count_number_activated_room(request.user.id, discipline.id)

        tabRooms.append(dic) 
    
    context={
        "rooms":tabRooms,
        "count_number_activated_d":count_number_activated_d(request.user.id),
        "parametre":parametre(),
        "date":date,
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request)
    }
    return render(request, "room/disc_room.html", context)

# Compter le nombre de new message d'une chambre
def count_new_chat_room(user_id, room_id):
    count = 0
    mgs = MessageStatus.objects.filter(user_id=user_id, read=2)
    for mg in mgs:
        if mg.message.room.id == room_id:
            count = count + 1
    return count

def room_disc(request, id):
    date = datetime.datetime.now()
    user_id = request.user.id
    # Recuperer les chats non lus 
    messagestatus = MessageStatus.objects.filter(user_id=request.user.id, read__in = [0,1])
    for ms in messagestatus:
        #Changer leur status à 2, juste pour indiquer l'accès à la page suivante.
        ms.read = 2
        ms.save() 
        
    discipline = Discipline.objects.get(id=id)
    rooms = Room.objects.filter(discipline_id=id)
    # Associer le nombre de chats à chaque chambre
    tabRooms = []
    for room in rooms:
        dic = {}
        dic["room"] = room
        dic["count_new_chat_room"] = count_new_chat_room(user_id, room.id)
        tabRooms.append(dic)
        
    # Recuperer les chambres selectionnées par l'utilisateur
    roomusers = RoomUser.objects.filter(user_id = user_id)
    tab_roomId = []
    for roomuser in roomusers:
        tab_roomId.append(roomuser.room.id)
        
    context = {
        "tabRooms":tabRooms,
        "tab_roomId":tab_roomId,
        "discipline":discipline,
        "parametre":parametre(),
        "date":date,
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request)
    }
    return render(request, "room/room_disc.html", context)

def chat(request, id):
    date = datetime.datetime.now()
    
    # Recuperer les chats non lus 
    messagestatus = MessageStatus.objects.filter(user_id=request.user.id, read__in = [0,1,2])
    for ms in messagestatus:
        #Changer leur status à 3, juste pour indiquer l'accès à la page suivante.
        ms.read = 3
        ms.save()
        
    # On récupère la chambre
    room = Room.objects.get(id=id)
    # On recupère la chambre activée par l'utilisateur
    roomuser = RoomUser.objects.get(user_id=request.user.id, room_id=id)
    # On recupère uniquement les chats inferieurs à la date d'activation de chambre de conversation de l'utilisateur
    messages = Message.objects.filter(room_id=id, date__gt = roomuser.date_ac)
    
    user_id = request.user.id
    
    context = {
        "room":room,
        "user_id":user_id,
        "messages":messages,
        "parametre":parametre(),
        "date":date,
        "countanswer":nbnew_answer(request),
        "count":nbnew_message(request),
        "users":new_message(request)
    }
    return render(request, "message/chat.html", context)
    
class activate_message(View):
    def get(self, request, id, *args, **kwargs):
        userId = request.user.id
        qs = RoomUser.objects.filter(room_id=id, user_id=userId)
        # Verifier si l'utilisateur a déjà activé les messages ou pas
        activate = False
        if qs.exists():
            qs.delete()
        else:
            roomuser = RoomUser(user_id=userId, room_id=id)
            roomuser.save()
            activate = True

        context = {"activate":activate, 'roomId':id}
        return render(request, "activate_message.html", context)
    
@login_required(login_url='login')
def del_message(request,id):
    message = Message.objects.get(id=id)
    if message.user.id == request.user.id:
        message.delete()
    return redirect("message/chat", id=message.room.id)


def content_chat(request, id):
    
    # Recuperer les chats non lus 
    messagestatus = MessageStatus.objects.filter(user_id=request.user.id, read__in = [0,1,2])
    for ms in messagestatus:
        #Changer leur status à 3, juste pour indiquer l'accès à la page suivante.
        ms.read = 3
        ms.save()
        
    # On récupère la chambre
    room = Room.objects.get(id=id)
    # On recupère la chambre activée par l'utilisateur
    roomuser = RoomUser.objects.get(user_id=request.user.id, room_id=id)
    # On recupère uniquement les chats inferieurs à la date d'activation de chambre de conversation de l'utilisateur
    messages = Message.objects.filter(room_id=id, date__gt = roomuser.date_ac)
    
    user_id = request.user.id
    
    context = {
        "room":room,
        "user_id":user_id,
        "messages":messages
    }
    return render(request, "message/content_chat.html", context)

@login_required(login_url='login')
def new_chat(request):
    user_id = request.user.id
    if request.method == "POST":
        content = bleach.clean(request.POST["content"].strip())
        room_id = int(request.POST["room_id"])
        
        print(content)
        
        message = Message(content=content, room_id=room_id, user_id=user_id)
        
        message.save()
        
        user = User.objects.get(id=user_id)
        return JsonResponse({
            "status": "Save",
            "message": {
                "message_id": message.id,
                "content": message.content,
                "room_id": message.room.id,
                "last_name": user.last_name,
                "first_name": user.first_name, 
                "date": message.date
            }
        })
