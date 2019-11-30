from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import include
from wagtail.admin import urls as wagtail_admin_urls
from wagtail.core import urls as wagtail_core_urls

from blog.views import search

urlpatterns = [
    # blog post search engine
    url(r"^search/$", search, name="search"),
    # wagtail admin
    url(r"^admin/", include(wagtail_admin_urls)),
    # blog slugs
    url(r"", include(wagtail_core_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
