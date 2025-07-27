from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseNotFound
from .models import FooterInfo, ContactInfo, AboutInfo, IndexContent, Product, Category
from .forms import ContactUsForm, UserMessage

menu = [
    {"title": "Home", "name": "home"},
    {"title": "About us", "name": "about"},
    {"title": "Products", "name": "products"},
    {"title": "Contact us", "name": "contact"},
]

def index(request):
    index_content = IndexContent.objects.first() 
    return render(request, "GlassPack_site/index.html", context={"menu": menu, "title": "Home", "index_content": index_content})


def about_us(request):
    about_text = AboutInfo.objects.first()
    return render(request, "GlassPack_site/about.html", context={"menu": menu, "title": "About us", "about_text":about_text})


def products(request):
    selected_types = request.GET.get('categories', '')
    selected_types = selected_types.split(',') if selected_types else ['bottles', 'jars']

    selected_categories = Category.objects.filter(name__in=selected_types)
    
    selected_production = Product.objects.filter(categories__in=selected_categories, is_published=True)

    data = {
        'menu': menu,
        'title': 'Products', 
        'selected_types': selected_types,
        'selected_production': selected_production
    }
    return render(request, "GlassPack_site/products.html", context=data)


def contact_us(request):
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
    form = ContactUsForm()

    contact_info = FooterInfo.objects.first()
    contact_subtitle = ContactInfo.objects.first()
    data = {
        'menu': menu,
        'title': "Contact us",
        'contact_info': contact_info,
        'contact_subtitle': contact_subtitle,
        'form': form
    }
    return render(request, "GlassPack_site/contact.html", context=data)


def show_product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, "GlassPack_site/show_product.html", context={"menu":menu, "product": product})


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
