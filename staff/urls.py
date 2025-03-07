from django.urls import path
from . import views

urlpatterns = [
  path('stafflistview/',StaffListView.as_view(),name='stafflistview')

from .views import StaffUserRetrieveUpdateDestroyAPIView
urlpatterns = [
    path("staff/<int:pk>/", StaffUserRetrieveUpdateDestroyAPIView.as_view(),
         name="staff-user-retrieve-update-destroy"),
]
