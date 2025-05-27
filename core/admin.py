from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.utils.translation import gettext_lazy as _


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('id', 'username', 'email', 'first_name', 'last_name',
                    'is_active', 'is_staff', 'is_superuser', 'is_team', 'date_joined')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'is_team')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)

    readonly_fields = ('last_login', 'date_joined')  # ⬅️ این خط اضافه شده

    fieldsets = (
        (_('اطلاعات حساب'), {
            'fields': ('username', 'password')}),
        (_('اطلاعات شخصی'), {
            'fields': ('first_name', 'last_name', 'email')}),
        (_('دسترسی‌ها'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'is_team', 'groups', 'user_permissions')}),
        (_('تاریخ‌ها'), {
            'fields': ('last_login', 'date_joined')}),  # ⬅️ حالا فقط نمایش داده می‌شود
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name',
                       'password1', 'password2', 'is_active', 'is_staff', 'is_team', 'is_superuser')}
         ),
    )


admin.site.register(CustomUser, CustomUserAdmin)
