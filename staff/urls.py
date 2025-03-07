from django.urls import path
from . import views



urlpatterns = [
    path('staff/', views.StaffListAPIView.as_view(), name='staff-list'),
    path("staff/<int:pk>/", views.StaffDetail.as_view(), name="staff-detail"),
  
    path("clarifications/", views.ClarificationListCreateAPIView.as_view(), name='clarifications-list-create'),
    path('clarifications/<int:pk>/', views.ClarificationDetailView.as_view(), name='clarification-detail'),
]
