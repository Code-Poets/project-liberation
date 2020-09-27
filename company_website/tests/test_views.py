from django.test import TestCase
from django.urls import reverse

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

    def test_that_estimate_project_view_should_redirect_to_thank_you_view(self):
        response = self.client.post(path=reverse("estimate_project"), data=self.form_data, follow=True)
        self.assertRedirects(response, reverse("thank_you"))
