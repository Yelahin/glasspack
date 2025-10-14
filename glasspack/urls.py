from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from glasspack_site.sitemaps import ProductsSitemap, StaticViewSitemap


sitemaps = {
    'product': ProductsSitemap,
    'static': StaticViewSitemap,
}

handler400 = 'glasspack_site.views.custom_400'
handler403 = 'glasspack_site.views.custom_403'
handler404 = 'glasspack_site.views.custom_404'
handler500 = 'glasspack_site.views.custom_500'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('glasspack_site.urls')),
    path('', include('glasspack_users.urls', namespace="glasspack_users")),
    path('api/v1/', include('glasspack_api.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path('', include('social_django.urls', namespace="social")),
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)