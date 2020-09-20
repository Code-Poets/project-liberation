from typing import List
from typing import Tuple

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from html2text import HTML2Text

from company_website.models import EstimateProjectEmailRecipients


def send_mail_to_management(email_data: dict, email_subject: str, template: str) -> None:
    (html_message, plain_text_message) = _create_messages_to_mail(template, email_data)
    recipient_list = _get_estimate_project_email_recipients()

    send_mail(
        subject=email_subject,
        message=plain_text_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipient_list,
        html_message=html_message,
    )


def _create_messages_to_mail(template: str, context: dict) -> Tuple[str, str]:
    html_message = render_to_string(template, context)
    plain_text_message = _convert_html_to_plain_text(html_message)
    return (html_message, plain_text_message)


def _get_estimate_project_email_recipients() -> List[str]:
    recipient_list = EstimateProjectEmailRecipients.objects.all().values_list("name")
    if not recipient_list.exists() or settings.USE_DEFAULT_RECIPIENTS:
        recipient_list = settings.DEFAULT_EMAIL_RECIPIENTS
    return recipient_list


def _convert_html_to_plain_text(html: str) -> str:
    converter = HTML2Text()
    converter.ignore_emphasis = True
    converter.ignore_links = True
    plain_text = converter.handle(html)
    return plain_text.rstrip()
