from core import serializers
from rest_framework import generics
from dj_rest_auth.views import LoginView
from .serializers import CustomLoginSerializer


class TeamSignUpAPIView(generics.CreateAPIView):
    serializer_class = serializers.TeamSignUpSerializer


class StaffSignUpAPIView(generics.CreateAPIView):
    serializer_class = serializers.StaffSignUpSerializer


class CustomLoginView(LoginView):
    serializer_class = CustomLoginSerializer
