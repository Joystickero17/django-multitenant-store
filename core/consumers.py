# chat/consumers.py
import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from core.models.notificacions import ChannelGroup

def create_group(name):
    group,_ = ChannelGroup.objects.get_or_create(name=name)

    return group
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["store_name"]
        user = self.scope["user"]
        self.room_group_name = "store_%s" % self.room_name
        print(self.room_group_name)
        database_sync_to_async(create_group)(self.room_group_name)
        database_sync_to_async(create_group)(f"chat{user.pk}")

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.channel_layer.group_add(f"chat{user.pk}", self.channel_name)

        await self.accept()
        
    async def chat_message(self,event):
        print(event)
        await self.send(text_data=json.dumps(
             {
            "message": event.get("message"),
            "entity_name": event.get("entity_name"),
            "entity_id": event.get("entity_id"),
            "from_user": event.get("from_user"),
            "from_user_email":event.get("from_user_email"),
            "from_user_img":event.get("from_user_img"),
            "to_user": event.get("to_user"),
            "content": event.get("content"),
            "created_at": event.get("created_at"),
            "updated_at": event.get("updated_at"),
            "channel_group": event.get("channel_group"),
        },
        ))
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    # # Receive message from room group
    # async def chat_message(self, event):
    #     message = event["message"]

    #     # Send message to WebSocket
    #     await self.send(text_data=json.dumps({"message": message}))