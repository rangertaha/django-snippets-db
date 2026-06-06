from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from .forms import SnippetForm
from .models import Category, Snippet
from .serializers import CategorySerializer, SnippetSerializer


class CategoryModelTests(TestCase):
    def test_str_returns_name(self):
        category = Category.objects.create(name="Linux")
        self.assertEqual(str(category), "Linux")

    def test_slug_is_autofilled_from_name_on_save(self):
        category = Category.objects.create(name="Version Control")
        self.assertEqual(category.slug, "version-control")

    def test_explicit_slug_is_preserved(self):
        category = Category.objects.create(name="Linux", slug="custom-slug")
        self.assertEqual(category.slug, "custom-slug")

    def test_default_count_is_zero(self):
        self.assertEqual(Category.objects.create(name="Empty").count, 0)

    def test_ordering_is_by_rank(self):
        low = Category.objects.create(name="Low", rank=1)
        high = Category.objects.create(name="High", rank=5)
        self.assertEqual(list(Category.objects.all()), [low, high])

    def test_verbose_name_plural(self):
        self.assertEqual(str(Category._meta.verbose_name_plural), "Categories")


class SnippetModelTests(TestCase):
    def test_str_returns_title(self):
        snippet = Snippet.objects.create(title="List files", code="ls -la")
        self.assertEqual(str(snippet), "List files")

    def test_slug_is_autofilled_from_title_on_save(self):
        snippet = Snippet.objects.create(title="List All Files", code="ls -la")
        self.assertEqual(snippet.slug, "list-all-files")

    def test_explicit_slug_is_preserved(self):
        snippet = Snippet.objects.create(
            title="List files", slug="ls", code="ls -la"
        )
        self.assertEqual(snippet.slug, "ls")

    def test_ordering_is_by_rank(self):
        first = Snippet.objects.create(title="First", code="a", rank=1)
        second = Snippet.objects.create(title="Second", code="b", rank=2)
        self.assertEqual(list(Snippet.objects.all()), [first, second])

    def test_categories_relation(self):
        category = Category.objects.create(name="Shell")
        snippet = Snippet.objects.create(title="List files", code="ls -la")
        snippet.categories.add(category)
        self.assertIn(snippet, category.snippets.all())
        self.assertIn(category, snippet.categories.all())

    def test_self_relation_is_not_symmetrical(self):
        parent = Snippet.objects.create(title="Parent", code="p")
        child = Snippet.objects.create(title="Child", code="c")
        child.snippets.add(parent)
        # related_name='parent' is the reverse side and only exists because the
        # relation is non-symmetrical.
        self.assertIn(parent, child.snippets.all())
        self.assertIn(child, parent.parent.all())
        self.assertNotIn(child, parent.snippets.all())


class SnippetFormTests(TestCase):
    def test_valid_form(self):
        form = SnippetForm(
            data={"title": "List files", "code": "ls -la", "description": ""}
        )
        self.assertTrue(form.is_valid())

    def test_exposes_expected_fields(self):
        form = SnippetForm()
        self.assertEqual(
            list(form.fields), ["title", "code", "description", "categories"]
        )


class SerializerTests(TestCase):
    def test_snippet_serializer_fields_and_categories(self):
        category = Category.objects.create(name="Shell")
        snippet = Snippet.objects.create(
            title="List files", code="ls -la", rank=3, description="lists files"
        )
        snippet.categories.add(category)

        data = SnippetSerializer(snippet).data

        self.assertEqual(
            set(data),
            {"rank", "categories", "title", "code", "description", "created", "updated"},
        )
        # categories is a StringRelatedField -> str(Category) == name
        self.assertEqual(data["categories"], ["Shell"])
        self.assertEqual(data["title"], "List files")

    def test_category_serializer_fields(self):
        category = Category.objects.create(name="Shell", rank=2)
        data = CategorySerializer(category).data
        self.assertEqual(set(data), {"rank", "slug", "name", "description"})
        self.assertEqual(data["name"], "Shell")
        self.assertEqual(data["slug"], "shell")


class SnippetAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_list_snippets(self):
        Snippet.objects.create(title="List files", code="ls -la")
        response = self.client.get("/api/snippets/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_snippet(self):
        response = self.client.post(
            "/api/snippets/",
            {"title": "Print working dir", "code": "pwd"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Snippet.objects.count(), 1)
        self.assertEqual(Snippet.objects.get().title, "Print working dir")

    def test_snippets_ordered_by_rank_descending(self):
        Snippet.objects.create(title="Low", code="a", rank=1)
        Snippet.objects.create(title="High", code="b", rank=9)
        response = self.client.get("/api/snippets/")
        ranks = [row["rank"] for row in response.data]
        self.assertEqual(ranks, [9, 1])

    def test_list_categories(self):
        Category.objects.create(name="Shell")
        response = self.client.get("/api/categories/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class SnippetViewTests(TestCase):
    def test_list_view_renders(self):
        Snippet.objects.create(title="List files", code="ls -la")
        response = self.client.get(reverse("snippet-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, "snippets/snippet_list.html")
        self.assertIn("categories", response.context)
        self.assertIsInstance(response.context["form"], SnippetForm)

    def test_list_view_search_filters_by_active_and_title(self):
        match = Snippet.objects.create(
            title="List files", code="ls -la", active=True
        )
        Snippet.objects.create(
            title="List files quietly", code="ls", active=False
        )
        Snippet.objects.create(title="Print dir", code="pwd", active=True)

        response = self.client.get(reverse("snippet-list"), {"q": "list"})

        results = list(response.context["object_list"])
        self.assertEqual(results, [match])

    def test_list_view_without_query_returns_all(self):
        Snippet.objects.create(title="One", code="a")
        Snippet.objects.create(title="Two", code="b")
        response = self.client.get(reverse("snippet-list"))
        self.assertEqual(len(response.context["object_list"]), 2)

    def test_detail_view_renders(self):
        snippet = Snippet.objects.create(title="List files", code="ls -la")
        response = self.client.get(
            reverse("snippet-detail", args=[snippet.slug])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, "snippets/snippet_detail.html")
        self.assertEqual(response.context["object"], snippet)
