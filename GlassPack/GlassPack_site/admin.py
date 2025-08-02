from cProfile import label
from django.contrib import admin
from django.utils.safestring import mark_safe
from GlassPack_site.models import Product, Category, FooterInfo, IndexContent, AboutInfo, ContactInfo, UserMessage
# Register your models here.

#Filter classes

class VolumeFilter(admin.SimpleListFilter):
    title = 'Volume'
    parameter_name = 'container_volume'

    def lookups(self, request, model_admin):
        return [('0-249', '0-249 ml'),
                ('250-349', '250-349 ml'),
                ('350-499', '350-499 ml'),
                ('500-749', '500-749 ml'),
                ('750-999', '750-999 ml'),
                ('1000-1249', '1000-1249 ml'),
                ('1250-1499', '1250-1499 ml'),
                ('1500-1999', '1500-1999 ml'),
                ('2000+', '2000ml+')]

    def queryset(self, request, queryset):
        value = self.value()
        if not value:
            return queryset 

        ranges = {
            '0-249': (0, 249),
            '250-349': (250, 349),
            '350-499': (350, 499),
            '500-749': (500, 749),
            '750-999': (750, 999),
            '1000-1249': (1000, 1249),
            '1250-1499': (1250, 1499),
            '1500-1999': (1500, 1999),}

        if value == '2000ml+':
            return queryset.filter(volume__gte=2000)
        
        if value in ranges:
            lower, upper = ranges[value]
            return queryset.filter(volume__range=(lower, upper))


#Production classes

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'model', 'product_photo', 'time_create', 'is_published')
    list_display_links = ('id', 'model', 'time_create')
    readonly_fields = ['product_photo']
    ordering = ('time_create',)
    list_editable = ('is_published',)
    list_per_page = 10
    search_fields = ('model', )
    list_filter = (VolumeFilter,'is_published', 'categories')
    save_on_top = True

    
    def volume_filter(self, request, queryset):
        if self.volume < 300:
            return queryset.filter(volume__lt=300)
        
    @admin.display(ordering='id')
    def product_photo(self, product: Product):
        return mark_safe(f"<img src='{product.image.url}' width='50'>")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    list_per_page = 10

#Pages classes

@admin.register(FooterInfo)
class FooterInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'company_name', 'address', 'work_time', 'email', 'phone')
    list_display_links = ('id', 'company_name', 'address', 'work_time', 'email', 'phone')


@admin.register(IndexContent)
class IndexContentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'subtitle',)
    list_display_links = ('id', 'title', 'subtitle', )


@admin.register(AboutInfo)
class AboutInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'content')
    list_display_links = ('id', 'content')


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'subtitle')
    list_display_links = ('id', 'subtitle')

#Forms

@admin.register(UserMessage)
class UserMessageAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'date']
    list_display_links = ['full_name', 'email', 'date']
    ordering = ['-date']
    list_per_page = 20
    search_fields = ['full_name', 'email']

    