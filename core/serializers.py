from rest_framework import serializers
from core import models
from core.models import CustomUser
from exceptions import *


class TeamAuthSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, max_length=255)
    password2 = serializers.CharField(write_only=True, max_length=255)

    class Meta:
        model = models.CustomUser
        fields = ('username', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise PasswordISNotSameAsPassword2()
        return attrs

    def create(self, validated_data):
        validated_data['is_team'] = True
        team = CustomUser.objects.create_user(
            username=validated_data.get('username'),
            password=validated_data.get('password')
            ** validated_data
        )
        return team
