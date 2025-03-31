from core import serializers
from rest_framework import generics
from dj_rest_auth.views import LoginView
from .serializers import CustomLoginSerializer
from staff.serializers import CustomStaffUserSerializer
from django.contrib.auth import get_user_model


class TeamSignUpAPIView(generics.CreateAPIView):
    serializer_class = serializers.TeamSignUpSerializer


class StaffSignUpAPIView(generics.CreateAPIView):
    serializer_class = serializers.StaffSignUpSerializer


class CustomLoginView(LoginView):
    serializer_class = CustomLoginSerializer


class CustomUserDetailView(generics.RetrieveAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = CustomStaffUserSerializer
