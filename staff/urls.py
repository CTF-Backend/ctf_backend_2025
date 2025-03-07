from django.urls import path
from . import views

urlpatterns = [
    path('staff/', views.StaffListAPIView.as_view(), name='staff-list'),
    path("staff/<int:pk>/", views.StaffDetail.as_view(), name="staff-detail"),
  
    path("clarifications/", ClarificationListCreateAPIView.as_view(), name='clarifications-list-create'),
]
