from urllib.parse import urlencode
from django.urls import include, path
from . import views
from django.contrib import admin

urlpatterns = [
    path('', views.IndexPage.as_view(), name='home'),
    path('products', views.ProductPage.as_view(), name='products'),
    path('about/', views.AboutUsPage.as_view(), name='about'),
    path('contact/', views.ContactUsPage.as_view(), name='contact'),
    path('products/<slug:slug>/', views.ShowProduct.as_view(), name='product_detail'),
    path('captcha/', include('captcha.urls'))
]


admin.site.site_header = 'Admin panel'