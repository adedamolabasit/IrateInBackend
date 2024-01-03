from django.urls import path
from .views import register_user, login, get_user_list

app_name = "chatapp"

urlpatterns = [
    path('register/', register_user , name='register'),
    path('login/', login , name='login'),
    path('users/', get_user_list , name='users'),

]