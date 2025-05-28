import json

from rest_framework import serializers
from core import serializers as core_serializers
from django.db import transaction
from . import models
from . import exceptions
from .CTF_K8S_main import main
from .models import CTFQuestionPort


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Team
        exclude = ('account',)


class TeamUpdateNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Team
        fields = [
            'name',
        ]
        read_only_fields = ['account', 'coin', 'score', 'status']


class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TeamMember
        exclude = ('team',)

    def create(self, validated_data):
        request = self.context.get('request')
        try:
            team = request.user.team
        except models.Team.DoesNotExist:
            raise exceptions.UserDoesNotHaveTeam()
        validated_data['team'] = team
        if models.TeamMember.objects.filter(team=team).count() >= 3:
            raise exceptions.MaxTeamMember()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        request = self.context.get('request')
        try:
            team = request.user.team
        except models.Team.DoesNotExist:
            raise exceptions.UserDoesNotHaveTeam()
        validated_data['team'] = team
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
            'type',
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
            'type',
            'score',
            'coin',
            'x_coordinate',
            'y_coordinate',
            'floor',
        ]


class CTFQuestionListCreateSerializer(serializers.ModelSerializer):
    creator = core_serializers.CustomUserSerializer(read_only=True)
    flag_ids = serializers.SerializerMethodField()
    flag_coins = serializers.SerializerMethodField()

    class Meta:
        model = models.CTFQuestion
        fields = '__all__'

    def get_flag_ids(self, obj):
        return list(obj.ctf_questions_flags.values_list('id', flat=True))

    def get_flag_coins(self, obj):
        return list(obj.ctf_questions_flags.values_list('coin', flat=True))

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user:
            validated_data['creator'] = request.user
        return super().create(validated_data)


class CTFQuestionDetailForStaffSerializer(serializers.ModelSerializer):
    creator = core_serializers.CustomUserSerializer(read_only=True)

    class Meta:
        model = models.CTFQuestion
        fields = '__all__'


class CTFQuestionDetailSerializer(serializers.ModelSerializer):
    creator = core_serializers.CustomUserSerializer(read_only=True)
    challenge_image_url = serializers.SerializerMethodField(read_only=True, allow_null=True)

    class Meta:
        model = models.CTFQuestion
        fields = '__all__'

    def get_challenge_image_url(self, obj):
        request = self.context.get('request')
        team = request.user.team
        if models.TeamChallengeImages.objects.filter(team_id=team, ctf_question_id=obj.id).exists():
            team_challenge_image = models.TeamChallengeImages.objects.get(team=team, ctf_question=obj)
            return team_challenge_image.url_str
        else:
            challenge_image = obj.challenge_image
            if challenge_image:
                ports = obj.ports.all()
                url_str = main.deploy_challenge(challenge_image, ports)
                models.TeamChallengeImages.objects.create(team=team, ctf_question=obj, url_str=url_str)
                return url_str
            return None

class CTFFlagsSerializer(serializers.ModelSerializer):
    creator = core_serializers.CustomUserSerializer(read_only=True)
    ctf_question = CTFQuestionListCreateSerializer(read_only=True)
    ctf_question_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = models.CTFFlags
        fields = ['id', 'ctf_question', 'ctf_question_id', 'flag', 'score', 'hint', 'coin', 'creator', 'created_at']

    def create(self, validated_data):
        flag_count = models.CTFQuestion.objects.get(id=validated_data['ctf_question_id']).flag_count
        if models.CTFFlags.objects.filter(ctf_question_id=validated_data['ctf_question_id']).count() >= flag_count:
            raise exceptions.FlagCountLimitation()
        request = self.context.get('request')
        if request and request.user:
            validated_data['creator'] = request.user
        return super().create(validated_data)


class CTFFlagsBaseSerializer(serializers.ModelSerializer):
    ctf_question = CTFQuestionListCreateSerializer(read_only=True)

    class Meta:
        model = models.CTFFlags
        fields = ['id', 'ctf_question', 'score', 'coin']


class TeamEscapeRoomQuestionReportSerializer(serializers.ModelSerializer):
    team = TeamSerializer(read_only=True)
    escape_room_question = EscapeRoomQuestionListCreateSerializer(read_only=True)

    class Meta:
        model = models.TeamEscapeRoomQuestion
        fields = ['id', 'team', 'escape_room_question', 'created_at']


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

            team, validated_data = self.counting_score(team, escape_room_question, validated_data)
            validated_data['team_id'] = team.id
            instance = super().create(validated_data)
            return instance

    def counting_score(self, team, escape_room_question, validated_data):
        total_score = escape_room_question.score
        total_coin = escape_room_question.coin
        solver_teams = models.TeamEscapeRoomQuestion.objects.filter(escape_room_question=escape_room_question)
        solver_teams_count = solver_teams.count() + 1
        denominator = (solver_teams_count * (solver_teams_count + 1)) // 2
        if solver_teams.count() != 0:

            i = solver_teams_count
            for solver_team in solver_teams:
                selected_team = solver_team.team
                team_escape_room_question_record = models.TeamEscapeRoomQuestion.objects.get(team=selected_team,
                                                                                             escape_room_question=escape_room_question)

                selected_team.score -= team_escape_room_question_record.score
                selected_team_score = (i // denominator) * total_score
                selected_team.score += selected_team_score
                team_escape_room_question_record.score = selected_team_score

                selected_team.coin -= team_escape_room_question_record.coin
                selected_team_coin = (i // denominator) * total_coin
                selected_team.coin += (i // denominator) * total_coin
                team_escape_room_question_record.coin = selected_team_coin

                selected_team.save()
                team_escape_room_question_record.save()
                i -= 1

        team.score += (1 // denominator) * total_score
        validated_data['score'] = (1 // denominator) * total_score
        team.coin += (1 // denominator) * total_coin
        validated_data['coin'] = (1 // denominator) * total_coin
        team.save()

        return team, validated_data


class TeamCTFFlagSerializer(serializers.ModelSerializer):
    team_answer = serializers.CharField(max_length=255, write_only=True)
    flag_id = serializers.IntegerField(write_only=True)

    team = TeamSerializer(read_only=True)
    flag = CTFFlagsSerializer(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = models.TeamCTFFlag
        fields = ['id', 'team_answer', 'team', 'flag_id', 'flag', 'created_at']

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
