from rest_framework import serializers
from core.models.chat.message import Message, get_user_model
from asgiref.sync import async_to_sync
from django.db.models import Q
from channels.layers import get_channel_layer
channel_layer = get_channel_layer()


User = get_user_model()

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"
        extra_kwargs = {
            "from_user":{
                "read_only":True
            }
        }
    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        data["from_user"] = self.context.get("request").user
        return data
        
    def create(self, validated_data):
        instance = super().create(validated_data)
        to_user = validated_data.get('to_user')
        has_profile_img = 
        consumer_data={
        "type":"chat.message",
        "message":"Ha llegado un nuevo mensaje",
        "content":f"{validated_data.get('content')}",
        "from_user":f"{instance.from_user.pk}",
        "from_user_email":f"{instance.from_user.email}",
        
        "to_user":f"{to_user.pk}",
        "created_at": f"{instance.created_at.isoformat()}"
        }
        if hasattr(instance.from_user.profile_img, "url"):
            consumer_data.update({"from_user_img":f"{instance.from_user.profile_img.url}",})
        async_to_sync(channel_layer.group_send)(f'chat{to_user.pk}', consumer_data)
        return instance


class UserChatMessageSerializer(serializers.ModelSerializer):
    messages = serializers.SerializerMethodField()
    # last_message_date = serializers.SerializerMethodField()
    class Meta:
        model = User
        exclude = [
            "password",
            "last_login",
            "is_superuser",
            "is_active",
            "is_staff",
            "role",
            "credits",
            "groups",
            "user_permissions"
        ]
    
    def get_messages(self, instance):
        messages = Message.objects.filter(Q(from_user=instance) & Q(to_user=self.context.get("request").user) | Q(to_user=instance) & Q(from_user=self.context.get("request").user)).order_by("created_at")
        return ChatMessageSerializer(messages, many=True).data
    
    # s