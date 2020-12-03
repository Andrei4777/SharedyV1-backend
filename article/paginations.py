from rest_framework.pagination import PageNumberPagination


class ArticlePagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 1
