from rest_framework import generics
from rest_framework import permissions
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from . import serializers
from . import models


class NotificationCreateAPIView(generics.CreateAPIView):
    queryset = models.Notification.objects.all()
    serializer_class = serializers.NotificationSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        notification = serializer.save()
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "notifications",
            {
                "type": "send_notification",
                "title": notification.title,
                "description": notification.description,
                "notification_type": notification.type,
            }
        )


class ClarificationDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Clarification.objects.all()
    serializer_class = serializers.ClarificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
