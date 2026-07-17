# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Entries for 2016 were reconstructed from git history after the fact; the
project has not yet been published to PyPI.

## [Unreleased]

### Added

- `pyproject.toml` packaging (hatchling, PEP 621 metadata) with the version
  read dynamically from `snippets/__init__.py`.
- Initial database migration (`0001_initial`) for the `Snippet` and
  `Category` models.
- Test suite (41 tests) covering models (including the current
  created/updated timestamp behavior), forms, serializers, the REST API,
  the list/detail views, and the admin.
- GitHub Actions CI workflow running the test suite, Ruff, and mypy on
  Python 3.12, 3.13, and 3.14.
- GitHub Actions publish workflow releasing to PyPI via Trusted Publishing
  (OIDC) when a GitHub release is published.
- Ruff (lint + format) and mypy configuration, plus a `dev` dependency
  group with coverage, Ruff, and mypy.
- This changelog and a full README (what/install/usage/configuration/
  development).

### Changed

- Target Python raised to >=3.12 (tested on 3.12–3.14).
- Django pinned to the 5.2 LTS series (`>=5.2,<5.3`); Django REST Framework
  raised to `>=3.17`.
- Package source moved to a `src/` layout (`src/snippets/`); the installed
  import path (`snippets`) is unchanged.
- Code modernized for Django 5.2: `django.conf.urls.url` replaced with
  `path()`/`re_path()`, `ugettext_lazy` with `gettext_lazy`,
  `__unicode__` with `__str__`, and modules reformatted/linted with Ruff.

### Removed

- Legacy `setup.py`, `MANIFEST.in`, and `requirements.txt` (superseded by
  `pyproject.toml`).

### Known issues

- `Snippet.created` uses `auto_now=True` and `Snippet.updated` uses
  `auto_now_add=True` — the conventional semantics are swapped. Fixing this
  changes behavior and requires a migration; it is deliberately left as-is
  for now and pinned by tests documenting the current behavior.

## [0.0.1] - 2016-05-30

Initial development version; never published to PyPI.

### Added

- `snippets` reusable Django app with `Snippet` and `Category` models:
  rank-based ordering, slug auto-generation via `pre_save` signals,
  category relations, and non-symmetrical snippet-to-snippet relations.
- Django admin registration for snippets and categories with list displays
  and search.
- Snippet list view with title search (`?q=`), pagination, and a
  slug-based detail view, styled with Bootstrap 3 templates.
- REST API built on Django REST Framework: router-based
  `/api/snippets/` and `/api/categories/` endpoints with serializers.
- Example Django project (`example/`) demonstrating installation, base
  templates, and navigation.
- MIT license.

### Removed

- Early `Subscriber` model and file-database leftovers (`fsdb` templates,
  file-type/extension choices) were dropped during initial development as
  the app was refocused on code snippets.

[Unreleased]: https://github.com/Rangertaha/django-snippets-db/compare/0d8b46c...HEAD
[0.0.1]: https://github.com/Rangertaha/django-snippets-db/commits/f8178b6
