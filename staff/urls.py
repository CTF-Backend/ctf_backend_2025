from django.urls import path
from . import views

urlpatterns = [
    path('stafflistview/', views.StaffListView.as_view(), name='stafflistview'),
    path("staff/<int:pk>/", views.StaffDetail.as_view(), name="staff-detail"),
]
