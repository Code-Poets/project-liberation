from django.conf.urls import url
from django.contrib import admin
from django.urls import include

urlpatterns = [
    url(r"^admin/", admin.site.urls),
    url(r"^", include("company_website.urls")),
    url(r"^blog/", include("blog.urls")),
    url(r"^blog-cms/", include("blog.urls_admin")),
]
