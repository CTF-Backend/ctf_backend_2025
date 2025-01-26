from rest_framework import serializers
from core import models
from core.models import CustomUser
from . import exceptions
from dj_rest_auth.serializers import LoginSerializer
from django.contrib.auth import authenticate


class TeamAuthSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, max_length=255)
    password2 = serializers.CharField(write_only=True, max_length=255)

    class Meta:
        model = models.CustomUser
        fields = ('id', 'username', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise exceptions.PasswordISNotSameAsPassword2()
        return attrs

    def create(self, validated_data):
        validated_data['is_team'] = True
        validated_data.pop('password2')
        team = CustomUser.objects.create_user(
            username=validated_data.pop('username', None),
            password=validated_data.pop('password', None),
            **validated_data
        )
        return team


class StaffAuthSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, max_length=255)
    password2 = serializers.CharField(write_only=True, max_length=255)

    class Meta:
        model = models.CustomUser
        fields = ('id', 'username', 'password', 'password2', 'first_name', 'last_name', 'email')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise exceptions.PasswordISNotSameAsPassword2()
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        team = CustomUser.objects.create_superuser(
            username=validated_data.pop('username', None),
            password=validated_data.pop('password', None),
            **validated_data
        )
        return team


class CustomLoginSerializer(LoginSerializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if not username or not password:
            raise exceptions.PasswordAndUsernameIsRequired()

        user = authenticate(username=username, password=password)
        if not user:
            raise exceptions.PasswordOrUsernameIsIncorrect()

        attrs['user'] = user
        return attrs
