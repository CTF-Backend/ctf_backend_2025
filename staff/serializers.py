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

    def update(self, instance, validated_data):
        request = self.context.get('request')
        if 'answer' in validated_data and (not request or not request.user.is_staff):
            raise serializers.ValidationError({"answer": "Only staff users can update this field."})
        return super().update(instance, validated_data) 
