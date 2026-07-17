from django.contrib import admin
from .models import*

class AdminRoom(admin.ModelAdmin):
    search_fields=('name',)

admin.site.register(Room, AdminRoom)

class AdminMessage(admin.ModelAdmin):
    search_fields=('content',)

admin.site.register(Message, AdminMessage)

class AdminMessageStatus(admin.ModelAdmin):
    search_fields=('user_id','room_id',)

admin.site.register(MessageStatus, AdminMessageStatus)

class AdminRoomUser(admin.ModelAdmin):
    search_fields=('user_id',)

admin.site.register(RoomUser, AdminRoomUser)
