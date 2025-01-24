from rest_framework import generics
from core import serializers
from rest_framework.permissions import IsAdminUser
from core import models
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView


class TeamSignUpAPIView(generics.CreateAPIView):
    serializer_class = serializers.TeamAuthSerializer


class LoginAPIView(APIView):
    pass
    # def post(self, request, *args, **kwargs):
