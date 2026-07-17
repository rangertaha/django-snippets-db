from django.urls import include, path, re_path
from rest_framework import routers

from .views import (
    CategoryAPIViewSet,
    SnippetAPIViewSet,
    SnippetViewDetail,
    SnippetViewList,
)

router = routers.DefaultRouter()
router.register(r"snippets", SnippetAPIViewSet)
router.register(r"categories", CategoryAPIViewSet)


urlpatterns = [
    path("api/", include(router.urls)),
    path("", SnippetViewList.as_view(), name="snippet-list"),
    re_path(r"^(?P<slug>.*)$", SnippetViewDetail.as_view(), name="snippet-detail"),
]
