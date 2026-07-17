# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message, Room, MessageStatus, RoomUser
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

User = get_user_model()

# Un dictionnaire global pour stocker les utilisateurs connectés dans chaque room
connected_users = {}

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name'] # Récuperation des parametres de l'URL.
        self.room_group_name = f'chat_{self.room_name}'

        # Joindre la room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        # Ajouter l'utilisateur à la liste des utilisateurs connectés
        await self.add_user_to_connected()

        await self.accept()
        
        # Envoyer la liste mise à jour des utilisateurs connectés
        await self.send_connected_users()

    async def disconnect(self, close_code):
        # Retirer l'utilisateur de la liste des utilisateurs connectés
        await self.remove_user_from_connected()
        
        # Quitter la room
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
        # Envoyer la liste mise à jour des utilisateurs connectés
        await self.send_connected_users()

    # Recevoir un message WebSocket du client
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        
        action = text_data_json.get('action')

        if action == 'delete_message':
            message_id = text_data_json.get('message_id')
            await self.delete_message(message_id)
            
            # Envoyer un message aux autres utilisateurs pour indiquer qu'un message a été supprimé
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'message_deleted',
                    'message_id': message_id
                }
            )
        else:
            message = text_data_json['message']
            
            # Sauvegarder le message dans la base de données
            user = self.scope['user']  # L'utilisateur authentifié qui envoie le message
            
            user_instance = None
            if user.is_authenticated:  # Vérifie que l'utilisateur est connecté
                room_instance = await self.get_room(self.room_name)
                user_instance = await self.get_user_object(user.id)
                # Créer et enregistrer le message dans la base de données
                message_obj = await self.save_message(user_instance, message, room_instance)  # Appel à une méthode asynchrone
                
                # Ajout du status de message
                await self.save_status_message(message_obj.id)
                # Mise à jour de la lecture du message
                await self.update_message_reading(user.id)

                message_time = message_obj.date.strftime('%d-%m-%Y %H:%M')  # Formater la date
                
                for u in connected_users[self.room_group_name]:
                    await self.update_message_reading(u[0])
                
                # Envoyer le message à la room
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': message,
                        'user_id':user.id,
                        'username':user.username,
                        'first_name':user.first_name,
                        'last_name':user.last_name,
                        'date': message_time,
                        'message_id':message_obj.id
                    }
                )
                
    # Mettre à jour la lecture de messages
    @database_sync_to_async
    def update_message_reading(self, userId):
        messagestatus = MessageStatus.objects.filter(user_id=userId, read__in = [0,1,2])
        for ms in messagestatus:
            #Changer leur status à 3, juste pour indiquer l'accès à la page suivante.
            ms.read=3
            ms.save()
            
    @database_sync_to_async
    def get_user_object(self, user_id):
        qs = User.objects.filter(id=user_id)
        if qs.exists():
            obj = qs.first()
        else:
            obj = None
        return obj
        
    @database_sync_to_async  
    def get_room(self, id):
        room_instance = Room.objects.get(pk=id)
        return room_instance
    
     # Méthode asynchrone pour sauvegarder le message
    @database_sync_to_async
    def save_message(self, user_id, message, room_id):
        message_obj = Message.objects.create(
            user=user_id,
            room=room_id,
            content=message
        )
        return message_obj

    # Recevoir un message de la room
    async def chat_message(self, event):
        message = event['message']
        user_id = event['user_id']
        username = event['username']
        first_name = event['first_name']
        last_name = event['last_name']
        date = event['date']

        # Envoyer le message au WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'user_id':user_id,
            'username': username,
            'first_name':first_name,
            'last_name':last_name,
            'date': date,
            'message_id': event['message_id']
        }))
    
    @database_sync_to_async   
    def delete_message(self, message_id):
        try:
            message = Message.objects.get(id=message_id)
            if message.user == self.scope['user']:  # Vérifier si c'est bien l'auteur
                message.delete()  # Supprimer le message
                
        except Message.DoesNotExist:
            pass
        
    # Méthode pour envoyer l'événement de suppression aux clients
    async def message_deleted(self, event):
        message_id = event['message_id']

        # Envoyer un événement de suppression au WebSocket
        await self.send(text_data=json.dumps({
            'action': 'delete_message',
            'message_id': message_id
        }))
      
    async def add_user_to_connected(self):
        user = self.scope['user']
        """Ajouter un utilisateur à la liste des utilisateurs connectés."""
        if self.room_group_name not in connected_users:
            connected_users[self.room_group_name] = set()

        if self.scope['user'].is_authenticated:
            connected_users[self.room_group_name].add((user.id, user.first_name, user.last_name))

    async def remove_user_from_connected(self):
        user = self.scope['user']
        """Supprimer un utilisateur de la liste des utilisateurs connectés."""
        if self.scope['user'].is_authenticated and self.room_group_name in connected_users:
            connected_users[self.room_group_name].discard((user.id, user.first_name, user.last_name))

            if not connected_users[self.room_group_name]:
                del connected_users[self.room_group_name]
                
    async def send_connected_users(self):
        """Envoyer la liste des utilisateurs connectés à tous les clients du groupe."""
        if self.room_group_name in connected_users:
            users = list(connected_users[self.room_group_name])
        else:
            users = []
           
        for user in users:
            await self.update_message_reading(user[0])

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_list',
                'users': users,
                'length_users':len(users)
            }
        )

    # Envoyer la liste des utilisateurs aux WebSockets
    async def user_list(self, event):
        users = event['users']

        # Envoyer la liste des utilisateurs connectés via WebSocket
        await self.send(text_data=json.dumps({
            'action': 'user_list',
            'users': users,
            'length_users':len(users)
        }))
        
    # Enregistrer le status du message
    @database_sync_to_async
    def save_status_message(self, message_id):
        user = self.scope['user']
        # Recuperer le message
        message = Message.objects.get(id=message_id)
        users = User.objects.exclude(id=user.id)
        for u in users:
            # Verifier si l'utilisateur a activer ou pas les message de la chambre ou le message a été envoyé
            qs = RoomUser.objects.filter(room_id=message.room.id, user_id=u.id)
            if qs.exists():
                messagestatus = MessageStatus(message_id=message_id, user_id=u.id)
                messagestatus.save()
                
        