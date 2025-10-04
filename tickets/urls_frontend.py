from django.urls import path
from .views_frontend import (
    ticket_list, ticket_detail, ticket_create,
    admin_dashboard, assign_ticket, agent_dashboard
)

urlpatterns = [
    path("", ticket_list, name="ticket_list"),
    path("create/", ticket_create, name="ticket_create"),
    path("<int:pk>/", ticket_detail, name="ticket_detail"),

    # Admin
    path("dashboard/", admin_dashboard, name="admin_dashboard"),
    path("assign/<int:ticket_id>/", assign_ticket, name="assign_ticket"),

    # Agent
    path("agent/dashboard/", agent_dashboard, name="agent_dashboard"),
]
