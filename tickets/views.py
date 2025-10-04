from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import APIException

from .models import Ticket
from .serializers import TicketSerializer, TicketCreateSerializer
from .permissions import IsOwnerOrAdmin
from core.pagination import TicketLimitOffsetPagination

# Create your views here.
class TicketListCreateView(generics.ListCreateAPIView):
  permission_classes = [IsAuthenticated]
  pagination_class = TicketLimitOffsetPagination

  def get_queryset(self):
    user = self.request.user
    q = self.request.query_params.get("q", "")
    qs = Ticket.objects.all() if user.role == "admin" else Ticket.objects.filter(created_by=user)
    if q:
      qs = qs.filter(title__iscontains=q) | qs.filter(description__iscontains=q)
    
    for ticket in qs:
      ticket.check_breach()

    return qs.order_by("-created_at")
  
  def get_serializer_class(self):
    return TicketCreateSerializer if self.request.method == "POST" else TicketSerializer


class VersionConflict(APIException):
  status_code = status.HTTP_409_CONFLICT
  default_detail = { 'error': { 'code': 'VERSION_MISMATCH', 'message': 'Ticket version mismatch'} }


class TicketDetailView(generics.RetrieveUpdateAPIView):
  queryset = Ticket.objects.all()
  serializer_class = TicketSerializer

  def get_object(self):
    ticket = super().get_object()
    ticket.check_breach()
    return ticket

  def patch(self, request, *args, **kwargs):
    ticket = self.get_object()
    client_version = request.data.get("version")

    if client_version is None:
      return Response(
        { "error": { "code": "FIELD_REQUIRED", "field": "version", "message": "Version is required" } },
        status=status.HTTP_400_BAD_REQUEST
      )
    
    if int(client_version) != ticket.version:
      raise VersionConflict()
    
    serializer = self.get_serializer(ticket, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    updated_ticket = serializer.save(version=ticket.version + 1)

    updated_ticket.check_breach()

    return Response(TicketSerializer(updated_ticket).data)


class BreachedTicketListView(generics.ListAPIView):
  serializer_class = TicketSerializer
  permission_classes = [IsAuthenticated]

  def get_queryset(self):
    qs = Ticket.objects.filter(breached=True).order_by("-updated_at")
    for ticket in qs:
      ticket.check_breach()

    return qs