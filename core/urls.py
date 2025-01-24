from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('team/signup', TokenObtainPairView.as_view(), name='jwt_create'),


    path('jwt/create/', TokenObtainPairView.as_view(), name='jwt_create')

]
