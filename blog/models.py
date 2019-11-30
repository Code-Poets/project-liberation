from typing import Any

from django import forms
from django.core.handlers.wsgi import WSGIRequest
from django.db import models
from django.db.models import QuerySet
from modelcluster.fields import ParentalManyToManyField
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.core.models import Site
from wagtail.core.query import PageQuerySet
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtailmarkdown.blocks import MarkdownBlock

from company_website.models import Employees


class MixinSeoFields(models.Model):
    class Meta:
        abstract = True

    meta_description = models.CharField(max_length=168, default="")
    keywords = models.CharField(max_length=512, default="")

    promote_panels = Page.promote_panels + [FieldPanel("meta_description"), FieldPanel("keywords")]


class MixinPageMethods:
    @staticmethod
    def get_menu_categories() -> PageQuerySet:
        return BlogCategory.objects.all().order_by("order")


class BlogCategoryPage(MixinSeoFields, Page, MixinPageMethods):
    template = "blog_categories_posts.haml"

    def get_context(self, request: WSGIRequest, *args: Any, **kwargs: Any) -> dict:
        context = super().get_context(request, *args, **kwargs)
        context["category_articles"] = BlogArticlePage.objects.filter(categories__slug=self.slug).order_by("-path")
        return context

    def get_proper_url(self) -> str:
        return self.slug

    def get_absolute_url(self) -> str:
        return f"/blog/{self.get_proper_url()}/"


@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(
        max_length=255, help_text="Name of category. This name will be shown as a category on blog main page."
    )
    slug = models.SlugField(
        unique=True,
        max_length=80,
        help_text="Category page url address. Under this url category page will be searched.",
    )
    order = models.PositiveSmallIntegerField(help_text="Order of categories shown on blog main page menu.")
    meta_description = models.CharField(max_length=168, default="", help_text="Meta description of category page.")
    keywords = models.CharField(max_length=512, default="", help_text="Keywords of category page.")
    title = models.CharField(
        verbose_name="page title",
        max_length=255,
        default="",
        help_text="'Search Engine Friendly' title. This will appear at the top of the browser window.",
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
        FieldPanel("title"),
        FieldPanel("meta_description"),
        FieldPanel("keywords"),
        FieldPanel("order"),
    ]

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def save(
        self, force_insert: Any = False, force_update: Any = False, using: Any = None, update_fields: Any = None
    ) -> None:
        if self.pk is not None:
            category = BlogCategory.objects.get(pk=self.pk)
            blog_category_page = BlogCategoryPage.objects.get(slug=category.slug)
            super().save(force_insert, force_update, using, update_fields)
            blog_category_page.title = self.title
            blog_category_page.seo_title = self.title
            blog_category_page.slug = self.slug
            blog_category_page.meta_description = self.meta_description
            blog_category_page.keywords = self.keywords
            blog_category_page.save()
        else:
            super().save(force_insert, force_update, using, update_fields)
            parent_page = Site.objects.get(is_default_site=True).root_page
            blog_category_page = BlogCategoryPage(
                title=self.title,
                seo_title=self.title,
                slug=self.slug,
                meta_description=self.meta_description,
                keywords=self.keywords,
            )
            parent_page.add_child(instance=blog_category_page)
            blog_category_page.save()

    def delete(self, using: Any = None, keep_parents: Any = False) -> None:
        Page.objects.get(slug=self.slug).delete()
        super().delete(using, keep_parents)


class BlogIndexPage(MixinSeoFields, Page, MixinPageMethods):
    template = "blog_index_page.haml"

    def get_all_articles(self) -> PageQuerySet:  # pylint: disable=no-self-use
        return BlogArticlePage.objects.filter(live=True).order_by("-path")

    def get_main_article(self) -> "BlogArticlePage":
        return self.get_all_articles().get(is_main_article=True)

    def get_rest_articles(self) -> PageQuerySet:
        return self.get_all_articles().filter(is_main_article=False)

    @staticmethod
    def get_popular_articles() -> PageQuerySet:
        return BlogArticlePage.objects.all().order_by("-views")[:3]

    def get_proper_url(self) -> str:
        return self.slug

    def get_absolute_url(self) -> str:  # pylint: disable=no-self-use
        return "/blog/"


class BlogArticlePage(MixinSeoFields, Page, MixinPageMethods):
    template = "blog_post.haml"
    categories = ParentalManyToManyField("blog.BlogCategory", blank=True, related_name="category_posts")
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = StreamField(
        [
            ("markdown", MarkdownBlock(icon="code")),
            ("paragraph", blocks.RichTextBlock()),
            ("table", TableBlock()),
            ("image", ImageChooserBlock()),
        ]
    )

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

    is_main_article = models.BooleanField(default=False)

    def get_article_categories(self) -> QuerySet:
        return self.specific.categories.all()

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("intro"),
        FieldPanel("author"),
        FieldPanel("read_time"),
        FieldPanel("views"),
        FieldPanel("is_main_article"),
        ImageChooserPanel("cover_photo"),
        ImageChooserPanel("article_photo"),
        FieldPanel("categories", widget=forms.CheckboxSelectMultiple),
        StreamFieldPanel("body"),
    ]

    def get_proper_url(self) -> str:
        return self.slug

    def get_absolute_url(self) -> str:
        return f"/blog/{self.get_proper_url()}/"

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

    def save(self, *args: Any, **kwargs: Any) -> None:
        if self.is_main_article:
            try:
                article = BlogArticlePage.objects.get(is_main_article=self.is_main_article)
                article.is_main_article = False
                article.save()
            except BlogArticlePage.DoesNotExist:
                pass
        super().save(*args, **kwargs)
