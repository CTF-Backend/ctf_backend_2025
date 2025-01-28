from rest_framework import serializers
from core import serializers as core_serializers

from . import models


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Team
        exclude = ('account',)


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
