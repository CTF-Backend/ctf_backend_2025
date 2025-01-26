from core import serializers
from rest_framework import generics
from dj_rest_auth.views import LoginView, LogoutView
from .serializers import CustomLoginSerializer
from . import exceptions


class TeamSignUpAPIView(generics.CreateAPIView):
    serializer_class = serializers.TeamAuthSerializer


class StaffSignUpAPIView(generics.CreateAPIView):
    serializer_class = serializers.StaffAuthSerializer


class CustomLoginView(LoginView):
    serializer_class = CustomLoginSerializer
