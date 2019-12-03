from django.test import TestCase
from parameterized import parameterized

from blog.models import BlogCategorySnippet
from blog.models import BlogCategoryPage
from blog.tests.test_helpers import BlogTestHelpers


class TestBlogCategoryPage(TestCase, BlogTestHelpers):
    def setUp(self) -> None:
        (self.blog_index_page, self.site) = self._set_default_blog_index_page_as_new_root_page_child()
        self.blog_category_parameters = {
            "title": "Test Category",
            "seo_title": "Page SEO title",
            "slug": "test-category",
            "meta_description": "This is test category page",
            "keywords": "Category, Page, Blog",
        }

    def test_that_new_blog_category_snippet_should_create_blog_category_page(self):
        self._create_blog_category_snippet(**self.blog_category_parameters)
        self.assertTrue(BlogCategoryPage.objects.filter(**self.blog_category_parameters).exists())

    def test_that_delete_blog_category_snippet_should_delete_blog_category_page(self):
        blog_category_snippet = self._create_blog_category_snippet(**self.blog_category_parameters)
        self.assertTrue(BlogCategoryPage.objects.filter(**self.blog_category_parameters).exists())
        self.assertTrue(BlogCategorySnippet.objects.filter(**self.blog_category_parameters).exists())

        # delete blog_category_snippet
        blog_category_snippet.delete()
        self.assertFalse(BlogCategoryPage.objects.filter(**self.blog_category_parameters).exists())
        self.assertEqual(len(BlogCategoryPage.objects.all()), 0)
        self.assertEqual(len(BlogCategorySnippet.objects.all()), 0)

    def test_that_new_blog_category_page_should_create_blog_category_snippet(self):
        self.assertEqual(BlogCategorySnippet.objects.all().count(), 0)
        category_order = 0

        self._create_blog_category_page(self.blog_index_page, **self.blog_category_parameters)

        # assert that BlogCategoryPage objects exists
        self.assertTrue(BlogCategoryPage.objects.get(**self.blog_category_parameters))

        # if this query finds BlogCategorySnippet it will means that it's equally to BlogCategoryPage parameters
        blog_category_snippet = BlogCategorySnippet.objects.get(**self.blog_category_parameters)
        self.assertEqual(blog_category_snippet.order, category_order)

    def test_that_delete_blog_category_page_should_delete_blog_category_snippet(self):
        blog_category_page = self._create_blog_category_page(self.blog_index_page, **self.blog_category_parameters)

        self.assertTrue(BlogCategorySnippet.objects.get(**self.blog_category_parameters))

        # delete blog_category_page
        blog_category_page.delete()
        self.assertFalse(BlogCategorySnippet.objects.filter(**self.blog_category_parameters).exists())
        self.assertEqual(len(BlogCategoryPage.objects.all()), 0)
        self.assertEqual(len(BlogCategorySnippet.objects.all()), 0)

    @parameterized.expand(
        [
            ("title", "New Title"),
            ("seo_title", "New Seo Title"),
            # ("slug", "new-slug-name"),  # FIXME Now Categories are queried by slug
            ("meta_description", "New Meta Description"),
            ("keywords", "New keywords, Not Old"),
        ]
    )
    def test_that_change_any_blog_category_snippet_parameter_should_change_blog_category_page_parameter(
        self, parameter_name, parameter_value
    ):
        blog_category_snippet = self._create_blog_category_snippet(**self.blog_category_parameters)
        blog_category_page = BlogCategoryPage.objects.get(**self.blog_category_parameters)
        setattr(blog_category_snippet, parameter_name, parameter_value)
        blog_category_snippet.save()

        # Get BlogCategoryPage with the same PK
        changed_blog_category_page = BlogCategoryPage.objects.get(pk=blog_category_page.pk)
        self.assertEqual(getattr(blog_category_snippet, parameter_name), parameter_value)
        self.assertEqual(
            getattr(blog_category_snippet, parameter_name), getattr(changed_blog_category_page, parameter_name)
        )

    @parameterized.expand(
        [
            ("title", "New Title"),
            ("seo_title", "New Seo Title"),
            # ("slug", "new-slug-name"),  # FIXME Now Categories are queried by slug
            ("meta_description", "New Meta Description"),
            ("keywords", "New keywords, Not Old"),
        ]
    )
    def test_that_change_any_blog_category_page_parameter_should_change_blog_category_snippet_parameter(
        self, parameter_name, parameter_value
    ):
        blog_category_page = self._create_blog_category_page(self.blog_index_page, **self.blog_category_parameters)
        changed_blog_category = BlogCategorySnippet.objects.get(**self.blog_category_parameters)
        setattr(blog_category_page, parameter_name, parameter_value)
        blog_category_page.save()

        # Get BlogCategory with the same PK
        changed_blog_category = BlogCategorySnippet.objects.get(pk=changed_blog_category.pk)
        self.assertEqual(getattr(blog_category_page, parameter_name), parameter_value)
        self.assertEqual(getattr(blog_category_page, parameter_name), getattr(changed_blog_category, parameter_name))

    def test_that_blog_category_page_can_be_only_index_blog_page_child(self):
        pass

    def test_that_new_category_page_should_has_all_mandatory_parameters(self):
        pass
