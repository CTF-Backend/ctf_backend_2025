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


class TeamMemberListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.TeamMember.objects.all()
    serializer_class = serializers.TeamMemberSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        'team__name',
        'name',
        'university_entry_year',
        'phone_number',
        'student_number',
        'email',
    ]

    ordering_fields = [
        'team__name',
        'name',
        'university_entry_year',
        'phone_number',
        'student_number',
        'email',
    ]


class TeamMemberDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.TeamMember.objects.all()
    serializer_class = serializers.TeamMemberSerializer
    permission_classes = [permissions.IsAuthenticated]


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
        'coin',
    ]


class CTFQuestionListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.CTFQuestionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        'name', 'description', 'type', 'topic', 'file', 'is_shown',
        'created_at'
    ]
    ordering_fields = [
        'name', 'type', 'topic', 'file', 'is_shown',
        'creator', 'created_at'
    ]

    def get_queryset(self):
        return models.CTFQuestion.objects.filter(is_shown=True)


class CTFQuestionDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.CTFQuestion.objects.all()
    serializer_class = serializers.CTFQuestionSerializer
    permission_classes = [permissions.IsAdminUser]
