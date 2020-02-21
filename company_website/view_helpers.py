import hashlib
from base64 import b64encode
from typing import Any
from typing import Dict

import requests
from django.views.generic import TemplateView
from requests.exceptions import Timeout

from company_website.models import PageSeo

REQUESTS_TIMOUT = 3


class CustomTemplateView(TemplateView):
    page_name = ""

    def get_context_data(self, **kwargs: Any) -> Dict:
        context_data = super().get_context_data(**kwargs)
        context_data = add_meta_tags_to_page_context(page_name=self.page_name, context_data=context_data)
        return context_data


def add_meta_tags_to_page_context(page_name: str, context_data: Dict) -> Dict:
    try:
        page_seo = PageSeo.objects.get(page_name=page_name)
    except PageSeo.DoesNotExist:
        return context_data
    context_data["title"] = page_seo.title
    context_data["meta_description"] = page_seo.meta_description
    context_data["keywords"] = page_seo.keywords
    return context_data


def generate_subresource_integrity_sha384(url: str) -> str:
    try:
        response = requests.get(url, timeout=REQUESTS_TIMOUT)
        sha = hashlib.sha384()
        sha.update(response.content)
        sha_diget = b64encode(sha.digest())
        return "sha384-" + sha_diget.decode()
    except Timeout:
        return ""
