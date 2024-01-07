from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializer import UserSerializer, LoginSerializer, UserGetSerializer,ChatMessageSerializer, FriendsListSerializer
from .authtoken import jwtAuth
from rest_framework import status
from .models import ChatMessage, FriendsList, User



@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        token = jwtAuth.generate_token(payload=serializer.data)
        return Response({
            "message": "Login Successful",
            "token": token,
            "user":serializer.data
        },status=status.HTTP_201_CREATED)
        
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_list(request):
    try:
        friends_list, _ = FriendsList.objects.get_or_create(user=request.user)
        excluded_users = [request.user] + list(friends_list.friends.all())
        user_obj = User.objects.exclude(id__in=[user.id for user in excluded_users])
        serializer = UserGetSerializer(user_obj, many=True)
        return Response(serializer.data, status=200)
    except Exception as e:
        print("error", str(e))
        return Response({"error": "Error getting users"}, status=400)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def get_user_details(request, id):
    try:
        user_obj = User.objects.get(id=id)
        serializer = UserGetSerializer(user_obj) 
        return Response(serializer.data, status=200)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)
    except Exception as e:
        print("error", str(e))
        return Response({"error": "Error getting user"}, status=400)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def get_previous_messages(request, id):
    user_ids = sorted([request.user.id, id])
    group_name = f"chat_{user_ids[0]}_{user_ids[1]}"
    try:
        user_obj = ChatMessage.objects.filter(
            group_name=group_name
        ).order_by('-timestamp')[:30]

        serializer = ChatMessageSerializer(user_obj, many=True)
        
        return Response(serializer.data, status=200)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)
    except ChatMessage.DoesNotExist:
        return Response({"error": "Messages not found"}, status=404)
    except Exception as e:
        return Response({"error": "Error getting messages"}, status=400)
    
    
@api_view(['POST'])
@permission_classes([IsAuthenticated]) 
def add_friend(request, email):
    try:
        friend_user = User.objects.filter(email=email).first()
        if friend_user is not None:
            friends_list, created = FriendsList.objects.get_or_create(user=request.user)
            friends_list.add_friend(friend_user)

            serializer = FriendsListSerializer(friends_list)
            return Response(serializer.data, status=200)
        else:
            print("Friend user not found for email:", email)
            return Response({"error": "Friend user not found"}, status=404)

    except FriendsList.DoesNotExist:
        print("FriendsList not found")
        return Response({"error": "FriendsList not found"}, status=404)
    except Exception as e:
        print("Error:", str(e))
        return Response({"error": f"Error adding friend directly: {str(e)}"}, status=500)




    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_friends(request):
    try:
        friends_list, created = FriendsList.objects.get_or_create(user=request.user)
        friends = friends_list.friends.all()  
        serializer = UserSerializer(friends, many=True) 
        return Response(serializer.data, status=200)

    except Exception as e:
        return Response({"error": f"Error getting user friends: {str(e)}"}, status=400)