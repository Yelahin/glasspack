from django.urls import path, include
from .views import ProductModelViewSet, UserMessageView, UserModelViewSet, me
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'products', ProductModelViewSet)
router.register(r'users', UserModelViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('contact/', UserMessageView.as_view()),
    path('me/', me)
]