from django.urls import path
from .views import EscapeRoomQuestionCreateAPIView

urlpatterns = [
    path('escape-room-questions/', EscapeRoomQuestionCreateAPIView.as_view(),
         name='create-escape-room-question'),
]
