from django import forms
from django.forms import ModelForm
from django.urls import reverse
from django.urls import reverse_lazy

from company_website.models import ProjectToEstimate


class ProjectToEstimateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    nda_choices = ((True, "Yes"), (False, "No"))
    nda_required = forms.ChoiceField(choices=nda_choices, widget=forms.RadioSelect(), required=False)

    build_or_improve = forms.ChoiceField(
        choices=ProjectToEstimate.I_want_to, widget=forms.RadioSelect(), required=False
    )
    monthly_bugdet = forms.ChoiceField(
        choices=ProjectToEstimate.budget_choices, widget=forms.RadioSelect(), required=False
    )
    project_time = forms.ChoiceField(choices=ProjectToEstimate.time_choices, widget=forms.RadioSelect(), required=False)
    design_product = forms.ChoiceField(
        choices=ProjectToEstimate.design_choices, widget=forms.RadioSelect(), required=False
    )
    company_info_origin = forms.ChoiceField(
        choices=ProjectToEstimate.company_info_choices, widget=forms.RadioSelect(), required=False
    )
    privacy_policy_accepted = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "policy-checkbox"}), required=False
    )

    class Meta:
        model = ProjectToEstimate

        fields = [
            "name",
            "email",
            "country",
            "idea_description",
            "nda_required",
            "privacy_policy_accepted",
            "build_or_improve",
            "monthly_bugdet",
            "project_time",
            "design_product",
            "company_info_origin",
        ]

    success_url = reverse_lazy("")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):  # pylint: disable: no-self-use
        return reverse("")
