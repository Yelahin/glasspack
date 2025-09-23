from django.db.models import Count 
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.urls import reverse_lazy
from .utils import DataMixin
from .models import  AboutInfo,  IndexContent, Product, Category, FooterInfo, ContactInfo
from .forms import ContactUsForm
from django.views.generic import DetailView, FormView, ListView, TemplateView


class IndexPage(DataMixin, TemplateView):
    template_name = "glasspack_site/index.html"
    title = 'Home'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_content'] = IndexContent.objects.first() or ''
        return context


class AboutUsPage(DataMixin, TemplateView):
    template_name = "glasspack_site/about.html"
    title = "About us"
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_content'] = AboutInfo.objects.first() or ''
        return context


class ProductPage(DataMixin, ListView):
    template_name = "glasspack_site/products.html"
    context_object_name = 'selected_production'
    paginate_by = 6


    def get_queryset(self):
        #all objects from db
        all_cats = Category.objects.values_list('name', flat=True).distinct()

        #template urls + template filters
        selected_types = self.request.GET.get('categories', '')
        self.selected_types = selected_types.split(',') if selected_types else all_cats

        qs = Product.objects.filter(is_published=True, categories__name__in=self.selected_types)

        self.selected_finish_types = self.request.GET.getlist('finish_types') 
        self.selected_colors = self.request.GET.getlist('colors')

        #get_queryset return
        checked_finish_types = self.selected_finish_types or qs.values_list('finish_type__name', flat=True).distinct()
        checked_color = self.selected_colors or qs.values_list('color__name', flat=True).distinct()

        #pagination url
        self.querydict = self.request.GET.copy()
        if 'page' in self.querydict:
            self.querydict.pop('page')

        self.filtered_finish_products = qs.filter(color__name__in=checked_color).values('finish_type__name').annotate(count=Count('finish_type'))
        self.filtered_color_products = qs.filter(finish_type__name__in=checked_finish_types).values('color__name').annotate(count=Count('color'))

        #get_queryset return
        products = qs.filter(finish_type__name__in=checked_finish_types, color__name__in=checked_color).order_by("model")
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_types'] = getattr(self, 'selected_types', ['bottles', 'jars'])
        context['filtered_finish_products'] = self.filtered_finish_products
        context['filtered_color_products'] = self.filtered_color_products
        context['selected_finish_types'] = self.selected_finish_types
        context['selected_colors'] = self.selected_colors
        context['querystring'] = self.querydict.urlencode()

        return self.get_mixin_content(context, title='Products')
    

class ContactUsPage(DataMixin, FormView):
    form_class = ContactUsForm
    template_name = "glasspack_site/contact.html"
    success_url = reverse_lazy('contact')
    title = "Contact us"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact_info'] = FooterInfo.objects.first() or ''
        context['contact_subtitle'] = ContactInfo.objects.first()
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class ShowProduct(DataMixin, DetailView):
    model = Product
    template_name = "glasspack_site/show_product.html"
    context_object_name = 'product'
    slug_url_kwarg = 'slug'
    

def custom_400(request, exception):
    mixin = DataMixin()
    context = mixin.get_mixin_content({})
    return render(request, 'glasspack_site/errors/400.html', context, status=400)

def custom_403(request, exception):
    mixin = DataMixin()
    context = mixin.get_mixin_content({})
    return render(request, 'glasspack_site/errors/403.html', context, status=403)

def custom_404(request, exception):
    mixin = DataMixin()
    context = mixin.get_mixin_content({})
    return render(request, 'glasspack_site/errors/404.html', context, status=404)

def custom_500(request):
    mixin = DataMixin()
    context = mixin.get_mixin_content({})
    return render(request, 'glasspack_site/errors/500.html', context, status=500)
