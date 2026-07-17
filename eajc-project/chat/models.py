from django.db import models
from django.contrib.auth.models import User
from forum.models import Discipline
from datetime import datetime

class Room(models.Model):
    discipline=models.ForeignKey(Discipline, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class Message(models.Model):
    content = models.CharField(max_length=10000)
    date = models.DateTimeField(default=datetime.now , blank = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.content
    
class MessageStatus(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="statuses")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="message_statuses")
    read = models.IntegerField(default=0, null=True)
    #read_at = models.DateTimeField(null=True, blank=True)
    
class RoomUser(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)
    date_ac = models.DateTimeField(default=datetime.now, null=True, blank=True)
