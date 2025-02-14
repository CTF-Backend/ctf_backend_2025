from django.urls import path

from . import views

urlpatterns = [
    path('clarifications/<int:pk>/', views.ClarificationDetailView.as_view(), name='clarification-detail'),
]
