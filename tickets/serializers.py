from rest_framework import serializers
from .models import Ticket
from accounts.models import User
from accounts.serializers import UserSerializer

class TicketSerializer(serializers.ModelSerializer):
  created_by = UserSerializer(read_only=True)
  assigned_to = UserSerializer(read_only=True)
  breached = serializers.BooleanField(read_only=True)

  assigned_to_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role="agent"),
        source="assigned_to",
        write_only=True,
        required=False
    )

  class Meta:
    model = Ticket
    fields = [
      "id", "title", "description", "status", "created_by", "assigned_to","assigned_to_id",
      "sla_deadline", "breached", "version", "created_at", "updated_at",
    ]
    read_only_fields = [
      "created_by", "assigned_to", "sla_deadline", "breached",
      "version", "created_at", "updated_at"
    ]

class TicketCreateSerializer(serializers.ModelSerializer):
  class Meta:
    model = Ticket
    fields = ["title", "description"]

  def create(self, validated_data):
    request = self.context.get("request")
    user = request.user if request else None
    ticket = Ticket.objects.create(created_by=user, **validated_data)
    return ticket
