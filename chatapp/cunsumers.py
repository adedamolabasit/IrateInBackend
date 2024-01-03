import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
# from .models import ChatMessage
from django.contrib.auth import get_user_model
import json



User = get_user_model()


class PersonalChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        request_user = self.scope['user']
        print("user...",request_user)
        if request_user.is_authenticated:
            print("yes")
            chat_with_user = self.scope['url_route']['kwargs']['id']
            
            user_ids = [int(request_user.id), int(chat_with_user)]
            user_ids = sorted(user_ids)
            self.room_group_name = f"chat"  
            self.room_group_name = f"chat_{user_ids[0]}_{user_ids[1]}"  
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()

            
    async def receive(self, text_data, bytes_data=None):
        data = json.loads(text_data)
        message = data['message']
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type":"chat_message",
                "message":message
            }
        )
             
            
    async def disconnect(self, code):
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
    async def chat_message(self,event):
        message = event["message"]
        await self.send(text_data=json.dumps({
            "message": message
        }))

