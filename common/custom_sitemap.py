from django.contrib.sitemaps import Sitemap


class CustomSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5
    protocol = "https"
