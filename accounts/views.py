from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework import serializers

User = get_user_model()

# Create your views here.
class RegisterSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only=True, required=True)
  class Meta:
    model = User
    fields = ("username", "email", "password", "role")
  
  def create(self, validated_data):
    user = User(
      username=validated_data["username"],
      email=validated_data["email"],
      role=validated_data.get("role", "user"),
    )
    user.set_password(validated_data["password"])
    user.save()
    return user
  

class RegisterView(generics.CreateAPIView):
  serializer_class = RegisterSerializer

  def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()

    refresh = RefreshToken.for_user(user)
    return Response({
      "user": UserSerializer(user).data,
      "refresh": str(refresh),
      "access": str(refresh.access_token),
    }, status=status.HTTP_201_CREATED)
  

class MeView(APIView):
  permission_classes = [IsAuthenticated]

  def get(self, request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)