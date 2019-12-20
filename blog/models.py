from typing import Any

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator
from django.db import models
from django.db.models import QuerySet
from modelcluster.fields import ParentalManyToManyField
from modelcluster.queryset import FakeQuerySet
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

    meta_description = models.CharField(max_length=168, blank=True)
    keywords = models.CharField(max_length=512, blank=True)

    promote_panels = Page.promote_panels + [FieldPanel("meta_description"), FieldPanel("keywords")]


class MixinPageMethods:
    @staticmethod
    def get_menu_categories() -> PageQuerySet:
        return BlogCategorySnippet.objects.all().order_by("order")

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


class BlogCategoryPage(MixinSeoFields, Page, MixinPageMethods):
    template = "blog_categories_posts.haml"

    def get_context(self, request: WSGIRequest, *args: Any, **kwargs: Any) -> dict:
        context = super().get_context(request, *args, **kwargs)
        context["category_articles"] = self.get_paginated_articles(
            BlogArticlePage.objects.filter(categories__slug=self.slug).order_by("-path"), request
        )
        return context

    def get_proper_url(self) -> str:
        return self.slug

    def get_absolute_url(self) -> str:
        return self.url_path

    def save(self) -> None:
        if self.pk is not None:
            blog_category_page = BlogCategoryPage.objects.get(pk=self.pk)
            blog_category = BlogCategorySnippet.objects.get(slug=blog_category_page.slug)
            if not blog_category.instance_parameters == self.instance_parameters:
                for (parameter_name, parameter_value) in self.instance_parameters.items():
                    setattr(blog_category, parameter_name, parameter_value)
            self._validate_parent_page()
            super().save()
            blog_category.save()
        else:
            order = getattr(BlogCategorySnippet.objects.all().order_by("order").last(), "order", 0)
            blog_category = BlogCategorySnippet(**self.instance_parameters, order=order)
            self._validate_parent_page()
            super().save()
            blog_category.save()

    def _validate_parent_page(self) -> None:
        if not isinstance(self.get_parent().specific, BlogIndexPage):
            raise ValidationError(message=f"{self.title} must be child of BlogIndexPage")

    def delete(self, *args: Any, **kwargs: Any) -> None:
        super().delete(*args, **kwargs)
        if BlogCategorySnippet.objects.filter(**self.instance_parameters):
            BlogCategorySnippet.objects.get(**self.instance_parameters).delete()

    @property
    def instance_parameters(self) -> dict:
        # Parameters for BlogCategoryPage and BlogCategorySnippet
        return {
            "title": self.title,
            "seo_title": self.seo_title,
            "slug": self.slug,
            "meta_description": self.meta_description,
            "keywords": self.keywords,
        }


