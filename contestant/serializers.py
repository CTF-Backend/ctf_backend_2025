from rest_framework import serializers
from core import serializers as core_serializers

from . import models
from . import exceptions


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Team
        exclude = ('account',)


class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TeamMember
        fields = '__all__'

    def create(self, validated_data):
        team = validated_data.get("team")
        if models.TeamMember.objects.filter(team=team).count() >= 3:
            raise exceptions.MaxTeamMember()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        team = validated_data.get("team")
        if team.status not in ['signed_up', 'solved_riddle']:
            raise exceptions.EditTeamMemberIsNotAllowed()
        return super().update(instance, validated_data)


class EscapeRoomQuestionListCreateSerializer(serializers.ModelSerializer):
    creator = core_serializers.CustomUserSerializer(read_only=True)

    class Meta:
        model = models.EscapeRoomQuestion
        fields = [
            'id',
            'name',
            'description',
            'floor',
            'x_coordinate',
            'y_coordinate',
            'score',
            'answer_limitation',
            'flag',
            'coin',
            'creator',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return models.EscapeRoomQuestion.objects.create(**validated_data)


class EscapeRoomQuestionForContestantsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EscapeRoomQuestion
        fields = [
            'id',
            'name',
            'description',
            'score',
            'flag',
            'coin',
        ]


class CTFQuestionSerializer(serializers.ModelSerializer):
    creator = core_serializers.CustomUserSerializer(read_only=True)

    class Meta:
        model = models.CTFQuestion
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user:
            validated_data['creator'] = request.user
        return super().create(validated_data)
