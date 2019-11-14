from typing import Any
from typing import Optional

from django.core.handlers.wsgi import WSGIRequest
from django.db import models
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.core.query import PageQuerySet
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index

from company_website.models import Employees

# extend Blog tree
Page.steplen = 8


class MixinPageMethods:
    def get_children(self) -> PageQuerySet:
        return Page.objects.child_of(self).filter(live=True)

    @staticmethod
    def get_menu_categories() -> PageQuerySet:
        return Page.objects.filter(live=True, show_in_menus=True)


class BlogCategoryPage(Page, MixinPageMethods):
    template = "blog_categories_posts.haml"


class BlogIndexPage(Page, MixinPageMethods):
    template = "blog_index_page.haml"

    def get_last_article(self) -> "BlogIndexPage":
        return self.get_all_categories_articles().first()

    def get_all_categories_articles(self, _id: Optional[int] = None) -> PageQuerySet:
        menu_categories = self.get_menu_categories()
        gathered_articles = []
        for category in menu_categories:
            gathered_articles.append(Page.objects.child_of(category).filter(live=True).exclude(id=_id))
        if len(gathered_articles) > 0:
            all_articles = gathered_articles[0].union(*gathered_articles[1:])
        else:
            all_articles = Page.objects.child_of(self).filter(live=True, show_in_menus=False)
        return all_articles.order_by("-last_published_at")

    def get_rest_articles(self) -> PageQuerySet:
        return self.get_all_categories_articles(_id=getattr(self.get_last_article(), "id", None))

    @staticmethod
    def get_popular_articles() -> PageQuerySet:
        return BlogArticlePage.objects.all().order_by("-views")[:3]


class BlogArticlePage(Page, MixinPageMethods):
    template = "blog_post.haml"
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = StreamField([("paragraph", blocks.RichTextBlock()), ("table", TableBlock()), ("image", ImageChooserBlock())])

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

    def get_category(self) -> BlogCategoryPage:
        return self.get_parent()

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("intro"),
        StreamFieldPanel("body"),
        FieldPanel("author"),
        FieldPanel("read_time"),
        FieldPanel("views"),
        ImageChooserPanel("cover_photo"),
        ImageChooserPanel("article_photo"),
    ]

    def get_proper_url(self) -> str:
        category_url = self.url.split("/")[-2]
        article_url = self.url.split("/")[-1]
        return f"{category_url}/{article_url}"

    def get_context(self, request: WSGIRequest, *args: Any, **kwargs: Any) -> dict:
        context = super().get_context(request, *args, **kwargs)
        self._increase_view_counter(context["page"])
        return context

    @staticmethod
    def _increase_view_counter(page: "BlogArticlePage") -> None:
        # increase page view counter
        page.views += 1
        page.full_clean()
        page.save()
