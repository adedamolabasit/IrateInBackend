"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from chatapp.routing import websocket_urlpatterns
from channels.auth import AuthMiddlewareStack
from chatapp.channelmiddleware import Jwtwebsocketmiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

application = get_asgi_application()


application = ProtocolTypeRouter({
    "http":application,
    "websocket": Jwtwebsocketmiddleware(AuthMiddlewareStack(URLRouter(websocket_urlpatterns)))
})

