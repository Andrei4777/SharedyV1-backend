from rest_framework import serializers

from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    infos_article = serializers.SerializerMethodField()

    def get_infos_article(self, obj):
        return obj.infos_article

    class Meta:
        model = Article
        exclude = ['creator', 'group_article']
        depth = 1
