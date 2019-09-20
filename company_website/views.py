from django.views.generic import TemplateView


class MainPageView(TemplateView):

    template_name = "main_page.haml"


class TeamIntroductionPageView(TemplateView):

    template_name = "team_introduction_page.haml"
