from django.db import models
from core.models import CustomUser
from . import consts


class Notification(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False, verbose_name="عنوان")
    description = models.TextField(null=True, blank=False, verbose_name="توضیحات")
    type = models.CharField(max_length=10, choices=consts.TYPE_CHOICES, default="info", verbose_name="نوع")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Clarification(models.Model):
    question = models.TextField(verbose_name="سوال")
    answer = models.TextField(verbose_name="پاسخ")

    questioner = models.ForeignKey(CustomUser, on_delete=models.PROTECT,
                                   verbose_name="سوال کننده", related_name="questioner")
    responder = models.ForeignKey(CustomUser, on_delete=models.PROTECT,
                                  verbose_name="پاسخ دهنده", related_name="responder")
    created_at = models.DateTimeField(auto_now_add=True)
