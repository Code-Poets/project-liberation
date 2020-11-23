import factory
from factory.django import DjangoModelFactory
from faker import Faker

from company_website.models import Employees
from company_website.models import EstimateProjectEmailRecipients


class EmployeeFactory(DjangoModelFactory):
    class Meta:
        model = Employees

    name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    position = factory.LazyAttributeSequence(lambda o, n: f"{Faker().job()[:50]}")


class BossFactory(EmployeeFactory):
    boss = True


class EstimateProjectEmailRecipientsFactory(DjangoModelFactory):
    class Meta:
        model = EstimateProjectEmailRecipients

    name = factory.Faker("email")
