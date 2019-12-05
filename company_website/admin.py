from django.contrib import admin
from sorl.thumbnail.admin import AdminImageMixin

from company_website.models import Employees
from company_website.models import EstimateProject
from company_website.models import PageSeo
from company_website.models import Testimonial


class EmployeesAdmin(AdminImageMixin, admin.ModelAdmin):
    model = Employees
    list_display = ("order", "name", "position", "boss", "is_working")


class EstimateAdmin(admin.ModelAdmin):
    model = EstimateProject
    list_display = ("name", "creation_date", "email", "nda_required", "idea_description")


class TestimonialAdmin(admin.ModelAdmin):
    model = Testimonial
    list_display = ("name", "position", "quote")


class PageSEOAdmin(admin.ModelAdmin):
    model = PageSeo


admin.site.register(Employees, EmployeesAdmin)
admin.site.register(Testimonial, TestimonialAdmin)
admin.site.register(EstimateProject, EstimateAdmin)
admin.site.register(PageSeo, PageSEOAdmin)
