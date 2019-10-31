from wagtail.contrib.modeladmin.options import ModelAdmin
from wagtail.contrib.modeladmin.options import ModelAdminGroup
from wagtail.contrib.modeladmin.options import modeladmin_register

from blog.models import BlogArticlePage
from blog.models import BlogCategoryPage


class BlogPageModelAdmin(ModelAdmin):
    model = BlogArticlePage


class BlogPageModelAdminGroup(ModelAdminGroup):
    menu_label = "Blog Pages"
    menu_order = 400
    items = (BlogPageModelAdmin,)


class BlogCategoryPageModelAdmin(ModelAdmin):
    model = BlogCategoryPage


class BlogCategoryPageModelAdminGroup(ModelAdminGroup):
    menu_label = "Blog Menu"
    menu_order = 500
    items = (BlogCategoryPageModelAdmin,)


modeladmin_register(BlogPageModelAdminGroup)
modeladmin_register(BlogCategoryPageModelAdminGroup)
