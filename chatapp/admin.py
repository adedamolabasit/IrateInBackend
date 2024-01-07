from django.contrib import admin
from .models import ChatMessage, User, FriendsList

admin.site.register(ChatMessage)
admin.site.register(User)
admin.site.register(FriendsList)
