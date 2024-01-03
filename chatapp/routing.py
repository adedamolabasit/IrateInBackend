# chat/routing.py
from django.urls import path

from .cunsumers import PersonalChatConsumer

websocket_urlpatterns = [
    path("ws/<int:id>", PersonalChatConsumer.as_asgi()),
]