from django.urls import include
from django.urls import re_path
from wagtail.admin import urls as wagtail_admin_urls
from wagtail.core import urls as wagtail_core_urls

urlpatterns = [re_path(r"", include(wagtail_admin_urls)), re_path(r"", include(wagtail_core_urls))]
