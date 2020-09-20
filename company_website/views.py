from typing import Any

from django.conf import settings
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.views.generic import ListView

from company_website.constants import PageNames
from company_website.forms import ProjectToEstimateForm
from company_website.models import Employees
from company_website.models import Testimonial
from company_website.send_emails_utils import send_mail_to_management
from company_website.view_helpers import CustomTemplateView
from company_website.view_helpers import GoogleAdsMixin
from company_website.view_helpers import add_meta_tags_to_page_context


class MainPageView(ListView, GoogleAdsMixin):

    template_name = "main_page.haml"
    model = Testimonial
    page_name = PageNames.MAIN_PAGE.name

    def get_context_data(self, **kwargs: Any) -> dict:
        context_data = super().get_context_data(**kwargs)
        context_data["google_api_key"] = settings.GOOGLE_API_KEY
        context_data = add_meta_tags_to_page_context(page_name=self.page_name, context_data=context_data)
        return context_data


class TeamIntroductionPageView(ListView, GoogleAdsMixin):

    template_name = "team_introduction_page.haml"
    model = Employees
    page_name = PageNames.TEAM_INTRODUCTION.name

    def get_context_data(self, *, _object_list: Any = None, **kwargs: Any) -> dict:
        context_data = super().get_context_data(**kwargs)
        context_data["bosses"] = self.model._get_bosses()
        context_data["employees"] = self.model._get_employees()
        context_data = add_meta_tags_to_page_context(page_name=self.page_name, context_data=context_data)
        return context_data


class HowWeWorkView(CustomTemplateView):

    template_name = "how_we_work_page.haml"
    page_name = PageNames.HOW_WE_WORK.name


class CareerPageView(CustomTemplateView):

    template_name = "career.haml"
    page_name = PageNames.CAREER.name


class PrivacyAndPolicyView(CustomTemplateView):

    template_name = "privacy_and_policy_page.haml"
    page_name = PageNames.PRIVACY_AND_POLICY.name


class EstimateProjectView(FormView, GoogleAdsMixin):

    template_name = "estimate_project.haml"
    email_template_name = "estimate_project/estimate_project_email.html"
    form_class = ProjectToEstimateForm
    page_name = PageNames.ESTIMATE_PROJECT.name

    def get_context_data(self, *, _object_list: Any = None, **kwargs: Any) -> dict:
        context_data = super().get_context_data(**kwargs)
        context_data["URL_PREFIX"] = settings.URL_PREFIX
        return context_data

    def form_valid(self, form: ProjectToEstimateForm) -> bool:
        messages.success(self.request, "Profile details updated.")
        form.save()

        if form.is_valid():
            send_mail_to_management(
                email_data=form.cleaned_data,
                email_subject="Project Liberation: New estimate project form has been filled in",
                template=self.email_template_name,
            )

        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy("thank_you")


class ThankYouView(CustomTemplateView):
    template_name = "thank_you.haml"
    page_name = PageNames.THANK_YOU.name
