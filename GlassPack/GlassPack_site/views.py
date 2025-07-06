from django.shortcuts import render
from django.http import HttpResponseNotFound
from .models import FooterInfo

menu = [
    {"title": "Home", "name": "home"},
    {"title": "About us", "name": "about"},
    {"title": "Products", "name": "products"},
    {"title": "Contact us", "name": "contact"},
]

def index(request):
    return render(request, "GlassPack_site/index.html", context={"menu": menu, "title": "Home",})


def about_us(request):
    return render(request, "GlassPack_site/about.html", context={"menu": menu, "title": "About us"})


def products(request):
    return render(request, "GlassPack_site/products.html", context={"menu": menu, "title": "Products"})


def contact_us(request):
    return render(request, "GlassPack_site/contact.html", context={"menu": menu, "title": "Contact us"})


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
