from django.urls import path
from .views import TeamSignUpAPIView, StaffSignUpAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('team/signup/', TeamSignUpAPIView.as_view(), name='team_signup'),
    path('staff/signup/', StaffSignUpAPIView.as_view(), name='staff_signup')

    # path('jwt/create/', TokenObtainPairView.as_view(), name='jwt_create')

]
