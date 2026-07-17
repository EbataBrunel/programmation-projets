
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('message/chat/<int:room_name>/', consumers.ChatConsumer.as_asgi()),
]