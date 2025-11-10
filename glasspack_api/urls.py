from django.urls import path, include
from .views import ProductModelViewSet, UserMessageView, UserModelViewSet, me
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'products', ProductModelViewSet, basename="products")
router.register(r'users', UserModelViewSet, basename="users")


urlpatterns = [
    path('', include(router.urls)),
    path('contacts/', UserMessageView.as_view(), name="contacts"),
    path('me/', me, name="me")
]