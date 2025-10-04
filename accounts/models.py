from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
  ROLE_CHOICES = (
    ("user", "User"),
    ("agent", "Agent"),
    ("admin", "Admin"),
  )
  role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="user")

  def __str__(self):
    return f"{self.username} ({self.role})"
