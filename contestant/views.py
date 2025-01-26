from rest_framework import generics
from contestant import serializers
from rest_framework.permissions import IsAdminUser
from contestant import models
from rest_framework.filters import SearchFilter


class EscapeRoomQuestionListCreateAPIView(generics.ListCreateAPIView):
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
        'creator',
        'created_at',
    ]
