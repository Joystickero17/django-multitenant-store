from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from core.models.chat.message import Message
channel_layer = get_channel_layer()

def send_message(from_user, to_user, message):
    instance = Message.objects.create(
        from_user=from_user,
        to_user=to_user,
        content=message
    )
    consumer_data={
            "type":"chat.message",  
            "message":"Ha llegado un nuevo mensaje",
            "content":f"{message}",
            "from_user":from_user,
            "to_user": to_user,
            "created_at": f"{instance.created_at.isoformat()}"
            }
    async_to_sync(channel_layer.group_send)(f'chat{to_user.pk}', consumer_data)