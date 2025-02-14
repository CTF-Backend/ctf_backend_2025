from rest_framework import serializers
from . import models


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Notification
        fields = "__all__"

class ClarificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Clarification
        fields = "__all__"