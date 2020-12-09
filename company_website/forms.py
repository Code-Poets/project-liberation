from django import forms
from django.forms import ModelForm

from company_website.models import EstimateProject


class ProjectToEstimateForm(ModelForm):
    privacy_policy_accepted = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "policy-checkbox"}), required=True
    )

    class Meta:
        model = EstimateProject

        fields = [
            "name",
            "email",
            "idea_description",
            "privacy_policy_accepted",
        ]

    def form_valid(self, form: "ProjectToEstimateForm") -> bool:
        form.save()
        return super().form_valid(form)
