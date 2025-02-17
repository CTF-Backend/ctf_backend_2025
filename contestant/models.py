from django.db import models
from core.models import *
from . import consts


class Team(models.Model):
    account = models.OneToOneField(CustomUser, on_delete=models.PROTECT, related_name="team")
    name = models.CharField(max_length=255, verbose_name="نام تیم")
    score = models.IntegerField(verbose_name="امتیاز", null=True, blank=True)
    coin = models.IntegerField(verbose_name="سکه", null=True, blank=True)
    status = models.CharField(max_length=50, choices=consts.TEAM_STATUS_CHOICES, default="signed_up")

    def __str__(self):
        return self.name


class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.PROTECT, related_name="team_members", verbose_name="تیم")
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


class CTFQuestion(models.Model):
    name = models.CharField(max_length=255, verbose_name="نام", unique=True)
    description = models.TextField(verbose_name="توضیحات", null=True, blank=True)
    type = models.CharField(max_length=50, choices=consts.CTF_QUESTION_TYPE_CHOICES,
                            default="file", verbose_name="نوع")
    topic = models.CharField(max_length=50, choices=consts.CTF_QUESTION_TOPIC_CHOICES,
                             default="steganography", verbose_name="موضوع")
    file = models.FileField(upload_to="uploads/", verbose_name="فایل")
    is_shown = models.BooleanField(default=True, verbose_name="قابل مشاهده")

    creator = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name="ctf_questions")
    created_at = models.DateTimeField(auto_now_add=True)


class CTFFlags(models.Model):
    ctf_question = models.ForeignKey(CTFQuestion, on_delete=models.PROTECT, related_name="ctf_questions_flags")
    flag = models.CharField(max_length=255, verbose_name="فلگ")
    score = models.IntegerField(verbose_name="امتیاز")

    creator = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name="ctf_flags")
    created_at = models.DateTimeField(auto_now_add=True)


class FlagHints(models.Model):
    flag = models.ForeignKey(CTFFlags, on_delete=models.PROTECT, related_name="ctf_flag_hints")
    hint = models.TextField(verbose_name="راهنمایی")
    coin = models.IntegerField(verbose_name="سکه")

    creator = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name="flag_hints")
    created_at = models.DateTimeField(auto_now_add=True)


class TeamEscapeRoomQuestion(models.Model):
    team = models.ForeignKey(Team, on_delete=models.PROTECT, related_name="escape_room_questions")
    escape_room_question = models.ForeignKey(EscapeRoomQuestion, on_delete=models.PROTECT)


class TeamCTFFlags(models.Model):
    team = models.ForeignKey(Team, on_delete=models.PROTECT, related_name="ctf_flags")
    flag = models.ForeignKey(CTFFlags, on_delete=models.PROTECT)
