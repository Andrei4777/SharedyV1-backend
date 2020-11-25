from rest_framework import serializers

from user.models import CustomUser


class RegistrerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
