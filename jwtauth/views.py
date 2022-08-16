from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework import permissions
from django.contrib.auth import get_user_model
from jwtauth.serializers import UserSerializer
# Create your views here.

User = get_user_model()

class UserRegisterViewSet(GenericViewSet, CreateModelMixin):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()