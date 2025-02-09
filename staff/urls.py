from django.urls import path
from . import views

urlpatterns = [
  path('stafflistview/',StaffListView.as_view(),name='stafflistview')
]
