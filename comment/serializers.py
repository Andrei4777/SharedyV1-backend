from rest_framework import serializers

from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    infos_comment = serializers.SerializerMethodField()

    def get_infos_comment(self, obj):
        return obj.infos_comment

    class Meta:
        model = Comment
        fields = '__all__'
