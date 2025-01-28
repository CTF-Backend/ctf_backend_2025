from django.db import models
from core.models import *
from . import consts


class Team(models.Model):
    account = models.OneToOneField(CustomUser, on_delete=models.PROTECT, related_name='team')
    name = models.CharField(max_length=255, verbose_name="نام تیم")
    score = models.IntegerField(verbose_name="امتیاز", null=True, blank=True)
    coin = models.IntegerField(verbose_name="سکه", null=True, blank=True)
    status = models.CharField(max_length=50, choices=consts.TEAM_STATUS_CHOICES, default="signed_up")

    def __str__(self):
        return self.name


class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.PROTECT, related_name='team_members', verbose_name="تیم")
    name = models.CharField(max_length=255, verbose_name="نام", unique=True)
    university_entry_year = models.IntegerField(verbose_name="سال ورودی")
    phone_number = models.CharField(max_length=255, verbose_name="شماره تلفن")
    student_number = models.CharField(max_length=255, verbose_name="شماره دانشجویی")
    email = models.EmailField(verbose_name="ایمیل")

    def __str__(self):
        return self.name


class EscapeRoomQuestion(models.Model):
    name = models.CharField(max_length=255, verbose_name="نام", unique=True)
    description = models.TextField(verbose_name="توضیحات")

    floor = models.IntegerField(verbose_name="طبقه")
    x_coordinate = models.CharField(max_length=255, verbose_name="مختصات طولی")
    y_coordinate = models.CharField(max_length=255, verbose_name="مختصات عرضی")

    flag = models.CharField(max_length=255, verbose_name="پرچم")
    answer_limitation = models.IntegerField(verbose_name="محدودیت تعداد پاسخ ها")
    score = models.IntegerField(verbose_name="امتیاز")
    coin = models.IntegerField(verbose_name="سکه")

    creator = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name="escape_room_questions")
    created_at = models.DateTimeField(auto_now_add=True)
