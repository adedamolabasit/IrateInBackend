# from django.db import models
# from django.db.models.signals import post_save
# from django.contrib.auth.models import AbstractUser


# class User(AbstractUser):
#     username = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)



# class ChatMessage(models.Models):
#     user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="user")
#     sender = models.ForeignKey(User, on_delete=models.CASCADE,related_name="sender")
#     reciever = models.ForeignKey(User, on_delete=models.CASCADE,related_name="reciever")
#     message = models.CharField(max_length=2000)
#     is_read = models.BooleanField(default=False)
#     date = models.DateTimeField(auto_now_add=True)


