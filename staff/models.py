from django.db import models
from . import consts


class Notification(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False, verbose_name="عنوان")
    description = models.TextField(null=True, blank=False, verbose_name="توضیحات")
    type = models.CharField(max_length=10, choices=consts.TYPE_CHOICES, default="info")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
