from collections import OrderedDict
from rest_framework import pagination
from rest_framework.response import Response
from django.conf import settings


class BasePagination(pagination.PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = settings.PAGINATION_MAX_PAGE_SIZE
    page_size = settings.PAGINATION_PAGE_SIZE

    def get_paginated_response(self, data):
        return Response({
            'meta': OrderedDict([
                ('count', self.page.paginator.count),
            ]),
            'pagination': OrderedDict([
                ('prev', self.page.previous_page_number() if self.page.has_previous() else None),
                ('next', self.page.next_page_number() if self.page.has_next() else None),
                ('last', self.page.paginator.num_pages),
            ]),
            'data': data,
        })

    def get_results(self, data):
        return data.get('data')
