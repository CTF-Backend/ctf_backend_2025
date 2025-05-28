from django.utils import timezone
from core.models import *
from . import consts


class Team(models.Model):
    account = models.OneToOneField(
        CustomUser, on_delete=models.PROTECT, related_name="team")
    name = models.CharField(max_length=255, verbose_name="نام تیم")
    score = models.IntegerField(verbose_name="امتیاز", default=0)
    coin = models.IntegerField(verbose_name="سکه", default=0)
    status = models.CharField(
        max_length=50, choices=consts.TEAM_STATUS_CHOICES, default="signed_up")

    def __str__(self):
        return self.name


class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.PROTECT,
                             related_name="team_members", verbose_name="تیم")
    name = models.CharField(max_length=255, verbose_name="نام")
    university_entry_year = models.IntegerField(verbose_name="سال ورودی")
    phone_number = models.CharField(max_length=255, verbose_name="شماره تلفن")
    student_number = models.CharField(
        max_length=255, verbose_name="شماره دانشجویی")
    email = models.EmailField(verbose_name="ایمیل")

    def __str__(self):
        return self.name


class EscapeRoomQuestion(models.Model):
    name = models.CharField(max_length=255, verbose_name="نام", unique=True)
    description = models.TextField(verbose_name="توضیحات")
    type = models.CharField(
        max_length=50, choices=consts.ESCAPEROOM_QUESTION_TOPIC_CHOICES, default="string", verbose_name="نوع")

    floor = models.IntegerField(verbose_name="طبقه")
    x_coordinate = models.CharField(max_length=255, verbose_name="مختصات طولی")
    y_coordinate = models.CharField(max_length=255, verbose_name="مختصات عرضی")

    flag = models.CharField(max_length=255, verbose_name="پرچم")
    answer_limitation = models.IntegerField(
        verbose_name="محدودیت تعداد پاسخ ها")
    score = models.IntegerField(verbose_name="امتیاز", default=0)
    coin = models.IntegerField(verbose_name="سکه", default=0)

    creator = models.ForeignKey(
        CustomUser, on_delete=models.PROTECT, related_name="escape_room_questions")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class CTFQuestion(models.Model):
    name = models.CharField(max_length=255, verbose_name="نام", unique=True)
    description = models.TextField(
        verbose_name="توضیحات", null=True, blank=True)
    type = models.CharField(max_length=50, choices=consts.CTF_QUESTION_TYPE_CHOICES,
                            default="file", verbose_name="نوع")
    topic = models.CharField(max_length=50, choices=consts.CTF_QUESTION_TOPIC_CHOICES,
                             default="steganography", verbose_name="موضوع")
    file = models.FileField(upload_to="uploads/", verbose_name="فایل", null=True, blank=True)
    is_shown = models.BooleanField(default=True, verbose_name="قابل مشاهده")
    flag_count = models.IntegerField(default=1, verbose_name="تعداد فلگ ها")
    challenge_image = models.CharField(max_length=255, verbose_name="ایمیج چالش", null=True, blank=True)

    creator = models.ForeignKey(
        CustomUser, on_delete=models.PROTECT, related_name="ctf_questions")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class TeamChallengeImages(models.Model):
    team = models.ForeignKey(Team, on_delete=models.PROTECT, related_name="team_challenge_images")
    url_str = models.CharField(max_length=700)
    ctf_question = models.ForeignKey(
        CTFQuestion, on_delete=models.PROTECT, related_name="team_challenge_images")


class CTFFlags(models.Model):
    ctf_question = models.ForeignKey(
        CTFQuestion, on_delete=models.PROTECT, related_name="ctf_questions_flags")
    flag = models.CharField(max_length=255, verbose_name="فلگ")
    score = models.IntegerField(verbose_name="امتیاز", default=0)
    hint = models.TextField(verbose_name="راهنمایی")
    coin = models.IntegerField(verbose_name="سکه", default=0)

    creator = models.ForeignKey(
        CustomUser, on_delete=models.PROTECT, related_name="ctf_flags")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.flag


class TeamEscapeRoomQuestion(models.Model):
    team = models.ForeignKey(Team, on_delete=models.PROTECT, related_name="escape_room_questions")
    escape_room_question = models.ForeignKey(EscapeRoomQuestion, on_delete=models.PROTECT)
    score = models.IntegerField(verbose_name="امتیاز", default=0)
    coin = models.IntegerField(verbose_name="سکه", default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class TeamCTFFlag(models.Model):
    team = models.ForeignKey(
        Team, on_delete=models.PROTECT, related_name="team_ctf_flag")
    flag = models.ForeignKey(
        CTFFlags, on_delete=models.PROTECT, related_name="team_ctf_flags")
    created_at = models.DateTimeField(auto_now_add=True)


class TeamCTFHint(models.Model):
    team = models.ForeignKey(
        Team, on_delete=models.PROTECT, related_name="team_ctf_hint")
    hint = models.ForeignKey(
        CTFFlags, on_delete=models.PROTECT, related_name="team_ctf_hints")
    created_at = models.DateTimeField(auto_now_add=True)


class Authority(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    authority = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.team}:{self.authority}"
