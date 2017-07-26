# -*- coding: utf-8 -*-
from rest_framework.pagination import PageNumberPagination


class ElasticPageNumberPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

    def _get_count(self, search):
        response = search.execute()
        return response.hits.total

    def paginate_search(self, search, request, view=None):
        return super().paginate_queryset(search, request, view=None)
