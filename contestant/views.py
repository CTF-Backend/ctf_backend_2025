from rest_framework import generics, filters
from contestant import serializers
from rest_framework import permissions
from contestant import models


class TeamListAPIView(generics.ListAPIView):
    queryset = models.Team.objects.all()
    serializer_class = serializers.TeamSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        'name', 'score', 'coin', 'status'
    ]
    ordering_fields = [
        'name', 'score', 'coin', 'status'
    ]


class TeamDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Team.objects.all()
    serializer_class = serializers.TeamSerializer
    permission_classes = [permissions.IsAdminUser]


class EscapeRoomQuestionListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.EscapeRoomQuestion.objects.all()
    serializer_class = serializers.EscapeRoomQuestionListCreateSerializer
    permission_classes = [permissions.IsAdminUser]

    filter_backends = [filters.SearchFilter]
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


class EscapeRoomQuestionDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.EscapeRoomQuestion.objects.all()
    serializer_class = serializers.EscapeRoomQuestionListCreateSerializer
    permission_classes = [permissions.IsAdminUser]


class EscapeRoomQuestionForContestantsListAPIView(generics.ListAPIView):
    queryset = models.EscapeRoomQuestion.objects.all()
    serializer_class = serializers.EscapeRoomQuestionForContestantsListSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [filters.SearchFilter]
    search_fields = [
        'id',
        'name',
        'description',
        'score',
        'flag',
        'coin',
    ]
