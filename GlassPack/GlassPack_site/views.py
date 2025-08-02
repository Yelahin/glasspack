from django.http import HttpResponseNotFound
from django.urls import reverse_lazy
from .utils import DataMixin
from .models import FooterInfo, ContactInfo, AboutInfo, IndexContent, Product, Category
from .forms import ContactUsForm
from django.views.generic import DetailView, FormView, ListView, TemplateView


class IndexPage(DataMixin, TemplateView):
    template_name = "GlassPack_site/index.html"
    title = 'Home'
    page_content = IndexContent.objects.first()


class AboutUsPage(DataMixin, TemplateView):
    template_name = "GlassPack_site/about.html"
    title = "About us"
    page_content = AboutInfo.objects.first()


class ProductPage(DataMixin, ListView):
    template_name = "GlassPack_site/products.html"
    context_object_name = 'selected_production'
    allow_empty = False
    paginate_by = 6

    def get_queryset(self):
        selected_types = self.request.GET.get('categories', '')
        selected_types = selected_types.split(',') if selected_types else ['bottles', 'jars']
        self.selected_types = selected_types
        selected_categories = Category.objects.filter(name__in=self.selected_types)
        return Product.objects.filter(categories__in=selected_categories, is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_types'] = getattr(self, 'selected_types', ['bottles', 'jars'])
        return self.get_mixin_content(context, title='Products')
    

class ContactUsPage(DataMixin, FormView):
    form_class = ContactUsForm
    template_name = "GlassPack_site/contact.html"
    success_url = reverse_lazy('contact')
    title = "Contact us"
    extra_context = {'contact_info': FooterInfo.objects.first(),
                     'contact_subtitle': ContactInfo.objects.first()}

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class ShowProduct(DataMixin, DetailView):
    model = Product
    template_name = "GlassPack_site/show_product.html"
    context_object_name = 'product'
    slug_url_kwarg = 'slug'
    

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
