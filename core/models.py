from django.db import models


class EscapeRoomQuestion(models.Model):
    name = models.CharField(max_length=255, verbose_name="نام", unique=True)
    description = models.TextField(verbose_name="توضیحات")

    floor = models.IntegerField(verbose_name="طبقه")
    x_coordinate = models.CharField(max_length=255, verbose_name="مختصات طولی")
    y_coordinate = models.CharField(max_length=255, verbose_name="مختصات عرضی")

    score = models.IntegerField(verbose_name="امتیاز")
    answer_limitation = models.IntegerField(verbose_name="محدودیت تعداد پاسخ ها")
    flag = models.CharField(max_length=255, verbose_name="پرچم")
    coin = models.IntegerField(verbose_name="مقدار سکه")

    # ToDo : add creator
    created_at = models.DateTimeField(auto_now_add=True)
