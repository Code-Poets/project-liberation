from django.db import models
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index

from company_website.models import Employees


class BlogCategoryPage(Page):
    template = "blog_categories_posts.haml"

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)
        return context

    def get_children(self):
        return super().get_children().live()

    def get_menu_categories(self):
        return self.get_parent().get_children().filter(live=True, show_in_menus=True)


class BlogIndexPage(Page):
    template = "blog_index_page.haml"

    def get_context(self, request, *args, **kwargs):
        context = super(BlogIndexPage, self).get_context(request)
        return context

    def get_children(self):
        return super().get_children().live()

    def get_last_article(self):
        return self.get_all_categories_articles().last()

    def get_all_categories_articles(self, _id=None):
        menu_categories = self.get_menu_categories()
        gathered_articles = []
        for category in menu_categories:
            gathered_articles.append(Page.objects.child_of(category).filter(live=True).exclude(id=_id))
        if len(gathered_articles) > 0:
            all_articles = gathered_articles[0].union(*gathered_articles[1:])
        else:
            all_articles = Page.objects.child_of(self).filter(live=True, show_in_menus=False)
        return all_articles

    def get_rest_articles(self):
        return self.get_all_categories_articles(_id=getattr(self.get_last_article(), "id", None))

    def get_menu_categories(self):
        return self.get_children().filter(live=True, show_in_menus=True)

    def get_popular_articles(self):  # pylint: disable=no-self-use
        return BlogArticlePage.objects.all().order_by("-views")[:3]


class BlogArticlePage(Page):
    template = "blog_post.haml"
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)

    search_fields = Page.search_fields + [index.SearchField("intro"), index.SearchField("body")]

    author = models.ForeignKey(Employees, on_delete=models.DO_NOTHING)

    read_time = models.IntegerField()

    views = models.PositiveIntegerField(default=0)

    cover_photo = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )

    article_photo = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )

    def get_category(self):
        return self.get_parent()

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("intro"),
        FieldPanel("body", classname="full"),
        FieldPanel("author"),
        FieldPanel("read_time"),
        FieldPanel("views"),
        ImageChooserPanel("cover_photo"),
        ImageChooserPanel("article_photo"),
    ]

    def get_proper_url(self):
        category_url = self.url.split("/")[-2]
        article_url = self.url.split("/")[-1]
        return f"{category_url}/{article_url}"

    def get_menu_categories(self):
        return self.get_parent().get_parent().get_children().filter(live=True, show_in_menus=True)

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        # increase page view counter
        context["page"].views += 1
        context["page"].full_clean()
        context["page"].save()
        return context
