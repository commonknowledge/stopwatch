from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from django.urls import include, path, re_path
from django.contrib import admin
from django.views.generic.base import TemplateView
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail_transfer import urls as wagtailtransfer_urls
from wagtail_content_import import urls as wagtail_content_import_urls

from commonknowledge.django import rest

from search import views as search_views


urlpatterns = [
    path('django-admin/', admin.site.urls),

    path('admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),

    path('search/', search_views.SearchView.as_view(), name='search'),
    path('api/', include(rest.get_urls())),
]


if settings.DEBUG:
    urlpatterns += (
        path('404/', TemplateView.as_view(template_name='404.html')),
        path('500/', TemplateView.as_view(template_name='500.html')),
    )

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

urlpatterns += [
    re_path(r'^wagtail-transfer/', include(wagtailtransfer_urls)),
    path("", include(wagtail_urls)),
]

urlpatterns += [
    re_path(r'', include(wagtail_content_import_urls)),
]
