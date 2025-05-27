from django.contrib import admin

from .models import Team, TeamMember


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


