from django.db import models
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

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





# class User(AbstractUser):
#     username = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']


#     def profile(self):
#         Profile.objects.get(user=self)

    

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     full_name = models.CharField(max_length=1000)
#     bio = models.CharField(max_length=100)
#     image = models.ImageField(upload_to="user_images", default="default.jpg")
#     verified = models.BooleanField(default=False)

#     def save(self, *args, **kwargs):
#         if self.full_name == "" or self.full_name == None:
#             self.full_name = self.user.username
#         super(Profile, self).save(*args, **kwargs)


# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()

# post_save.connect(create_user_profile, sender=User)
# post_save.connect(save_user_profile, sender=User)


# class ChatMessage(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="user", default=1)
#     sender = models.ForeignKey(User, on_delete=models.CASCADE,related_name="sender", default=1)
#     reciever = models.ForeignKey(User, on_delete=models.CASCADE,related_name="reciever", default=1)
#     message = models.TextField(default="None")
#     is_read = models.BooleanField(default=False)
#     date = models.DateTimeField(auto_now_add=True)

   
#     class Meta:
#         ordering = ['date']
#         verbose_name_plural = "Message"
        
#     def __str__(self):
#         return F"{self.sender} - {self.reciever}"
    
#     @property
#     def sender_profile(self):
#         sender_profile = Profile.objects.get(user=self.sender)
#         return sender_profile
#     @property
#     def reciever_profile(self):
#         reciever_profile = Profile.objects.get(user=self.reciever)
#         return reciever_profile


