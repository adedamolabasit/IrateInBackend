from .models import ChatMessage
from rest_framework import serializers



class ChatMessageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ChatMessage
        fields = ["id","user","sender","reciever","message","is_read","date"]