from core.models.notificacions import Notification,ChannelGroup
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
channel_layer = get_channel_layer()




def create_notification(content, entity_name, entity_id, group="general"):
    channel_group,_ = ChannelGroup.objects.get_or_create(name=group)
    notification = Notification.objects.create(
        message=content, 
        entity_name=entity_name, 
        entity_id=entity_id, 
        channel_group=channel_group
        )
    consumer_data={
        "type":"chat.message",
        "message":f"{content}",
        "entity_data":f"{entity_id}",
        "entity_name": f"{entity_name}",
        "group":f"{group}",
        "created_at": f"{notification.created_at.isoformat()}"
        }
    async_to_sync(channel_layer.group_send)(group, consumer_data) 