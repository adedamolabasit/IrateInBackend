import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import ChatMessage
from django.contrib.auth import get_user_model




User = get_user_model()


class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        print(data,"kfjfj")
        messages = ChatMessage.last_10_messages()
        content = {
            'message': self.messages_to_json(messages)
        }
        self.send_message(content)

    def new_message(self, data):
        user = data['from']
        sender_user = User.objects.filter(username=user)[0]
        ChatMessage.objects.create(user=sender_user,content=data["message"])
        content = {
            'command': 'new_message',
            'message': self.message_to_json
        }
        return self.send_chat_message(content)
    
    def messages_to_json(self,messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result
  
    
    def message_to_json(self,message):
        return{
            'id': message.id,
            'user':message.user.username,
            'content':message.content,
            'date':str(message.date)
        }
    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }

    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data["command"]](self,data)

    def send_chat_message(self,message):     
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": message}
        )
    
    def send_message(self,message):
        self.send(text_data=json.dumps({"message": message}))

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))