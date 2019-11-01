from typing import Any

from django.conf import settings
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.views.generic import ListView
from django.views.generic import TemplateView

from company_website.forms import ProjectToEstimateForm
from company_website.models import Employees
from company_website.models import Testimonial


class MainPageView(ListView):

    template_name = "main_page.haml"
    model = Testimonial

    def get_context_data(self, **kwargs: Any) -> dict:
        context_data = super().get_context_data(**kwargs)
        context_data["google_api_key"] = settings.GOOGLE_API_KEY
        return context_data


class TeamIntroductionPageView(ListView):

    template_name = "team_introduction_page.haml"
    model = Employees

    def get_context_data(self, *, _object_list: Any = None, **kwargs: Any) -> dict:
        context_data = super().get_context_data(**kwargs)
        context_data["bosses"] = self.get_queryset().filter(boss=True).order_by("order")
        context_data["employees"] = self.get_queryset().filter(boss=False).order_by("order")
        return context_data


class HowWeWorkView(TemplateView):

    template_name = "how_we_work_page.haml"


class CareerPageView(TemplateView):

    template_name = "career.haml"


class PrivacyAndPolicyView(TemplateView):

    template_name = "privacy_and_policy_page.haml"


class EstimateProjectView(FormView):
    template_name = "estimate_project.haml"
    form_class = ProjectToEstimateForm

    def form_valid(self, form):
        messages.success(self.request, "Profile details updated.")
        form.save()

        return super().form_valid(form)

    def get_success_url(self):
        print()
        return reverse_lazy("estimate_project")
