# chat/routing.py
from django.urls import path

from .cunsumers import PersonalChatConsumer, OnlineStatusConsumer

websocket_urlpatterns = [
    path("ws/<int:id>", PersonalChatConsumer.as_asgi()),
    path("ws/online", OnlineStatusConsumer.as_asgi()),
]