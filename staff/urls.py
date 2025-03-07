from django.urls import path
from . import views

urlpatterns = [
    path('stafflistview/', views.StaffListAPIView.as_view(), name='staff-list'),
    path("staff/<int:pk>/", views.StaffDetail.as_view(), name="staff-detail"),
]
