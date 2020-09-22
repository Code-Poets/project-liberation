from typing import Any
from typing import List

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator
from django.db import models
from django.db.models import QuerySet
from django.db.models.signals import post_delete
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.functional import cached_property
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.core.blocks import CharBlock
from wagtail.core.blocks import PageChooserBlock
from wagtail.core.blocks import RichTextBlock
from wagtail.core.blocks import StreamBlock
from wagtail.core.blocks import StreamValue
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.core.query import PageQuerySet
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtailmarkdown.blocks import MarkdownBlock

from blog.constants import MAX_BLOG_ARTICLE_TITLE_LENGTH
from blog.constants import RICH_TEXT_BLOCK_FEATURES
from company_website.models import Employees
from company_website.view_helpers import GoogleAdsMixin


class MixinSeoFields(models.Model):
    class Meta:
        abstract = True

    meta_description = models.CharField(max_length=168, blank=True)
    keywords = models.CharField(max_length=512, blank=True)

    promote_panels = Page.promote_panels + [FieldPanel("meta_description"), FieldPanel("keywords")]


class MixinPageMethods:
    @staticmethod
    def get_paginated_articles(articles: QuerySet, request: WSGIRequest) -> Page:
        paginator = Paginator(articles, 6)
        page = request.GET.get("page")
        try:
            paginated_articles = paginator.page(page)
        except PageNotAnInteger:
            paginated_articles = paginator.page(1)
        except EmptyPage:
            paginated_articles = paginator.page(paginator.num_pages)
        return paginated_articles


class BlogIndexPage(MixinSeoFields, Page, MixinPageMethods, GoogleAdsMixin):
    template = "blog_index_page.haml"

    def get_all_articles(self) -> PageQuerySet:  # pylint: disable=no-self-use
        return BlogArticlePage.objects.filter(live=True).order_by("-path")

    def get_main_article(self) -> "BlogArticlePage":
        return self.get_all_articles().get(is_main_article=True)

    def get_rest_articles(self) -> PageQuerySet:
        return self.get_all_articles().filter(is_main_article=False)

    @staticmethod
    def get_popular_articles() -> PageQuerySet:
        return BlogArticlePage.objects.all().order_by("-views")[:5]

    def get_proper_url(self) -> str:
        return self.slug

    def get_absolute_url(self) -> str:
        return self.url_path

    def get_context(self, request: WSGIRequest, *args: Any, **kwargs: Any) -> dict:
        context_data = super().get_context(request, *args, **kwargs)
        context_data["paginated_rest_articles"] = self.get_paginated_articles(self.get_rest_articles(), request)
        context_data["paginated_all_articles"] = self.get_paginated_articles(self.get_all_articles(), request)
        return context_data


class BlogArticlePage(MixinSeoFields, Page, MixinPageMethods, GoogleAdsMixin):
    template = "blog_post.haml"
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = StreamField(
        [
            ("markdown", MarkdownBlock(icon="code")),
            ("header", CharBlock()),
            ("paragraph", RichTextBlock(features=RICH_TEXT_BLOCK_FEATURES)),
            ("table", TableBlock()),
            ("image", ImageChooserBlock()),
        ],
    )

    search_fields = Page.search_fields + [index.SearchField("intro"), index.SearchField("body")]

    author = models.ForeignKey(Employees, on_delete=models.DO_NOTHING)

    read_time = models.PositiveIntegerField()

    table_of_contents = models.BooleanField(default=False)

    recommended_articles = StreamField(
        [("page", PageChooserBlock(can_choose_root=False, page_type="blog.BlogArticlePage"))], null=True, blank=True,
    )

    views = models.PositiveIntegerField(default=0)

    cover_photo = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )

    article_photo = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )

    is_main_article = models.BooleanField(default=False)

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("intro"),
        FieldPanel("author"),
        FieldPanel("read_time"),
        StreamFieldPanel("recommended_articles"),
        FieldPanel("views"),
        FieldPanel("is_main_article"),
        ImageChooserPanel("cover_photo"),
        ImageChooserPanel("article_photo"),
        FieldPanel("table_of_contents"),
        StreamFieldPanel("body"),
    ]

    @cached_property
    def headers_list(self) -> List[str]:
        list_of_headers = []
        for stream_child in self.body:  # pylint: disable=not-an-iterable
            if stream_child.block.name == "header":
                list_of_headers.append(stream_child.value)
        return list_of_headers

    def get_header_id(self, title: str) -> int:
        return self.headers_list.index(title)

    def get_proper_url(self) -> str:
        return self.slug

    def get_absolute_url(self) -> str:
        return self.url_path

    def get_context(self, request: WSGIRequest, *args: Any, **kwargs: Any) -> dict:
        context = super().get_context(request, *args, **kwargs)
        self._increase_view_counter()
        context["URL_PREFIX"] = settings.URL_PREFIX
        return context

    def _increase_view_counter(self) -> None:
        # increase page view counter
        self.views += 1
        self.full_clean()
        self.save()

    def save(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=signature-differs
        if not BlogArticlePage.objects.filter(is_main_article=True) and not self.is_main_article:
            self.is_main_article = True
        if self.is_main_article:
            try:
                article = BlogArticlePage.objects.get(is_main_article=self.is_main_article)
                article.is_main_article = False
                article.save()
            except BlogArticlePage.DoesNotExist:
                pass

        if self.table_of_contents and len(self.headers_list) == 0:
            self.table_of_contents = False

        self._validate_parent_page()
        super().save(*args, **kwargs)

    def clean(self) -> None:
        super().clean()
        self._clean_recommended_articles()
        self._validate_title_length()
        self._validate_recommended_articles_uniqueness()

    def _clean_recommended_articles(self) -> None:
        self.recommended_articles = StreamValue(
            stream_block=StreamBlock([("page", PageChooserBlock())]),
            stream_data=[
                ("page", stream_child.value)
                for stream_child in self.recommended_articles
                if stream_child.value is not None
            ],
        )

    def _validate_parent_page(self) -> None:
        if not isinstance(self.get_parent().specific, BlogIndexPage):
            raise ValidationError(message=f"{self.title} must be child of BlogIndexPage")

    def _validate_title_length(self) -> None:
        if self.title is not None and len(self.title) > MAX_BLOG_ARTICLE_TITLE_LENGTH:
            raise ValidationError({"title": f"Title must be less than {MAX_BLOG_ARTICLE_TITLE_LENGTH} characters."})

    def _validate_recommended_articles_uniqueness(self) -> None:
        article_pages_set = set()
        for stream_child in self.recommended_articles:  # pylint: disable=not-an-iterable
            if stream_child.value in article_pages_set:
                raise ValidationError(message=f"'{stream_child.value}' is listed more than once!")
            article_pages_set.add(stream_child.value)


@receiver(post_save, sender=BlogArticlePage)
def ensure_main_article_exists(sender: BlogArticlePage, instance: BlogArticlePage, **_kwargs: Any) -> None:
    if (
        not instance.is_main_article
        and not sender.objects.exclude(id=instance.id).filter(is_main_article=True).exists()
    ):
        instance.is_main_article = True
        instance.save()
    if instance.is_main_article:
        try:
            article = sender.objects.exclude(id=instance.id).get(is_main_article=True)
            article.is_main_article = False
            article.save()
        except sender.DoesNotExist:
            pass


@receiver(post_delete, sender=BlogArticlePage)
def mark_latest_article_as_main(sender: BlogArticlePage, **_kwargs: Any) -> None:
    if not sender.objects.filter(is_main_article=True).exists():
        article = sender.objects.order_by("-date").first()
        if article is not None:
            article.is_main_article = True
            article.save()
