from django.urls import path
from . import views
urlpatterns = [
    path("staff/<int:pk>/", views.StaffDetail.as_view(),
         name="staff-detail"),

]
