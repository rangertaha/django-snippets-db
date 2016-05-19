# -*- coding: utf-8 -*-
from django.views.generic import ListView, DetailView
from rest_framework import viewsets

from .models import Snippet, Category
from .serializers import SnippetSerializer, CategorySerializer


class SnippetViewDetail(DetailView):
    model = Snippet

    def get_context_data(self, **kwargs):
        context = super(SnippetViewDetail, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.filter().distinct()
        return context


class SnippetViewList(ListView):
    model = Snippet
    paginate_by = 5

    def get_queryset(self):
        if self.request.GET.get('q'):
            return self.model.objects.filter(
                active=True,
                title__icontains=self.request.GET['q']).distinct()
        else:
            return self.model.objects.all()

    def get_context_data(self, **kwargs):
        context = super(SnippetViewList, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.filter().distinct()
        return context


class CategoryViewDetail(DetailView):
    model = Category


class CategoryViewList(ListView):
    model = Category


class SnippetAPIViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Snippet.objects.all().order_by('-rank')
    serializer_class = SnippetSerializer


class CategoryAPIViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to b
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
