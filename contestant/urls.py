from django.urls import path
from .views import EscapeRoomQuestionListCreateAPIView

urlpatterns = [
    path('escape-room-questions/', EscapeRoomQuestionListCreateAPIView.as_view(),
         name='create-escape-room-question'),
]
