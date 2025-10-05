# programs/urls.py
from django.urls import path
from . import views

app_name = 'programs'

urlpatterns = [
    path('', views.ProgramListView.as_view(), name='program_list'),
    path('<int:pk>/', views.ProgramDetailView.as_view(), name='program_detail'),
]
