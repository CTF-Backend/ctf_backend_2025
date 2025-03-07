from rest_framework import generics
from rest_framework import permissions
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from . import serializers
from . import models
from core.models import CustomUser


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


class StaffListAPIView(generics.ListAPIView):
    queryset = CustomUser.objects.filter(is_staff=True)
    serializer_class = serializers.CustomUserSerializer


class StaffDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = get_user_model().objects.filter(is_staff=True)
    serializer_class = serializers.CustomUserSerializer
    permission_classes = [permissions.IsAdminUser]
