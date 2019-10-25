from django.contrib import admin
from sorl.thumbnail.admin import AdminImageMixin

from company_website.models import Employees


class EmployeesAdmin(AdminImageMixin, admin.ModelAdmin):
    model = Employees
    list_display = ("order", "name", "position", "boss")


admin.site.register(Employees, EmployeesAdmin)
