# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from rest_framework import routers

from .views import SnippetViewDetail, SnippetViewList, SnippetAPIViewSet, CategoryAPIViewSet

router = routers.DefaultRouter()
router.register(r'snippets', SnippetAPIViewSet)
router.register(r'categories', CategoryAPIViewSet)


urlpatterns = [
    url(r'^api/', include(router.urls)),

    url(r'^$', SnippetViewList.as_view(), name='snippet-list'),
    url(r'^(?P<path>.*)$', SnippetViewDetail.as_view(), name='snippet-detail'),




]



