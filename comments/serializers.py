from rest_framework import serializers
from .models import Comment
from accounts.serializers import UserSerializer

class CommentSerializer(serializers.ModelSerializer):
  user = UserSerializer(read_only=True)

  class Meta:
    model = Comment
    fields = ["id", "ticket", "user", "text", "created_at"]
  
  def create(self, validated_data):
    user = self.context["request"].user
    ticket = self.context["ticket"]
    return Comment.objects.create(user=user, ticket=ticket, **validated_data)