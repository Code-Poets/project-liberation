from django import forms
from django.forms import ModelForm

from company_website.constants import EstimateConstants
from company_website.models import EstimateProject


class ProjectToEstimateForm(ModelForm):

    nda_required = forms.ChoiceField(
        choices=EstimateConstants.true_false_choices, widget=forms.RadioSelect(), required=False
    )
    project_development = forms.ChoiceField(
        choices=EstimateConstants.product_choices, widget=forms.RadioSelect(), required=False
    )
    monthly_bugdet = forms.ChoiceField(
        choices=EstimateConstants.budget_choices, widget=forms.RadioSelect(), required=False
    )
    project_duration = forms.ChoiceField(
        choices=EstimateConstants.project_duration_choices, widget=forms.RadioSelect(), required=False
    )
    design_product = forms.ChoiceField(
        choices=EstimateConstants.true_false_choices, widget=forms.RadioSelect(), required=False
    )
    find_out_way = forms.ChoiceField(
        choices=EstimateConstants.company_info_origin_choices, widget=forms.RadioSelect(), required=False
    )
    privacy_policy_accepted = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "policy-checkbox"}), required=False
    )

    class Meta:
        model = EstimateProject

        fields = [
            "name",
            "email",
            "country",
            "idea_description",
            "nda_required",
            "privacy_policy_accepted",
            "project_development",
            "monthly_bugdet",
            "project_duration",
            "design_product",
            "company_info_origin",
        ]

    def form_valid(self, form: "ProjectToEstimateForm") -> bool:
        form.save()
        return super().form_valid(form)
