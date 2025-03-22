from django.urls import path
from contestant import views
from rest_framework.urlpatterns import format_suffix_patterns

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

    path('ctf-questions/', views.CTFQuestionListCreateAPIView.as_view(),
         name='ctf-question'),
    path('ctf-questions/<int:pk>/', views.CTFQuestionDetailAPIView.as_view(),
         name='ctf-question-detail'),

    path('ctf-flags/', views.CTFFlagsListCreateAPIView.as_view(),
         name='ctf-flag'),
    path('ctf-flags/<int:pk>/', views.CTFFlagsDetailAPIView.as_view(),
         name='ctf-flags-detail'),

    path('team-escape-room/', views.TeamEscapeRoomQuestionListCreateAPIView.as_view(),
         name='team-escape-room'),
    path('team-ctf-flag/', views.TeamCTFFlagListCreateAPIView.as_view(),
         name='team-ctf-flag'),
    path('team-ctf-hint/', views.TeamCTFHintListCreateAPIView.as_view(),
         name='team-ctf-hint'),

    path('team-escape-room-report/', views.TeamEscapeRoomQuestionReport.as_view(),
         name='team-escape-room-report'),
    path('team-ctf-flag-report/', views.TeamCTFFlagReport.as_view(),
         name='team-ctf-flag-report'),
]
