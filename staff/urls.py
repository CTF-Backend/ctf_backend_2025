from django.urls import path
from .views import StaffUserRetrieveUpdateDestroyAPIView
urlpatterns = [
    path("staff/<int:pk>/", StaffUserRetrieveUpdateDestroyAPIView.as_view(),
         name="staff-user-retrieve-update-destroy"),

]
