from django.urls import path, include
from .views import ProductModelViewSet, UserMessageView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'products', ProductModelViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('contact/', UserMessageView.as_view()),
]