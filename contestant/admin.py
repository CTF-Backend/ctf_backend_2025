from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Team, TeamMember
from core.models import CustomUser
from django.utils.translation import gettext_lazy as _


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name',
                    'is_active', 'is_staff', 'is_superuser', 'is_team')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'is_team')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)

    fieldsets = (
        (_('اطلاعات حساب'), {
         'fields': ('username', 'password')}),
        (_('اطلاعات شخصی'), {
         'fields': ('first_name', 'last_name', 'email')}),
        (_('دسترسی‌ها'), {
         'fields': ('is_active', 'is_staff', 'is_superuser', 'is_team', 'groups', 'user_permissions')}),
        (_('تاریخ‌ها'), {
         'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'is_active', 'is_staff', 'is_team', 'is_superuser')}
         ),
    )


class TeamMemberInline(admin.TabularInline):
    model = TeamMember
    extra = 1
    verbose_name = "عضو تیم"
    verbose_name_plural = "اعضای تیم"


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'account', 'score', 'coin', 'status')
    list_filter = ('status',)
    search_fields = ('name', 'account__username')
    inlines = [TeamMemberInline]


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'team', 'university_entry_year',
                    'student_number', 'phone_number', 'email')
    list_filter = ('university_entry_year',)
    search_fields = ('name', 'student_number', 'email', 'phone_number')


admin.site.register(CustomUser, CustomUserAdmin)
