from company_website.fields import ChoiceEnum


class EstimateConstants:
    product_choices = (("build", "Build something new"), ("improve", "Improve existing project"))
    budget_choices = (
        ("-8", "up to $8.000"),
        ("8-25", "$8.000 — $25.000"),
        ("25-100", "$25.000 — $100.000"),
        ("100+", "$100.000+"),
    )
    project_duration_choices = (("-3", "up to 3 months"), ("3-6", "3-6 months"), ("6+", "6+ months"))
    true_false_choices = ((True, "Yes"), (False, "No"))
    company_info_origin_choices = (
        ("Google", "Google"),
        ("Clutch", "Clutch.com"),
        ("Friend", "Friend"),
        ("Social Media", "Social Media"),
        ("Tech Event", "Tech Event"),
        ("Other", "Other"),
    )


class PageNames(ChoiceEnum):
    MAIN_PAGE = "Main Page"
    TEAM_INTRODUCTION = "Team Introduction"
    HOW_WE_WORK = "How we Work"
    CAREER = "Career"
    ESTIMATE_PROJECT = "Estimate Project"
    PRIVACY_AND_POLICY = "Privacy and Policy"
    THANK_YOU = "Thank You"
    GO_TO_BRAND_PROJECT = "Go to Brand"


ESTIMATE_PROJECT_EMAIL_SUBJECT_BASE = "Code Poets estimation for"
ESTIMATE_PROJECT_EMAIL_TEMPLATE_NAME = "estimate_project/estimate_project_email.html"
