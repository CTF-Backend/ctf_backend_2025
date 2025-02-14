from django.urls import path
from .views import ClarificationListCreateAPIView

urlpatterns = [
    path("clarifications/", ClarificationListCreateAPIView.as_view(), name='clarifications-list-create'),
]