@register_snippet
class BlogCategorySnippet(models.Model):
    title = models.CharField(
        max_length=255,
        help_text="Category title. This name will be shown as a category on blog main page.",
        unique=True,
    )
    seo_title = models.CharField(
        verbose_name="page seo title",
        max_length=255,
        blank=True,
        help_text="'Search Engine Friendly' title. This will appear at the top of the browser window.",
    )
    slug = models.SlugField(
        unique=True,
        max_length=80,
        help_text="Category page url address. Under this url category page will be searched.",
    )
    order = models.PositiveSmallIntegerField(help_text="Order of categories shown on blog main page menu.")
    meta_description = models.CharField(max_length=168, blank=True, help_text="Meta description of category page.")
    keywords = models.CharField(max_length=512, blank=True, help_text="Keywords of category page.")

    panels = [
        FieldPanel("title"),
        FieldPanel("seo_title"),
        FieldPanel("slug"),
        FieldPanel("meta_description"),
        FieldPanel("keywords"),
        FieldPanel("order"),
    ]

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def save(
        self, force_insert: Any = False, force_update: Any = False, using: Any = None, update_fields: Any = None
    ) -> None:
        # Updating BlogCategoryPage
        if self.pk is not None:
            category = BlogCategorySnippet.objects.get(pk=self.pk)
            blog_category_page = BlogCategoryPage.objects.get(slug=category.slug)
            if not blog_category_page.instance_parameters == self.instance_parameters:
                for (parameter_name, parameter_value) in self.instance_parameters.items():
                    setattr(blog_category_page, parameter_name, parameter_value)
                blog_category_page.save()
            self._validate_mandatory_fields()
            self.order = self._get_lowest_possible_order_number()
            super().save(force_insert, force_update, using, update_fields)
        else:
            # If BlogCategoryPage already exists skip this statement
            if not BlogCategoryPage.objects.filter(**self.instance_parameters).exists():
                self._validate_mandatory_fields()
                self.order = self._get_lowest_possible_order_number()
                super().save(force_insert, force_update, using, update_fields)
                parent_page = BlogIndexPage.objects.get(id=Site.objects.get(is_default_site=True).root_page_id)
                blog_category_page = BlogCategoryPage(**self.instance_parameters)
                parent_page.add_child(instance=blog_category_page)
                parent_page.save()
                blog_category_page.save()
        # Save BlogCategory object
        if not BlogCategorySnippet.objects.filter(**self.instance_parameters).exists():
            self._validate_mandatory_fields()
            self.order = self._get_lowest_possible_order_number()
            super().save(force_insert, force_update, using, update_fields)

    def _get_lowest_possible_order_number(self) -> int:
        order_number_exists = BlogCategorySnippet.objects.filter(order=self.order).exists()
        if not order_number_exists and isinstance(self.order, int):
            return self.order
        elif order_number_exists and isinstance(self.order, int):
            try:
                blog_category_snippet_with_bigger_order = BlogCategorySnippet.objects.get(order=(self.order))
                blog_category_snippet_with_bigger_order.order += 1
                blog_category_snippet_with_bigger_order.save()
                return self.order
            except BlogCategorySnippet.DoesNotExist:
                return self.order
        else:
            blog_category_snippets = BlogCategorySnippet.objects.all().order_by("order")
            if len(blog_category_snippets) == 0:
                return 0
            else:
                return blog_category_snippets.last().order + 1

    def _validate_mandatory_fields(self) -> None:
        mandatory_fields = ["title", "slug"]
        for field in mandatory_fields:
            if not getattr(self, field):
                raise ValidationError(message=f"{field} should not be None")

    def delete(self, using: Any = None, keep_parents: Any = False) -> None:
        super().delete(using, keep_parents)
        if BlogCategoryPage.objects.filter(**self.instance_parameters):
            BlogCategoryPage.objects.get(**self.instance_parameters).delete()

    @property
    def instance_parameters(self) -> dict:
        # Parameters for BlogCategoryPage and BlogCategorySnippet
        return {
            "title": self.title,
            "seo_title": self.seo_title,
            "slug": self.slug,
            "meta_description": self.meta_description,
            "keywords": self.keywords,
        }


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


class BlogArticlePage(MixinSeoFields, Page, MixinPageMethods):
    template = "blog_post.haml"
    categories = ParentalManyToManyField("blog.BlogCategorySnippet", related_name="category_posts")
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

    read_time = models.PositiveIntegerField()

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

    def save(self, *args: Any, **kwargs: Any) -> None:
        if not BlogArticlePage.objects.filter(is_main_article=True) and not self.is_main_article:
            self.is_main_article = True
        if self.is_main_article:
            try:
                article = BlogArticlePage.objects.get(is_main_article=self.is_main_article)
                article.is_main_article = False
                article.save()
            except BlogArticlePage.DoesNotExist:
                pass
        if isinstance(self.categories.all(), FakeQuerySet):
            if self.categories.all().results == []:
                raise ValidationError(message=f"Categories must set to an instance of BlogCategorySnippet")
        else:
            if self.categories.all() == []:
                raise ValidationError(message=f"Categories must set to an instance of BlogCategorySnippet")
        self._validate_parent_page()
        super().save(*args, **kwargs)

    def _validate_parent_page(self) -> None:
        if not isinstance(self.get_parent().specific, BlogIndexPage):
            raise ValidationError(message=f"{self.title} must be child of BlogIndexPage")
