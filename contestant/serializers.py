from rest_framework import serializers
from . import models


class EscapeRoomQuestionCreateSerializer(serializers.ModelSerializer):
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
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']