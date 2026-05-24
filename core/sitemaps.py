from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Product


class ProductsSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.9

    def items(self):
        return Product.objects.filter(is_published=True)
        

class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return ['home', 'about', 'contact']
    
    def location(self, item):
        return reverse(item)
