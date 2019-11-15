from django.contrib import admin
from sorl.thumbnail.admin import AdminImageMixin

from company_website.models import Employees
from company_website.models import ProjectToEstimate
from company_website.models import Testimonial


class EmployeesAdmin(AdminImageMixin, admin.ModelAdmin):
    model = Employees
    list_display = ("order", "name", "position", "boss")


class ProjectToEstimateAdmin(admin.ModelAdmin):
    model = ProjectToEstimate
    list_display = ("name", "creation_date", "email", "nda_required", "idea_description")


admin.site.register(Employees, EmployeesAdmin)
admin.site.register(Testimonial)
admin.site.register(ProjectToEstimate, ProjectToEstimateAdmin)
