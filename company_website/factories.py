from factory import DjangoModelFactory
from factory import Faker

from company_website.models import Employees


class EmployeeFactory(DjangoModelFactory):
    class Meta:
        model = Employees

    name = Faker("name")
    position = Faker("name")


class BossFactory(EmployeeFactory):

    boss = True
