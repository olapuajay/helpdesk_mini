from django.urls import path
from .views import TicketListCreateView, TicketDetailView
from comments.views import CommentListCreateView

urlpatterns = [
  path("", TicketListCreateView.as_view(), name="ticket-list-create"),
  path("<int:pk>/", TicketDetailView.as_view(), name="ticket-detail"),
  path("<int:ticket_id>/comments/", CommentListCreateView.as_view(), name="ticket-comments"),
]