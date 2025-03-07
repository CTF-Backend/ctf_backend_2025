from rest_framework import serializers
from core import serializers as core_serializers
from django.db import transaction
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


class CTFFlagsSerializer(serializers.ModelSerializer):
    creator = core_serializers.CustomUserSerializer(read_only=True)
    ctf_question = CTFQuestionSerializer(read_only=True)
    ctf_question_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = models.CTFFlags
        fields = ['id', 'ctf_question', 'ctf_question_id', 'flag', 'score', 'hint', 'coin', 'creator', 'created_at']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user:
            validated_data['creator'] = request.user
        return super().create(validated_data)


class CTFFlagsBaseSerializer(serializers.ModelSerializer):
    ctf_question = CTFQuestionSerializer(read_only=True)

    class Meta:
        model = models.CTFFlags
        fields = ['id', 'ctf_question', 'score', 'coin']


class TeamEscapeRoomQuestionSerializer(serializers.ModelSerializer):
    team_answer = serializers.CharField(max_length=255, write_only=True)
    escape_room_question_id = serializers.IntegerField(write_only=True)

    team = TeamSerializer(read_only=True)
    escape_room_question = EscapeRoomQuestionForContestantsListSerializer(read_only=True)

    class Meta:
        model = models.TeamEscapeRoomQuestion
        fields = ['id', 'team_answer', 'team', 'escape_room_question', 'escape_room_question_id']

    def create(self, validated_data):
        team_answer = validated_data.pop('team_answer')

        escape_room_question_id = validated_data.get('escape_room_question_id')
        request = self.context.get('request')
        with transaction.atomic():
            escape_room_question = models.EscapeRoomQuestion.objects.select_for_update().get(id=escape_room_question_id)
            try:
                team = request.user.team
            except models.Team.DoesNotExist:
                raise exceptions.UserDoesNotHaveTeam()
            flag = escape_room_question.flag
            correct_answers_count = models.TeamEscapeRoomQuestion.objects.select_for_update().filter(
                escape_room_question=escape_room_question
            ).count()
            if correct_answers_count >= escape_room_question.answer_limitation:
                raise exceptions.AnswerLimitExceeded()
            elif (models.TeamEscapeRoomQuestion.objects.filter
                (team=team, escape_room_question=escape_room_question).exists()):
                raise exceptions.FlagIsDuplicate()
            elif team_answer != flag:
                raise exceptions.FlagIsWrong()

            team.score += escape_room_question.score
            team.coin += escape_room_question.coin
            team.save()

            validated_data['team_id'] = team.id
            instance = super().create(validated_data)
            return instance


class TeamCTFFlagSerializer(serializers.ModelSerializer):
    team_answer = serializers.CharField(max_length=255, write_only=True)
    flag_id = serializers.IntegerField(write_only=True)

    team = TeamSerializer(read_only=True)
    flag = CTFFlagsBaseSerializer(read_only=True)

    class Meta:
        model = models.TeamCTFFlag
        fields = ['id', 'team_answer', 'team', 'flag_id', 'flag', ]

    def create(self, validated_data):
        team_answer = validated_data.pop('team_answer')

        flag_id = validated_data.get('flag_id')
        request = self.context.get('request')

        with transaction.atomic():
            ctf_flag = models.CTFFlags.objects.get(id=flag_id)
            try:
                team = request.user.team
            except models.Team.DoesNotExist:
                raise exceptions.UserDoesNotHaveTeam()
            flag = ctf_flag.flag

            if (models.TeamCTFFlag.objects.filter
                (team=team, flag=ctf_flag).exists()):
                raise exceptions.FlagIsDuplicate()
            elif team_answer != flag:
                raise exceptions.FlagIsWrong()

            team.score += ctf_flag.score
            team.save()

            validated_data['team_id'] = team.id
            instance = super().create(validated_data)
            return instance


class TeamCTFHintSerializer(serializers.ModelSerializer):
    hint_id = serializers.IntegerField(write_only=True)
    team = TeamSerializer(read_only=True)

    class Meta:
        model = models.TeamCTFHint
        fields = ['id', 'team', 'hint_id', ]

    def create(self, validated_data):
        ctf_flag_hint_id = validated_data.get('hint_id')
        request = self.context.get('request')

        with transaction.atomic():
            ctf_flag_hint = models.CTFFlags.objects.get(id=ctf_flag_hint_id)
            try:
                team = request.user.team
            except models.Team.DoesNotExist:
                raise exceptions.UserDoesNotHaveTeam()

            existing_hint = models.TeamCTFHint.objects.filter(team=team, hint=ctf_flag_hint).first()
            if existing_hint:
                return existing_hint
            elif team.coin < ctf_flag_hint.coin:
                raise exceptions.CoinIsNotEnough()

            team.coin -= ctf_flag_hint.coin
            team.save()

            validated_data['team_id'] = team.id
            instance = super().create(validated_data)
            return instance
