from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

# Create your models here.
class IdempotencyKey(models.Model):
  key = models.CharField(max_length=225, unique=True)
  method = models.CharField(max_length=10)
  path = models.CharField(max_length=225)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  response_hash = models.CharField(max_length=225)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"{self.key} - {self.user}"