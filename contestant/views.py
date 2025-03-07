from rest_framework import generics, filters, status
from rest_framework.response import Response

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

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]


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


class CTFFlagsListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.CTFFlags.objects.all()
    serializer_class = serializers.CTFFlagsSerializer
    permission_classes = [permissions.IsAdminUser]


class CTFFlagsDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.CTFFlags.objects.all()
    serializer_class = serializers.CTFFlagsSerializer
    permission_classes = [permissions.IsAdminUser]


class FlagHintsListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.FlagHints.objects.all()
    serializer_class = serializers.FlagHintsSerializer
    permission_classes = [permissions.IsAdminUser]


class FlagHintsDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.FlagHints.objects.all()
    serializer_class = serializers.FlagHintsSerializer
    permission_classes = [permissions.IsAdminUser]


class TeamEscapeRoomQuestionListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.TeamEscapeRoomQuestion.objects.all()
    serializer_class = serializers.TeamEscapeRoomQuestionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        'team__name',
        'escape_room_question__name',
    ]

    ordering_fields = [
        'team__name',
        'escape_room_question__name',
        'created_at'
    ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        return Response({
            "message": "پاسخ شما با موفقیت ثبت شد.",
            "instance": self.get_serializer(instance).data
        }, status=status.HTTP_201_CREATED)
