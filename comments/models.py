from django.db import models
from django.conf import settings
from tickets.models import Ticket

User = settings.AUTH_USER_MODEL

# Create your models here.
class Comment(models.Model):
  ticket = models.ForeignKey(Ticket, related_name="comments", on_delete=models.CASCADE)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  text = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"Comment by {self.user} on Ticket #{self.ticket.id}"