from django.core.exceptions import ValidationError
from django.test import TestCase
from parameterized import parameterized

from blog.models import BlogCategoryPage
from blog.models import BlogCategorySnippet
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
        blog_category_page = self._create_blog_category_page(self.blog_index_page, **self.blog_category_parameters)
        new_blog_category_parameters = {
            "title": "Another Test Category",
            "seo_title": "Another Page SEO title",
            "slug": "another-test-category",
            "meta_description": "Another This is test category page",
            "keywords": "Another Category, Page, Blog",
        }

        # Add new BlogCateoryPage as a child of BlogCategoryPage
        new_blog_category_page = BlogCategoryPage(**new_blog_category_parameters)
        with self.assertRaises(ValidationError):
            blog_category_page.add_child(instance=new_blog_category_page)

    @parameterized.expand([("title"), ("slug")])
    def test_that_new_category_models_should_has_all_mandatory_parameters(self, parameter_name):
        self.blog_category_parameters[parameter_name] = None
        with self.assertRaises(ValidationError):
            self._create_blog_category_snippet(**self.blog_category_parameters)

        with self.assertRaises(ValidationError):
            self._create_blog_category_page(self.blog_index_page, **self.blog_category_parameters)

    @parameterized.expand([("seo_title"), ("meta_description"), ("keywords")])
    def test_that_unnecesarry_category_snippet_parameters_should_not_raise_exception(self, parameter_name):
        self.blog_category_parameters[parameter_name] = ""
        category_snippet = self._create_blog_category_snippet(**self.blog_category_parameters)
        self.assertIsInstance(category_snippet, BlogCategorySnippet)

    @parameterized.expand([("seo_title"), ("meta_description"), ("keywords")])
    def test_that_unnecesarry_category_page_parameters_should_not_raise_exception(self, parameter_name):
        self.blog_category_parameters[parameter_name] = ""
        category_page = self._create_blog_category_page(self.blog_index_page, **self.blog_category_parameters)
        self.assertIsInstance(category_page, BlogCategoryPage)

    def test_that_order_field_should_correctly_set_if_order_parameter_is_wrong(self):
        category_snippet_1 = self._create_blog_category_snippet(**self.blog_category_parameters)
        blog_category_parameters_2 = {name: value + "1" for (name, value) in self.blog_category_parameters.items()}
        category_snippet_2 = self._create_blog_category_snippet(**blog_category_parameters_2)
        blog_category_parameters_3 = {name: value + "2" for (name, value) in self.blog_category_parameters.items()}
        category_snippet_3 = self._create_blog_category_snippet(**blog_category_parameters_3)
        blog_category_parameters_4 = {name: value + "3" for (name, value) in self.blog_category_parameters.items()}
        category_snippet_4 = self._create_blog_category_snippet(**blog_category_parameters_4)
        self.assertEqual(category_snippet_1.order, 0)
        self.assertEqual(category_snippet_2.order, 1)
        self.assertEqual(category_snippet_3.order, 2)
        self.assertEqual(category_snippet_4.order, 3)

        # Change order "by hand" to different one
        category_snippet_4.order = 0
        category_snippet_4.save()

        self.assertEqual(BlogCategorySnippet.objects.get(slug=category_snippet_4.slug).order, 0)
        self.assertEqual(BlogCategorySnippet.objects.get(slug=category_snippet_1.slug).order, 1)
        self.assertEqual(BlogCategorySnippet.objects.get(slug=category_snippet_2.slug).order, 2)
        self.assertEqual(BlogCategorySnippet.objects.get(slug=category_snippet_3.slug).order, 3)