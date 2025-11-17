from django.shortcuts import  render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import  ProductPageContext
from .models import Product
from glasspack_users.forms import ContactUsForm
from django.views.generic import DetailView, FormView, ListView, TemplateView
from glasspack import settings

class IndexPage(TemplateView):
    template_name = "glasspack_site/index.html"


class AboutUsPage(TemplateView):
    template_name = "glasspack_site/about.html"


class ProductPage(ListView):
    template_name = "glasspack_site/products.html"
    context_object_name = 'selected_production'
    paginate_by = settings.PRODUCT_PAGINATE_BY

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

        return context
    

class ContactUsPage(LoginRequiredMixin, FormView):
    form_class = ContactUsForm
    template_name = "glasspack_site/contact.html"
    success_url = reverse_lazy('contact')
    
    def form_valid(self, form):
        msg = form.save(commit=False)
        msg.user = self.request.user
        msg.save()
        return super().form_valid(form)


class ShowProduct(DetailView):
    model = Product
    template_name = "glasspack_site/show_product.html"
    context_object_name = 'product'
    slug_url_kwarg = 'slug'


def handler400(request, exception):
    return render(request, 'glasspack_site/errors/400.html', status=400)

def handler403(request, exception):
    return render(request, 'glasspack_site/errors/403.html', status=403)

def handler404(request, exception):
    return render(request, 'glasspack_site/errors/404.html', status=404)

def handler500(request):
    return render(request, 'glasspack_site/errors/500.html', status=500)