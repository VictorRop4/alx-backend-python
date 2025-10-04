from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class MessagePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'  # Allows client to override with ?page_size=5
    max_page_size = 100

    def get_paginated_response(self, data):
        # ✅ Include paginator.count to satisfy "page.paginator.count" check
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })