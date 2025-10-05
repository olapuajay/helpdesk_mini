from django.http import JsonResponse

# Health check endpoint
def health_check(request):
  return JsonResponse({ "status": "ok" })

# Meta info endpoint
def meta_info(request):
  return JsonResponse({
    "name": "Helpdesk Mini Ticket Management System",
    "version": "1.0.0",
    "description": "A Django-based ticketing system with role-based dashboards for users, agents, and admins",
    "author": "Ajay Olapu",
    "status": "running"
  })
