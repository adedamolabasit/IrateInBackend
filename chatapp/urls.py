from django.urls import path
from .views import register_user, login, get_user_list, get_user_details, get_previous_messages, add_friend, get_user_friends

app_name = "chatapp"

urlpatterns = [
    path('register/', register_user , name='register'),
    path('login/', login , name='login'),
    path('users/', get_user_list , name='users'),
    path('users/<int:id>/', get_user_details , name='users'),
    path('messages/<int:id>/', get_previous_messages , name='chat messages'),
    path('friends/<str:email>/', add_friend , name='add friends'),
    path('friends/', get_user_friends , name='get friends'),

]