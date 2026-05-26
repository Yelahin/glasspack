import django_filters.rest_framework
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from .serializers import ProductSerializer
from .permissions import IsAdminOrReadOnly
from core.models import Product



class PaginationProductModelViewSet(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 1000


class ProductModelViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_published=True)
    serializer_class = ProductSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PaginationProductModelViewSet
    filterset_fields = ['categories', 'color', 'finish_type', "volume", "height", "weight", "diameter", "slug", "is_published"]
