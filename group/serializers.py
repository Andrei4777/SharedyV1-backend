from rest_framework import serializers

from .models import Group


class GroupFollowSerializer(serializers.ModelSerializer):
    infos_user = serializers.SerializerMethodField()

    def get_infos_user(self, obj):
        return obj.infos_user

    class Meta:
        model = Group
        fields = '__all__'
