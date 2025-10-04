from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

# Create your models here.
User = settings.AUTH_USER_MODEL

class Ticket(models.Model):
  STATUS_CHOICES = (
    ("open", "Open"),
    ("in_progress", "In Progress"),
    ("resolved", "Resolved"),
    ("closed", "Closed"),
  )

  title = models.CharField(max_length=225)
  description = models.TextField()
  status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="open")

  created_by = models.ForeignKey(User, related_name="created_tickets", on_delete=models.CASCADE)
  assigned_to = models.ForeignKey(
    User, related_name="assigned_tickets", on_delete=models.SET_NULL, null=True, blank=True
  )

  sla_deadline = models.DateTimeField(blank=True, null=True)
  breached = models.BooleanField(default=False)
  version = models.IntegerField(default=1)

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def check_breach(self):
    if self.sla_deadline and timezone.now() > self.sla_deadline:
      if not self.breached:
        self.breached = True
        self.save(update_fields=["breached", "updated_at"])

  def save(self, *args, **kwargs):
    # Auto-set SLA deadline if not defined
    if not self.sla_deadline:
      self.sla_deadline = timezone.now() + timedelta(hours=48)
    # Update breach status
    self.check_breach()
    super().save(*args, **kwargs)
  
  def __str__(self):
    return f"#{self.id} - {self.title}"