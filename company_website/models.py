from typing import Any
from typing import List
from typing import Optional

from django.conf import settings
from django.db import models
from django.db.models import BooleanField
from django.db.models import CharField
from django.db.models import EmailField
from django.db.models import PositiveSmallIntegerField
from django.db.models import QuerySet
from sorl.thumbnail import ImageField

from company_website.constants import PageNames


class Testimonial(models.Model):
    name = CharField(max_length=32)
    position = CharField(max_length=64)
    quote = CharField(max_length=300)
    image = ImageField(default=None, blank=True, upload_to=settings.TESTIMONIAL_PHOTOS_STORAGE)

    def __str__(self) -> str:
        return self.name


class Employees(models.Model):
    name = CharField(max_length=50)
    last_name = CharField(max_length=50, blank=True)
    display_name = CharField(max_length=50, blank=True)
    position = CharField(max_length=50)
    front_image = ImageField(default=None, blank=True, upload_to=settings.COMPANY_EMPLOYEES_STORAGE)
    back_image = ImageField(default=None, blank=True, upload_to=settings.COMPANY_EMPLOYEES_STORAGE)
    boss = BooleanField(default=False)
    order = PositiveSmallIntegerField(unique=True, blank=True)
    is_working = BooleanField(default=True)
    bio = CharField(max_length=300, blank=True)

    def __str__(self) -> str:
        return self.full_name

    @property
    def full_name(self) -> str:
        return f"{self.name} {self.last_name}"

    def get_display_name(self) -> str:
        if len(self.display_name) > 0:
            return self.display_name
        return self.name

    @staticmethod
    def _get_all_order_numbers() -> List[Optional[int]]:
        employees = Employees.objects.all().order_by("order")
        if len(employees) > 0:
            return [employee.order for employee in employees]
        else:
            return []

    def _get_lowest_available_order_number(self) -> int:
        order_list = self._get_all_order_numbers()
        if len(order_list) > 0:
            order_numbers_range = [x for x in range(1, max(order_list) + 1)]  # type: ignore
            new_order_list = list(set(order_numbers_range) - set(order_list))
            if not len(new_order_list) > 0:
                return max(order_list) + 1  # type: ignore
            else:
                return min(list(set(order_numbers_range) - set(order_list)))
        else:
            return 1

    @staticmethod
    def _get_bosses() -> QuerySet:
        return Employees.objects.filter(boss=True, is_working=True).order_by("order")

    @staticmethod
    def _get_employees() -> QuerySet:
        return Employees.objects.filter(boss=False, is_working=True).order_by("order")

    def save(
        self, force_insert: bool = False, force_update: bool = False, using: Any = None, update_fields: Any = None
    ) -> None:
        if not isinstance(self.order, int):
            self.order = self._get_lowest_available_order_number()
        super().save()


class EstimateProject(models.Model):
    def __str__(self) -> str:
        return f"{self.creation_date} {self.email}"

    creation_date = models.DateField(auto_now_add=True)

    name = models.CharField(max_length=60)
    email = models.EmailField(max_length=60)
    idea_description = models.TextField(max_length=10000)
    privacy_policy_accepted = models.BooleanField(default=False)


class PageSeo(models.Model):
    def __str__(self) -> str:
        return self.page_name

    page_name = models.CharField(max_length=40, choices=PageNames.choices(), unique=True)
    title = models.CharField(max_length=80)
    meta_description = models.CharField(max_length=168)
    keywords = models.CharField(max_length=512)

    class Meta:
        verbose_name = "Page SEO"
        verbose_name_plural = "Pages SEO"


class EstimateProjectEmailRecipients(models.Model):
    class Meta:
        verbose_name = "Estimate Project Email Recipients"
        verbose_name_plural = "Estimate Project Email Recipients"

    def __str__(self) -> str:
        return str(self.name)

    name = EmailField()
