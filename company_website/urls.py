from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r"^$", views.MainPageView.as_view(), name="main_page"),
    url(r"estimate-project/$", views.EstimateProjectView.as_view(), name="estimate_project"),
    url(r"^team-introduction/$", views.TeamIntroductionPageView.as_view(), name="team_introduction"),
    url(r"^how-we-work/$", views.HowWeWorkView.as_view(), name="how_we_work"),
    url(r"^privacy-and-policy/$", views.PrivacyAndPolicyView.as_view(), name="privacy_and_policy"),
    url(r"^thank-you/$", views.ThankYouView.as_view(), name="thank_you"),
    url(r"^CodePoetsPlaybook/$", views.PlaybookView.as_view(), name="display_playbook"),
    url(r"go-to-brand/$", views.GoToBrandProjectView.as_view(), name="go_to_brand"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
