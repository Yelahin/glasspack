from django.urls import path, include
from .views import ProductModelViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'products', ProductModelViewSet, basename="products")

urlpatterns = [
    path('', include(router.urls)),
]