from django.shortcuts import  render
from django.urls import reverse_lazy
from .utils import DataMixin, ProductPageContext
from .models import  AboutInfo, IndexContent, Product, FooterInfo, ContactInfo
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
        self.data = ProductPageContext(self.request).get_all_data()
        return self.data['products']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_types'] = self.data.get('selected_types', ['bottles', 'jars'])
        context['filtered_finish_products'] = self.data['filtered_finish_products']
        context['filtered_color_products'] = self.data['filtered_color_products']
        context['selected_finish_types'] = self.data['selected_finish_types']
        context['selected_colors'] = self.data['selected_colors']
        context['querystring'] = self.data['querydict'].urlencode()

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
