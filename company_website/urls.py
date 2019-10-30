from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r"^$", views.MainPageView.as_view(), name="main_page"),
    url(r"^team-introduction/$", views.TeamIntroductionPageView.as_view(), name="team_introduction"),
    url(r"^how-we-work/$", views.HowWeWorkView.as_view(), name="how_we_work"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
