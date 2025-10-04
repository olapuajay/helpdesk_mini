from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Comment
from .serializers import CommentSerializer
from tickets.models import Ticket

# Create your views here.
class CommentListCreateView(generics.ListCreateAPIView):
  serializer_class = CommentSerializer
  permission_classes = [IsAuthenticated]

  def get_queryset(self):
    ticket_id = self.kwargs["ticket_id"]
    return Comment .objects.filter(ticket_id=ticket_id).order_by("created_at")
  
  def perform_create(self, serializer):
    ticket = Ticket.objects.get(id=self.kwargs["ticket_id"])
    serializer.save(user=self.request.user, ticket=ticket)
