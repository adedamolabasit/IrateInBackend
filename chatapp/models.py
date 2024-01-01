from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="user", default=1)
    sender = models.ForeignKey(User, on_delete=models.CASCADE,related_name="sender", default=1)
    reciever = models.ForeignKey(User, on_delete=models.CASCADE,related_name="reciever", default=1)
    message = models.TextField(default="None")
    is_read = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

   
    class Meta:
        ordering = ['date']
        verbose_name_plural = "Message"
        
    def __str__(self):
        return F"{self.sender} - {self.reciever}"


