from typing import Any
from typing import Dict

from django.views.generic import TemplateView

from company_website.models import PageSeo


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
