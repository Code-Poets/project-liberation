from django.contrib import admin
from sorl.thumbnail.admin import AdminImageMixin

from company_website.models import Employees
from company_website.models import EstimateProject
from company_website.models import EstimateProjectEmailRecipients
from company_website.models import PageSeo
from company_website.models import Testimonial


class EmployeesAdmin(AdminImageMixin, admin.ModelAdmin):
    model = Employees
    list_display = ("order", "full_name", "position", "boss", "is_working")


class EstimateAdmin(admin.ModelAdmin):
    model = EstimateProject
    list_display = ("name", "creation_date", "email", "idea_description")


class TestimonialAdmin(admin.ModelAdmin):
    model = Testimonial
    list_display = ("name", "position", "quote")


class PageSEOAdmin(admin.ModelAdmin):
    model = PageSeo


class EstimateProjectEmailRecipientsAdmin(admin.ModelAdmin):
    model = EstimateProjectEmailRecipients


admin.site.register(Employees, EmployeesAdmin)
admin.site.register(Testimonial, TestimonialAdmin)
admin.site.register(EstimateProject, EstimateAdmin)
admin.site.register(PageSeo, PageSEOAdmin)
admin.site.register(EstimateProjectEmailRecipients, EstimateProjectEmailRecipientsAdmin)
