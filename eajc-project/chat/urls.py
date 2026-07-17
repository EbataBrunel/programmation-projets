from django.urls import path
from .views import*

urlpatterns=[

    path("rooms", rooms, name="room/rooms"),
    path("add-room", add_room, name="room/add_room"),
    path("edit_room/<str:id>", edit_room, name="room/edit_room"),
    path("edit-ro", edit_ro, name="room/edit_ro"),
    path("ajax_delete_multiple_room/<int:id>", ajax_delete_multiple_room, name="ajax_delete_multiple_room"),  
    path("del-room-multiple/<str:id>", del_multiple_room, name="del_multiple_room"),
    path("details_room/ajax_delete_room/<int:id>", ajax_delete_room, name="ajax_delete_room"),  
    path("del-room/<str:id>", del_room, name="del_room"),
    path("details_room/<str:id>", details_room, name="room/details_room"),
    path("disc_room", disc_room, name="room/disc_room"),
    path("room-disc/<int:id>", room_disc, name="room/room_disc"),
    
    path("d/<int:id>", chat, name="message/chat"),
    path("del-message/<int:id>", del_message, name="del_message"),
    
    path("d/chat/content_chat/<int:id>", content_chat, name="chat/content_chat"),
    path("new-chat", new_chat, name="new_chat"),
    path("room-disc/activate_message/<int:id>", activate_message.as_view(), name="activate_message"),

]