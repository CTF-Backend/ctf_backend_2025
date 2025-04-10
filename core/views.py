from core import serializers
from rest_framework import generics
from dj_rest_auth.views import LoginView
from .serializers import CustomLoginSerializer
from staff.serializers import CustomStaffUserSerializer
from .models import *
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status
from django.conf import settings
import requests
import json
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class TeamSignUpAPIView(generics.CreateAPIView):
    serializer_class = serializers.TeamSignUpSerializer


class StaffSignUpAPIView(generics.CreateAPIView):
    serializer_class = serializers.StaffSignUpSerializer


class CustomLoginView(LoginView):
    serializer_class = CustomLoginSerializer


class CustomUserDetailView(generics.RetrieveAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = CustomStaffUserSerializer


class Pay(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Initiate Zarinpal Payment",
        responses={
            200: openapi.Response(
                description="Payment initiated successfully",
                examples={
                    "application/json": {
                        "status": True,
                        "url": "https://zarinpal.com/startpay/<authority>",
                        "authority": "<authority>"
                    }
                }
            ),
            400: "Bad Request"
        }
    )
    def get(self, request):
        data = {
            "merchant_id": settings.MERCHANT,
            "amount": settings.AMOUNT,
            "description": settings.DESCRIPTION,
            "callback_url": settings.CALLBACK_URL,
        }
        data = json.dumps(data)
        headers = {'content-type': 'application/json',
                   'content-length': str(len(data))}
        try:
            response = requests.post(
                settings.ZP_API_REQUEST, data=data, headers=headers, timeout=10)
            if response.status_code == 200:
                response = response.json()
                if response['Status'] == 100:
                    authority = response['Authority']
                    Authority.objects.create(
                        user=request.user, authority=response['Authority'])
                    return Response({'status': True, 'url': settings.ZP_API_STARTPAY + str(authority), 'authority': authority})
                else:
                    return Response({'status': False, 'code': str(response['Status'])}, status=status.HTTP_400_BAD_REQUEST)
            return HttpResponse(response)

        except requests.exceptions.Timeout:
            return Response({'status': False, 'code': 'timeout'}, status=status.HTTP_400_BAD_REQUEST)
        except requests.exceptions.ConnectionError:
            return Response({'status': False, 'code': 'connection error'}, status=status.HTTP_400_BAD_REQUEST)


class Vrify(APIView):

    def get(self, request):
        authority = request.GET.get('Authority', '')
        data = {
            "MerchantID": settings.MERCHANT,
            "Amount": settings.AMOUNT,
            "Authority": authority,
        }
        data = json.dumps(data)
        headers = {'content-type': 'application/json',
                   'content-length': str(len(data))}
        response = requests.post(settings.ZP_API_VERIFY,
                                 data=data, headers=headers)
        redirect_url = settings.REDIRECT_PATH
        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:
                authority_object = None
                try:
                    authority_object = Authority.objects.get(
                        authority=authority)
                except Authority.DoesNotExist:

                    return Response(status=302, headers={'Location': f"{redirect_url}?status:False&message=Authority Doesnt Exist"})

                if (authority_object.verified):
                    return Response(status=302, headers={'Location': f"{redirect_url}?status:False&message=Authority Already Verified"})

                else:
                    setattr(authority_object.user, "payed", True)
                    authority_object.user.save()
                    setattr(authority_object, "verified", True)
                    authority_object.save()
                return Response(status=302, headers={'Location': f"{redirect_url}?status:True&RefID={response['RefID']}&message=transaction complete"})

            else:
                return Response(status=302, headers={'Location': f"{redirect_url}?status:False&RefID={response['RefID']}&message={str(response['Status'])}"})

        return response
