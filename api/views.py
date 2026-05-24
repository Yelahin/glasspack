from django.contrib.auth import get_user_model
import django_filters.rest_framework
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import UserMessageSerializer, ProductSerializer, UserSerializer
from .permissions import IsAdminOrReadOnly, IsAdminUserOrUnauthorizedUserOnlyCreate
from core.models import Product
from users.models import UserMessage
from rest_framework import status


# Create your views here.


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


class UserMessageView(generics.CreateAPIView):
    queryset = UserMessage.objects.all()
    serializer_class = UserMessageSerializer
    permission_classes = [IsAuthenticated]


class UserModelViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUserOrUnauthorizedUserOnlyCreate]


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@api_view(['POST'])
def register_user(request):
    user = UserSerializer(data=request.data)
    if user.is_valid():
        user.save()
        return Response(
            data={"message": "User was successfully created!"},
            status=status.HTTP_201_CREATED
        )
    else:
        return Response(
            data={"message": user.errors},
            status=status.HTTP_400_BAD_REQUEST
        )