from unittest import mock

from django.test import TestCase
from django.urls import reverse

from company_website.constants import ESTIMATE_PROJECT_EMAIL_SUBJECT_BASE
from company_website.constants import ESTIMATE_PROJECT_EMAIL_TEMPLATE_NAME
from company_website.factories import BossFactory
from company_website.factories import EmployeeFactory


class TeamIntroductionViewTests(TestCase):
    def setUp(self):
        self.url = reverse("team_introduction")
        self.list_of_bosses = [BossFactory() for _ in range(2)]
        self.list_of_employees = [EmployeeFactory() for _ in range(10)]

    def test_get_context_data_return_data_with_bosses_and_employees(self):
        response = self.client.get(self.url)
        self.assertEqual(list(response.context_data["bosses"]), self.list_of_bosses)
        self.assertEqual(list(response.context_data["employees"]), self.list_of_employees)

    def test_that_get_context_data_return_bosses_and_employees_which_are_working(self):
        new_employees_list = self.list_of_employees + [EmployeeFactory(is_working=False) for _ in range(5)]
        self.assertEqual(len(new_employees_list), 15)
        response = self.client.get(self.url)
        self.assertEqual(list(response.context_data["bosses"]), self.list_of_bosses)
        self.assertEqual(list(response.context_data["employees"]), self.list_of_employees)


class EstimateProjectViewTests(TestCase):
    def setUp(self) -> None:
        self.form_data = {
            "name": "John Doe",
            "email": "email@address.com",
            "idea_description": "Some description",
            "privacy_policy_accepted": True,
        }
        self.expected_mocked_mail_called = {
            "email_data": {
                "name": "John Doe",
                "email": "email@address.com",
                "idea_description": "Some description",
                "privacy_policy_accepted": True,
            },
            "email_subject": f"{ESTIMATE_PROJECT_EMAIL_SUBJECT_BASE} John Doe",
            "template": ESTIMATE_PROJECT_EMAIL_TEMPLATE_NAME,
        }

    @mock.patch("company_website.send_emails_utils.EmailMessage")
    def test_that_estimate_project_view_should_redirect_to_thank_you_view(self, _):
        response = self.client.post(path=reverse("estimate_project"), data=self.form_data, follow=True)
        self.assertRedirects(response, reverse("thank_you"))

    @mock.patch("company_website.views.send_mail_to_management")
    def test_that_valid_form_will_trigger_mail_sending(self, mocked_mail):
        response = self.client.post(path=reverse("estimate_project"), data=self.form_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(mocked_mail.call_count, 1)
        mocked_mail.assert_called_with(**self.expected_mocked_mail_called)


class DisplayPlaybookViewTests(TestCase):
    def setUp(self) -> None:
        self.url = reverse("display_playbook")

    def test_that_display_playbook_view_should_display_file_on_get(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("application/pdf", str(response))

    def test_that_display_playbook_view_should_return_method_not_allowed_status_code_on_post(self):
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 405)

    @mock.patch("os.path.isfile")
    def test_that_display_playbook_view_should_return_404_status_code_when_file_does_not_exist(self, mocked_function):
        mocked_function.return_value = False
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 404)
