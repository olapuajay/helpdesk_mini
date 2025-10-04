from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

class TicketLimitOffsetPagination(LimitOffsetPagination):
  default_limit = 5
  max_limit = 50

  def get_paginated_response(self, data):
    return Response({
      'items': data,
      'next_offset': self.offset + self.limit if self.offset + self.limit < self.count else None
    })