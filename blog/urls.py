from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import include
from wagtail.core import urls as wagtail_core_urls

from blog.views import search

app_name = "blog"

urlpatterns = [
    url(r"^search/$", search, name="search"),
    url(r"", include((wagtail_core_urls, "company-blog"), namespace="company-blog")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
