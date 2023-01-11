# chat/routing.py
from django.urls import re_path, path

from . import consumers

websocket_urlpatterns = [
    path("ws/notifications/<str:store_name>/", consumers.ChatConsumer.as_asgi()),
]