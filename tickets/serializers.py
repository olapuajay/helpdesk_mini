from rest_framework import serializers
from .models import Ticket
from accounts.serializers import UserSerializer

class TicketSerializer(serializers.ModelSerializer):
  created_by = UserSerializer(read_only=True)
  assigned_to = UserSerializer(read_only=True)

  class Meta:
    model = Ticket
    fields = [
      "id", "title", "description", "status", "created_by", "assigned_to",
      "sla_deadline", "breached", "version", "created_at", "updated_at",
    ]

class TicketCreateSerializer(serializers.ModelSerializer):
  class Meta:
    model = Ticket
    fields = ["title", "description"]

  def create(self, validated_data):
    user = self.context["request"].user
    return Ticket.objects.create(created_by=user, **validated_data)
