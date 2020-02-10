from typing import List

from django.urls import reverse

from common.custom_sitemap import CustomSitemap


class CompanyWebsiteViewSitemap(CustomSitemap):
    def items(self) -> List[str]:
        return ["main_page", "estimate_project", "team_introduction", "how_we_work", "privacy_and_policy"]

    def location(self, item: str) -> str:
        return reverse(item)
