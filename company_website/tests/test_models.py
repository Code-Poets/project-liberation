from django.test import TestCase

from company_website.factories import EmployeeFactory
from company_website.models import Employees


class TestEmployees(TestCase):
    def setUp(self) -> None:
        self.list_of_employees = [EmployeeFactory() for _ in range(10)]

    def test_create_model_set_last_possible_order_number(self):
        self.assertEqual(len(self.list_of_employees), Employees.objects.order_by("order").last().order)

    def test_method_should_create_employee_with_first_possible_order_number(self):
        employee_to_delete = Employees.objects.all().order_by("order")[5]
        employee_to_delete_order = employee_to_delete.order
        employee_to_delete.delete()
        created_employee = EmployeeFactory()
        self.assertEqual(created_employee.order, employee_to_delete_order)
