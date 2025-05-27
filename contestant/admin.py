from django.contrib import admin

from .models import Team, TeamMember
from django.contrib import admin
from .models import (
    EscapeRoomQuestion, CTFQuestion, CTFFlags,
    TeamEscapeRoomQuestion, TeamCTFFlag, TeamCTFHint, Authority
)


class TeamMemberInline(admin.TabularInline):
    model = TeamMember
    extra = 1
    verbose_name = "عضو تیم"
    verbose_name_plural = "اعضای تیم"


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'account', 'score', 'coin', 'status')
    list_filter = ('status',)
    search_fields = ('name', 'account__username')
    inlines = [TeamMemberInline]


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'team', 'university_entry_year',
                    'student_number', 'phone_number', 'email')
    list_filter = ('university_entry_year',)
    search_fields = ('name', 'student_number', 'email', 'phone_number')


@admin.register(EscapeRoomQuestion)
class EscapeRoomQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'floor', 'score', 'coin', 'creator', 'created_at')
    list_filter = ('floor', 'type', 'creator')
    search_fields = ('name', 'description', 'flag', 'creator__username')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)


@admin.register(CTFQuestion)
class CTFQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'topic', 'is_shown', 'flag_count', 'creator', 'created_at')
    list_filter = ('type', 'topic', 'is_shown', 'creator')
    search_fields = ('name', 'description', 'creator__username')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)


@admin.register(CTFFlags)
class CTFFlagsAdmin(admin.ModelAdmin):
    list_display = ('id', 'flag', 'score', 'coin', 'ctf_question', 'creator', 'created_at')
    list_filter = ('score', 'coin', 'creator')
    search_fields = ('flag', 'hint', 'creator__username', 'ctf_question__name')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)


@admin.register(TeamEscapeRoomQuestion)
class TeamEscapeRoomQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'team', 'escape_room_question', 'score', 'coin', 'created_at')
    list_filter = ('score', 'coin', 'team')
    search_fields = ('team__name', 'escape_room_question__name')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)


@admin.register(TeamCTFFlag)
class TeamCTFFlagAdmin(admin.ModelAdmin):
    list_display = ('id', 'team', 'flag', 'get_question_name', 'created_at')
    list_filter = ('team',)
    search_fields = ('team__name', 'flag__flag', 'flag__ctf_question__name')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

    def get_question_name(self, obj):
        return obj.flag.ctf_question.name

    get_question_name.short_description = "نام سوال مربوطه"


@admin.register(TeamCTFHint)
class TeamCTFHintAdmin(admin.ModelAdmin):
    list_display = ('id', 'team', 'get_hint_text', 'get_question_name', 'created_at')
    list_filter = ('team',)
    search_fields = ('team__name', 'hint__hint', 'hint__ctf_question__name')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

    def get_hint_text(self, obj):
        return obj.hint.hint

    get_hint_text.short_description = "راهنمایی"

    def get_question_name(self, obj):
        return obj.hint.ctf_question.name

    get_question_name.short_description = "نام سوال مربوطه"


@admin.register(Authority)
class AuthorityAdmin(admin.ModelAdmin):
    list_display = ('id', 'team', 'authority')
    list_filter = ('team',)
    search_fields = ('team__name', 'authority')
    ordering = ('id',)
