from typing import Any

from django.conf import settings
from django.views.generic import TemplateView


class MainPageView(TemplateView):

    template_name = "main_page.haml"

    def get_context_data(self, **kwargs: Any) -> dict:
        context_data = super().get_context_data(**kwargs)
        context_data["google_api_key"] = settings.GOOGLE_API_KEY
        return context_data
