from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('products/', views.products, name='products'),
    path('about_us/', views.about_us, name='about'),
    path('contact_us/', views.contact_us, name='contact'),
]
