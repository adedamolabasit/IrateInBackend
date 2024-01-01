from django.shortcuts import render, get_object_or_404
from .models import ChatMessage
# Create your views here.
def index(request):
    return render(request, "chat/index.html")

def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})

def get_last_10_messages(chatId):
    chat = get_object_or_404(ChatMessage, id=chatId)
    return chat.messages.order_by('-timestamp').all()[:10]