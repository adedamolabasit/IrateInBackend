from django.db import models
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
class userManager(BaseUserManager):
    def create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError("users must have an email")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,password=None,**extra_fields):
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_superuser",True)
        return self.create_user(email,password,**extra_fields)
    
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=256, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    objects = userManager()
    
    USERNAME_FIELD = "email"
    
    def get_full_name(self):
        return F"{self.first_name} {self.last_name}"
    
    def __str__(self):
        return self.email
    
# class UserProfile(models.Model):
#     user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='user_profile')
#     name = models.CharField(max_length=255, blank=True)
#     online_status = models.BooleanField(default=False)
    
#     def __str__(self):
#         return self.user.username


class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    initiator = models.IntegerField(default=0)
    group_name = models.CharField(max_length=256, blank=False, default="group")
    
    
class FriendsList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="users")
    friends = models.ManyToManyField(User,blank=True,related_name="friends")

    
    def __str__(self):
        return self.user.email
    
    def add_friend(self, friend_user):
        if not friend_user in self.friends.all():
            self.friends.add(friend_user)
            self.save()

    def remove_friend(self, friend_user):
        if friend_user in self.friends.all():
            self.friends.remove(friend_user)
    

            
            
        
    