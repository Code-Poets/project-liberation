import os
from typing import Any

from django.conf import settings
from django.contrib import messages
from django.http import HttpRequest
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.views.generic import ListView

from common.helpers import read_file
from company_website.constants import ESTIMATE_PROJECT_EMAIL_SUBJECT
from company_website.constants import ESTIMATE_PROJECT_EMAIL_TEMPLATE_NAME
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
    email_template_name = ESTIMATE_PROJECT_EMAIL_TEMPLATE_NAME
    form_class = ProjectToEstimateForm
    page_name = PageNames.ESTIMATE_PROJECT.name

    def get_context_data(self, *, _object_list: Any = None, **kwargs: Any) -> dict:
        context_data = super().get_context_data(**kwargs)
        context_data["URL_PREFIX"] = settings.URL_PREFIX
        context_data = add_meta_tags_to_page_context(page_name=self.page_name, context_data=context_data)
        return context_data

    def form_valid(self, form: ProjectToEstimateForm) -> bool:
        messages.success(self.request, "Profile details updated.")
        form.save()

        if form.is_valid():
            send_mail_to_management(
                email_data=form.cleaned_data,
                email_subject=ESTIMATE_PROJECT_EMAIL_SUBJECT,
                template=self.email_template_name,
            )

        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy("thank_you")


class ThankYouView(CustomTemplateView):
    template_name = "thank_you.haml"
    page_name = PageNames.THANK_YOU.name


def display_playbook_view(request: HttpRequest) -> HttpResponse:
    playbook_file_name = "CodePoetsPlaybook.pdf"
    playbook_path = os.path.join(settings.STATIC_ROOT, "how_we_work", "files", playbook_file_name)

    if request.method == "GET":
        if os.path.isfile(playbook_path):
            response = HttpResponse(read_file(playbook_path), content_type="application/pdf")
            response["Content-Disposition"] = f"filename={playbook_file_name}"
            return response
        return HttpResponse(status=404)
    return HttpResponse(status=405)
