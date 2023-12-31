from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="user")
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
    def last_10_messages(self):
        return ChatMessage.objects.order_by('-timestamp').all()[:10]


