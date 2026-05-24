from django.urls import path, include
from .views import ProductModelViewSet, UserMessageView, UserModelViewSet, me, register_user
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)


router = DefaultRouter()
router.register(r'products', ProductModelViewSet, basename="products")
router.register(r'users', UserModelViewSet, basename="users")


urlpatterns = [
    path('', include(router.urls)),
    path('contacts/', UserMessageView.as_view(), name="contacts"),
    path('me/', me, name="me"),
    path('register/', register_user, name="register"),
    path('token/', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('token/refresh/', TokenRefreshView.as_view(), name="token_refresh")
]