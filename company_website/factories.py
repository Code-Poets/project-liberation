import factory
from factory import DjangoModelFactory
from faker import Faker

from company_website.models import Employees


class EmployeeFactory(DjangoModelFactory):
    class Meta:
        model = Employees

    name = factory.Faker("first_name")
    position = factory.LazyAttributeSequence(lambda o, n: f"{Faker().job()[:50]}")


class BossFactory(EmployeeFactory):

    name = factory.Faker("name")
    boss = True
