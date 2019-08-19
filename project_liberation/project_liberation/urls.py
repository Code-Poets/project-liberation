from django.conf.urls import url
from django.contrib import admin
from django.urls import include

urlpatterns = [url(r"^admin/", admin.site.urls), url(r"^", include("main_page.urls"))]
