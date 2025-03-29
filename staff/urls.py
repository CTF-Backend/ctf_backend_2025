from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'notifications', views.NotificationListCreateAPIView, basename='notification')

urlpatterns = [
    path('staff/', views.StaffListAPIView.as_view(), name='staff-list'),
    path("staff/<int:pk>/", views.StaffDetail.as_view(), name="staff-detail"),

    path("clarifications/", views.ClarificationListCreateAPIView.as_view(), name='clarifications-list-create'),
    path('clarifications/<int:pk>/', views.ClarificationDetailAPIView.as_view(), name='clarification-detail'),

    path("notifications/", views.NotificationListCreateAPIView.as_view(), name='notifications-list-create'),
    path('notifications-index/', views.index, name='index'),

]
