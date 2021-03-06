from rest_framework import serializers

from .models import CustomUser, Subscription


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'image_profile',
            'description',
            'id',
            'username',
            )


class MyUserSerializer(serializers.ModelSerializer):
    infos_user = serializers.SerializerMethodField()

    def get_infos_user(self, obj):
        return obj.infos_user

    class Meta:
        model = CustomUser
        fields = (
            'image_profile',
            'description',
            'id',
            'username',
            'infos_user',
        )


class FollowersSerializer(serializers.ModelSerializer):
    infos_user = serializers.SerializerMethodField()

    def get_infos_user(self, obj):
        return obj.infos_user

    class Meta:
        model = Subscription
        fields = '__all__'
