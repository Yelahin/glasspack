from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
    path('', views.index, name='home'),
    path('products/', views.products, name='products'),
    path('about/', views.about_us, name='about'),
    path('contact/', views.contact_us, name='contact'),
    path('products/<slug:slug>/', views.show_product, name='product_detail'),
]


admin.site.site_header = 'Admin panel'