from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import generics
from rest_framework import permissions

from core.models import CustomUser
from . import models
from . import serializers


class NotificationListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.Notification.objects.all()
    serializer_class = serializers.NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]


def index(request):
    return render(request, "staff/index.html")


class StaffListAPIView(generics.ListAPIView):
    queryset = CustomUser.objects.filter(is_staff=True)
    serializer_class = serializers.CustomStaffUserSerializer
    permission_classes = [permissions.IsAdminUser]


class StaffDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = get_user_model().objects.filter(is_staff=True)
    serializer_class = serializers.CustomStaffUserSerializer
    permission_classes = [permissions.IsAdminUser]


class ClarificationListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.Clarification.objects.all()
    serializer_class = serializers.ClarificationSerializer
    permission_classes = [permissions.IsAuthenticated]


class ClarificationDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Clarification.objects.all()
    serializer_class = serializers.ClarificationSerializer
    permission_classes = [permissions.IsAdminUser]
