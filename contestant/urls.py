from django.urls import path
from contestant import views

urlpatterns = [
    path('teams/', views.TeamListAPIView.as_view(),
         name='teams'),
    path('teams/<int:pk>/', views.TeamDetailAPIView.as_view(),
         name='teams'),

    path('team-members/', views.TeamMemberListCreateAPIView.as_view(),
         name='team-members'),
    path('team-members/<int:pk>/', views.TeamMemberDetailAPIView.as_view(),
         name='team-members'),

    path('escape-room-questions/<int:pk>/', views.EscapeRoomQuestionDetailAPIView.as_view(),
         name='escape-room-question-detail'),
    path('escape-room-questions/', views.EscapeRoomQuestionListCreateAPIView.as_view(),
         name='escape-room-question'),
    path('escape-room-questions/contestans/', views.EscapeRoomQuestionForContestantsListAPIView.as_view(),
         name='escape-room-question-for-contestants'),

]
