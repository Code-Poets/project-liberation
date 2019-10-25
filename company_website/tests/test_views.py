from django.test import TestCase
from django.urls import reverse

from company_website.factories import BossFactory
from company_website.factories import EmployeeFactory
from company_website.models import Employees


class TeamIntroductionViewTests(TestCase):
    def setUp(self):
        self.url = reverse("team_introduction")
        self.list_of_bosses = [BossFactory() for _ in range(2)]
        self.list_of_employees = [EmployeeFactory() for _ in range(10)]

    def test_get_context_data_return_data_with_bosses_and_employees(self):
        response = self.client.get(self.url)
        self.assertEqual(
            list(response.context_data["bosses"]), list(Employees.objects.filter(boss=True).order_by("order"))
        )
        self.assertEqual(
            list(response.context_data["employees"]), list(Employees.objects.filter(boss=False).order_by("order"))
        )
