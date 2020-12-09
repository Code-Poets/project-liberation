from unittest import mock

from django.conf import settings
from django.test import TestCase
from django.test import override_settings
from parameterized import parameterized

from company_website.constants import ESTIMATE_PROJECT_EMAIL_SUBJECT
from company_website.constants import ESTIMATE_PROJECT_EMAIL_TEMPLATE_NAME
from company_website.factories import EstimateProjectEmailRecipientsFactory
from company_website.send_emails_utils import _convert_html_to_plain_text
from company_website.send_emails_utils import _create_messages_to_mail
from company_website.send_emails_utils import _get_estimate_project_email_recipients
from company_website.send_emails_utils import send_mail_to_management


class EstimateProjectEmailRecipientsTestCase(TestCase):
    @override_settings(USE_DEFAULT_RECIPIENTS=True)
    def test_that_when_use_default_recipients_settings_is_enabled_method_returns_default_recipients_list(self):

        returned_recipients_list = _get_estimate_project_email_recipients()

        self.assertEqual(returned_recipients_list, settings.DEFAULT_EMAIL_RECIPIENTS)

    def test_that_when_recipient_list_is_empty_method_returns_default_email_recipients_list(self):
        returned_recipients_list = _get_estimate_project_email_recipients()

        self.assertEqual(returned_recipients_list, settings.DEFAULT_EMAIL_RECIPIENTS)

    def test_that_when_recipient_list_is_not_empty_and_default_recipient_settings_is_disabled_it_return_recipients_list(
        self,
    ):
        defined_recipient = EstimateProjectEmailRecipientsFactory()

        returned_recipients_list = list(_get_estimate_project_email_recipients())

        self.assertEqual(returned_recipients_list, [(defined_recipient.name,)])


class SendEmailTestCase(TestCase):
    def setUp(self) -> None:
        self.template = ESTIMATE_PROJECT_EMAIL_TEMPLATE_NAME
        self.template_context = {
            "name": "John Doe",
            "email": "email@address.com",
            "idea_description": "Some description",
            "privacy_policy_accepted": True,
        }

        self.expected_mail_body = (
            "Project Liberation - New estimate project form has been filled in.\n\n"
            "Form data:\n\n"
            "Name: John Doe\n\n"
            "Email address: email@address.com\n\n"
            "Idea description: Some description"
        )

    def test_that_create_messages_to_mail_method_create_proper_email_messages(self):
        plain_text_message = _create_messages_to_mail(self.template, self.template_context)[1]

        self.assertEqual(plain_text_message, self.expected_mail_body)

    @parameterized.expand(
        [
            ("<p> Some text </p>", "Some text"),
            ("<p> Some <a href='https://www.google.com/earth/'>text</p>", "Some text"),
            ("<p> Some <em>text</em> </p>", "Some text"),
        ]
    )
    def test_that_convert_html_to_plain_test_method_create_proper_message(
        self, html_message, expected_plain_text_message
    ):
        returned_value = _convert_html_to_plain_text(html_message)

        self.assertEqual(returned_value, expected_plain_text_message)

    @mock.patch("company_website.send_emails_utils.send_mail")
    def test_that_send_email_to_management_pass_proper_parameters_to_send_email_method(self, mocked_send_mail):
        send_mail_to_management(self.template_context, ESTIMATE_PROJECT_EMAIL_SUBJECT, self.template)

        email_subject = mocked_send_mail.call_args[1]["subject"]
        passed_message = mocked_send_mail.call_args[1]["message"]

        self.assertEqual(email_subject, ESTIMATE_PROJECT_EMAIL_SUBJECT)
        self.assertEqual(passed_message, self.expected_mail_body)
