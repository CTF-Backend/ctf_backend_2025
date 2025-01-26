from django.urls import path
from .views import TeamSignUpAPIView, StaffSignUpAPIView, CustomLoginView
from dj_rest_auth.views import LogoutView

urlpatterns = [
    path('auth/signup/team/', TeamSignUpAPIView.as_view(), name='team_signup'),
    path('auth/signup/staff/', StaffSignUpAPIView.as_view(), name='staff_signup'),
    path('auth/login/', CustomLoginView.as_view(), name='custom_login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
]
