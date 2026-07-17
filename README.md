# django-snippets-db

[![CI](https://github.com/Rangertaha/django-snippets-db/actions/workflows/ci.yml/badge.svg)](https://github.com/Rangertaha/django-snippets-db/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.12%20%7C%203.13%20%7C%203.14-blue)](https://github.com/Rangertaha/django-snippets-db/blob/master/pyproject.toml)
[![Django](https://img.shields.io/badge/django-5.2%20LTS-0C4B33)](https://www.djangoproject.com/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](https://github.com/Rangertaha/django-snippets-db/blob/master/LICENSE)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

A reusable Django app for storing and serving reusable code snippets.

## What is it?

`django-snippets-db` adds a snippets database to any Django project. It
provides:

- **Models** — `Snippet` (title, code, usage, example, description, rank,
  slug, categories, related snippets) and `Category`, with slugs generated
  automatically from titles/names on save.
- **Views** — a paginated snippet list with title search (`?q=...`) and a
  slug-based detail view, rendered from overridable templates.
- **REST API** — `/api/snippets/` and `/api/categories/` endpoints built on
  Django REST Framework.
- **Admin** — both models registered with list displays and search.

It requires Python 3.12+, Django 5.2 LTS, and Django REST Framework 3.17+.

## Install

Not yet on PyPI; install from GitHub:

```bash
pip install "django-snippets-db @ git+https://github.com/Rangertaha/django-snippets-db.git"
```

## Usage

1. Add the app and its dependency to `INSTALLED_APPS` in `settings.py`:

   ```python
   INSTALLED_APPS = [
       # ...
       "snippets",
       "rest_framework",
   ]
   ```

2. Include the URLs in your project `urls.py`:

   ```python
   from django.urls import include, path

   urlpatterns = [
       # ...
       path("snippets/", include("snippets.urls")),
   ]
   ```

3. Create the tables:

   ```bash
   python manage.py migrate snippets
   ```

This exposes:

| URL | What |
| --- | --- |
| `snippets/` | Paginated snippet list; filter with `?q=<title>` |
| `snippets/<slug>` | Snippet detail |
| `snippets/api/snippets/` | REST API for snippets |
| `snippets/api/categories/` | REST API for categories |

## Configuration

- **Templates** — the bundled `snippets/snippet_list.html` and
  `snippets/snippet_detail.html` extend a project-level `base.html` and fill
  `navbar`, `breadcrumb`, `lsidebar`, and content blocks (see
  `example/templates/base.html` for a working Bootstrap 3 base). Override
  the templates in your project to restyle them.
- **REST Framework** — the API uses your project-wide `REST_FRAMEWORK`
  settings (permissions, pagination, etc.); nothing snippet-specific is
  required.

## Development

The repository ships an example project used as the test harness. With
[uv](https://docs.astral.sh/uv/) installed:

```bash
git clone https://github.com/Rangertaha/django-snippets-db.git
cd django-snippets-db
uv sync --extra example --dev

# Run the test suite
uv run example/manage.py test snippets

# Coverage
uv run coverage run example/manage.py test snippets
uv run coverage report

# Lint, format, type-check
uv run ruff check .
uv run ruff format --check .
uv run mypy

# Try the example site at http://127.0.0.1:8000/
uv run example/manage.py migrate
uv run example/manage.py runserver
```

The package source lives in `src/snippets/`; tests are in
`src/snippets/tests.py` and run through the example project's settings.

See [CHANGELOG.md](CHANGELOG.md) for release history. Licensed under the
[MIT license](LICENSE).
