from rest_framework import serializers
from contestant import serializers as contestant_serializers
from . import models
from core.models import CustomUser
from . import exceptions


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Notification
        fields = "__all__"


class CustomStaffUserSerializer(serializers.ModelSerializer):
    team = contestant_serializers.TeamSerializer(read_only=True, required=False)

    class Meta:
        model = CustomUser
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        user = CustomUser.objects.get(id=data['id'])

        try:
            data["team"] = contestant_serializers.TeamSerializer(user.team).data
        except:
            data["team"] = None

        return data



class ClarificationSerializer(serializers.ModelSerializer):
    questioner = contestant_serializers.TeamSerializer(read_only=True)
    responder = CustomStaffUserSerializer(read_only=True)

    class Meta:
        model = models.Clarification
        fields = ['id', 'contest_question', 'contest_question_type', 'question', 'answer', 'questioner', 'responder']

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
