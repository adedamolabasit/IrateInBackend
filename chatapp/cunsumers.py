from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
from .models import ChatMessage
from asgiref.sync import sync_to_async
import json

User = get_user_model()

class PersonalChatConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def get_user(self, user_id):
        return User.objects.get(id=user_id)

    @sync_to_async
    def get_last_30_messages(self):
        return list(ChatMessage.objects.filter(
            receiver=self.scope['user'],
            sender__id=self.scope['url_route']['kwargs']['id']
        ).order_by('-timestamp')[:30])

    async def connect(self):
        request_user = self.scope['user']
        chat_with_user_id = self.scope['url_route']['kwargs']['id']

        if request_user.is_authenticated:
            receiver = await self.get_user(chat_with_user_id)
            user_ids = sorted([request_user.id, receiver.id])
            self.room_group_name = f"chat_{user_ids[0]}_{user_ids[1]}"

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            # Accept the WebSocket connection
            await self.accept()

    async def receive(self, text_data, bytes_data=None):
        data = json.loads(text_data)
        message_content = data['message']
        initiator_id = data['initiator']
        sender = self.scope['user']
        receiver_id = self.scope['url_route']['kwargs']['id']
        initiator = initiator_id

        receiver = await self.get_user(receiver_id)
        
        await sync_to_async(ChatMessage.objects.create)(
            sender=sender,
            receiver=receiver,
            content=message_content,
            initiator=initiator,
            group_name=self.room_group_name
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message_content,
                'initiator':initiator
            }
        )

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def chat_message(self, event):
        message = event["message"]
        initiator = event["initiator"]
        await self.send(text_data=json.dumps({
            "message": message,
            "initiator":initiator
        }))
        
class OnlineStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "user"
        await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
        )
        await self.accept()
        
        async def disconnect(self,message):
            self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )