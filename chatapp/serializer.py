from .models import User, ChatMessage, FriendsList
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    def create(self,validated_data):
        user = User.objects.create_user(
            email = validated_data['email'],
            password = validated_data['password'],
            first_name = validated_data.get('first_name',''),
            last_name = validated_data.get('last_name','')
        )
        
        return user
    
    class Meta:
        model = User
        fields = ['email','password','first_name','last_name','id']
        extra_kwargs = {
            'password':{'write_only':True}
        }

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    id = serializers.CharField(max_length=24, read_only= True)
    password = serializers.CharField(max_length=255, write_only=True)
    
    def validate(self,data):
        email = data.get("email", None)
        password = data.get("password", None)
        
        if email is None:
            raise serializers.ValidationError("An email is required")
        if password is None:
            raise serializers.ValidationError("password is required")
        
        user = authenticate(username=email, password=password)
        
        if user is None:
            raise serializers.ValidationError("Invalid email?Password")
        
        if not user.is_active:
            raise serializers.ValidationError("user is inactive")
        
        return {
            "id":user.id,
            "email":user.email,
        }
        
class UserGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','first_name', 'last_name', 'id']
        extra_kwargs = {'id':{'read_only':True}}
        
class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = '__all__'
            
class FriendsListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='user.id')
    email = serializers.EmailField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')

    class Meta:
        model = FriendsList
        fields = ['id', 'friends', 'email', 'first_name', 'last_name']