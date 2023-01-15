from rest_framework import serializers
from core.models import Category
import itertools



class CategorySerializer(serializers.ModelSerializer):
    full_path = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = "__all__"
    
    def get_full_path(self,instance):
        route = []
        new_instance = instance
        while new_instance.parent:
            route.append(new_instance.parent.name)
            new_instance = new_instance.parent
        route.append(instance.name)
        return route
