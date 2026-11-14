from rest_framework.pagination import PageNumberPagination

class MyPagination(PageNumberPagination):
    """Пагинация для вывода курсов и уроков."""
    page_size = 5  # Количество элементов на странице по умолчанию
    page_size_query_param = 'page_size'  # Параметр запроса для изменения размера
    max_page_size = 20  # Максимальное количество элементов на странице