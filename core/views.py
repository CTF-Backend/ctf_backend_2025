from rest_framework import generics
from core import serializers
from rest_framework.permissions import IsAdminUser
from core import models
from rest_framework.filters import SearchFilter


class EscapeRoomQuestionCreateAPIView(generics.ListCreateAPIView):
    queryset = models.EscapeRoomQuestion.objects.all()
    serializer_class = serializers.EscapeRoomQuestionCreateSerializer
    permission_classes = [IsAdminUser]

    filter_backends = [SearchFilter]
    search_fields = [
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

