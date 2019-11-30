from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import include
from wagtail.admin import urls as wagtail_admin_urls
from wagtail.core import urls as wagtail_core_urls

from blog.views import search

urlpatterns = [
    url(r"^search/$", search, name="search"),
    url(r"^admin/", include(wagtail_admin_urls)),
    url(r"", include(wagtail_core_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
