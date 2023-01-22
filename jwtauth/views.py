from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.views import APIView
from rest_framework.mixins import CreateModelMixin
from rest_framework import permissions, response, status
from django.contrib.auth import get_user_model
from jwtauth.serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.

User = get_user_model()

class UserRegisterViewSet(GenericViewSet, CreateModelMixin):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()

class TokenWithSessionViewSet(APIView):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
           return response.Response(status=status.HTTP_401_UNAUTHORIZED)
        refresh = RefreshToken.for_user(request.user)
        print("Usuario que pidio exchange",request.user)
        print(refresh.access_token)

        return response.Response({'refresh': str(refresh),'access': str(refresh.access_token)})
        