from rest_framework import serializers

from .models import Category, Snippet


class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    categories = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Snippet
        fields = (
            "rank",
            "categories",
            "title",
            "code",
            "description",
            "created",
            "updated",
        )


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ("rank", "slug", "name", "description")
