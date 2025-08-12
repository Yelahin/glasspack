from django.db.models import Count, Max, Min
from django.http import  HttpResponseNotFound
from django.urls import reverse_lazy
from .utils import DataMixin
from .models import  FooterInfo, ContactInfo, AboutInfo, IndexContent, Product, Category
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
    paginate_by = 6


    def get_queryset(self):
        #display min-max volume in template
        self.volumes = Product.objects.aggregate(min_volume=Min('volume'), max_volume=Max('volume'))

        #template urls + template filters
        selected_types = self.request.GET.get('categories', '')
        self.selected_types = selected_types.split(',') if selected_types else ['bottles', 'jars']
        self.selected_finish_types = self.request.GET.getlist('finish_types') 
        self.selected_colors = self.request.GET.getlist('colors')

        #get_queryset return
        checked_finish_types = self.selected_finish_types if self.selected_finish_types else Product.objects.filter(is_published=True).values_list('finish_type__name', flat=True).distinct()
        checked_color = self.selected_colors if self.selected_colors else Product.objects.filter(is_published=True).values_list('color__name', flat=True).distinct()

        #pagination url
        self.querydict = self.request.GET.copy()
        if 'page' in self.querydict:
            self.querydict.pop('page')

        #get objects from db
        selected_categories = Category.objects.filter(name__in=self.selected_types)
        min_volume = int(self.request.GET.get("slider_1")) if self.request.GET.get("slider_1") else self.volumes['min_volume']
        max_volume = int(self.request.GET.get("slider_2")) if self.request.GET.get("slider_2") else self.volumes['max_volume']
        self.filtered_finish_products = Product.objects.filter(categories__in=selected_categories, color__name__in=checked_color, volume__range=(min_volume, max_volume), is_published=True).values('finish_type__name').annotate(count=Count('finish_type'))
        self.filtered_color_products = Product.objects.filter(categories__in=selected_categories, finish_type__name__in=checked_finish_types, volume__range=(min_volume, max_volume), is_published=True).values('color__name').annotate(count=Count('color'))

        #get_queryset return
        products = Product.objects.filter(categories__in=selected_categories, volume__range=(min_volume, max_volume), finish_type__name__in=checked_finish_types, color__name__in=checked_color, is_published=True).order_by("model")
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_types'] = getattr(self, 'selected_types', ['bottles', 'jars'])
        context['min_volume'] = self.volumes['min_volume']
        context['max_volume'] = self.volumes['max_volume']
        context['filtered_finish_products'] = self.filtered_finish_products
        context['filtered_color_products'] = self.filtered_color_products
        context['selected_finish_types'] = self.selected_finish_types
        context['selected_colors'] = self.selected_colors
        context['querystring'] = self.querydict.urlencode()
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

