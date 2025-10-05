from django.db.models import F, Count
from glasspack_site.models import Category, Product


#Pages in menu
menu = [
    {"title": "Home", "name": "home"},
    {"title": "About us", "name": "about"},
    {"title": "Products", "name": "products"},
    {"title": "Contact us", "name": "contact"},
]

#Data mixin for views classes 
class DataMixin:
    menu = None
    title = None
    page_content = None
    extra_context = {}

    def __init__(self):
        if 'menu' not in self.extra_context:
            self.extra_context['menu'] = menu

        if self.title is not None:
            self.extra_context['title'] = self.title

        if self.page_content is not None:
            self.extra_context['page_content'] = self.page_content


    def get_mixin_content(self, context, **kwargs):
        context['menu'] = menu
        context['title'] = self.title
        context['page_content'] = self.page_content
        context.update(kwargs)
        return context


#Context for product page filter
class ProductPageContext:
    def __init__(self, request):
        self.request = request
        self.qs = None

    def get_selected_types(self):
        all_cats = Category.objects.values_list('name', flat=True).distinct()
        selected_types = self.request.GET.get('categories', '')
        selected_types = selected_types.split(',') if selected_types else all_cats
        return selected_types

    def get_qs(self):
        if self.qs is None:
            self.qs = Product.objects.filter(is_published=True, categories__name__in=self.get_selected_types())
        return self.qs

    def get_selected_obj(self, obj_name):
        selected_obj = self.request.GET.getlist(f"{obj_name}s") 
        return selected_obj
    
    def get_querydict(self):
        querydict = self.request.GET.copy()
        if 'page' in querydict:
            querydict.pop('page')
        return querydict
    
    def get_checked_obj(self, obj_name):
        selected_obj = self.get_selected_obj(obj_name)
        checked_obj = selected_obj or self.get_qs().values_list(f"{obj_name}__name", flat=True).distinct()
        return checked_obj

    def get_obj_with_count(self, obj_name):
        result = self.get_qs().values(obj_name).annotate(name=F(f"{obj_name}__name") ,count=Count(obj_name)).values("name", "count")
        return result
    
    def get_products(self):
        finish_filter = self.get_checked_obj("finish_type")
        color_filter = self.get_checked_obj("color")
        result = self.get_qs().filter(finish_type__name__in=finish_filter, color__name__in=color_filter).order_by("model")
        return result 

    def get_all_data(self):
        all_data = {
            "selected_types": self.get_selected_types(),
            "filtered_finish_products": self.get_obj_with_count("finish_type"),
            "filtered_color_products": self.get_obj_with_count("color"),
            "selected_finish_types": self.get_selected_obj("finish_type"),
            "selected_colors": self.get_selected_obj("color"),
            "querydict": self.get_querydict(),
            "products": self.get_products(),
        }
        
        return all_data