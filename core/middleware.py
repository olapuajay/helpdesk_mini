from django.utils.deprecation import MiddlewareMixin
from core.models import IdempotencyKey
from django.http import JsonResponse
import hashlib
import json

class IdempotencyMiddleware(MiddlewareMixin):
  def process_request(self, request):
    if request.method == "POST":
      key = request.headers.get("Idempotency-Key")
      if key:
        existing = IdempotencyKey.objects.filter(key=key, user=request.user, path=request.path).first()
        if existing:
          return JsonResponse(json.loads(existing.response_hash))
    return None
  
  def process_response(self, request, response):
    if request.method == "POST":
      key = request.headers.get("Idempotency-Key")
      if key:
        hash_response = json.dumps(response.data if hasattr(response, "data") else response.content.decode())
        IdempotencyKey.objects.update_or_create(
          key=key, user=request.user, path=request.path,
          defaults={'method': request.method, 'response_hash': hash_response}
        )
    return response