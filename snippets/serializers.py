# -*- coding: utf-8 -*-
from rest_framework import serializers

from .models import Snippet, Category


class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    categories = serializers.StringRelatedField(many=True)

    class Meta:
        model = Snippet
        fields = ('rank', 'categories', 'title', 'code',
                  'description', 'created', 'updated')


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('rank', 'slug', 'name', 'description')
