from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from core.sitemaps import ProductsSitemap, StaticViewSitemap

sitemaps = {
    'product': ProductsSitemap,
    'static': StaticViewSitemap,
}

handler400 = 'core.views.handler400'
handler403 = 'core.views.handler403'
handler404 = 'core.views.handler404'
handler500 = 'core.views.handler500'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('accounts/', include('users.urls', namespace="users")),
    path('api/', include([
        path('', include('core.api.urls')),
        path('', include('users.api.urls')),
    ])),
    path('', include('social_django.urls', namespace="social")),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
