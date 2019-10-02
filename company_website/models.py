from typing import Any
from typing import List
from typing import Optional

from django.conf import settings
from django.db import models
from django.db.models import BooleanField
from django.db.models import CharField
from django.db.models import PositiveSmallIntegerField
from sorl.thumbnail import ImageField


class Testimonial(models.Model):
    name = CharField(max_length=32)
    position = CharField(max_length=64)
    quote = CharField(max_length=300)
    image = ImageField(default=None, blank=True, upload_to=settings.TESTIMONIAL_PHOTOS_STORAGE)


class Employees(models.Model):
    name = CharField(max_length=50)
    position = CharField(max_length=50)
    front_image = ImageField(default=None, blank=True, upload_to=settings.COMPANY_EMPLOYEES_STORAGE)
    back_image = ImageField(default=None, blank=True, upload_to=settings.COMPANY_EMPLOYEES_STORAGE)
    boss = BooleanField(default=False)
    order = PositiveSmallIntegerField(unique=True, blank=True)

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

    def save(
        self, force_insert: bool = False, force_update: bool = False, using: Any = None, update_fields: Any = None
    ) -> None:
        if not isinstance(self.order, int):
            self.order = self._get_lowest_available_order_number()
        super().save()
