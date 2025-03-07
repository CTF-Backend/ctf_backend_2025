from rest_framework import serializers
from contestant import serializers as contestant_serializers
from . import models
from core.models import CustomUser
from . import exceptions


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Notification
        fields = "__all__"


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"


class ClarificationSerializer(serializers.ModelSerializer):
    questioner = contestant_serializers.TeamSerializer(read_only=True)
    responder = CustomUserSerializer(read_only=True)

    class Meta:
        model = models.Clarification
        fields = ['id', 'question', 'answer', 'questioner', 'responder']

    def create(self, validated_data):
        request = self.context.get('request')
        if request.user.is_staff:
            raise exceptions.OnlyTeamIsAllowed()
        validated_data['questioner_id'] = request.user.team.id
        instance = super().create(validated_data)
        return instance

    def update(self, instance, validated_data):
        request = self.context.get('request')
        validated_data['responder_id'] = request.user.id
        return super().update(instance, validated_data)
