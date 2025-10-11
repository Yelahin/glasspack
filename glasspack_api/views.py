from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.decorators import action 
from rest_framework.response import Response
from .serializers import UserMessageSerializer, ProductSerializer, SelectedFiltersSerializer
from .permissions import IsAdminOrReadOnly
from glasspack_site.models import Product
from glasspack_users.models import UserMessage
from glasspack_site.utils import ProductPageContext


# Create your views here.


class PaginationProductModelViewSet(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 1000


class ProductModelViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_published=True)
    serializer_class = ProductSerializer
    lookup_field = "slug"
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PaginationProductModelViewSet

    @action(detail=False, methods=['get'])
    def parameters(self, request):
        page_context = ProductPageContext(request)
        instance = {
            "selected_types": page_context.get_selected_types(),
            "selected_finish_types": page_context.get_selected_obj("finish_type"),
            "selected_colors": page_context.get_selected_obj("color"),
            "all_finish_types": page_context.get_obj_with_count("finish_type"),
            "all_colors": page_context.get_obj_with_count("color")
        }

        serializer = SelectedFiltersSerializer(instance=instance)
        return Response(serializer.data)
    
    
class UserMessageView(generics.CreateAPIView):
    queryset = UserMessage.objects.all()
    serializer_class = UserMessageSerializer

