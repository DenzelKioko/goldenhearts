# programs/urls.py
from django.urls import path
from . import views

app_name = 'programs'

urlpatterns = [
    # Public routes
    path('', views.ProgramListView.as_view(), name='program_list'),

    path('<int:pk>/', views.ProgramDetailView.as_view(), name='program_detail'),
    
    # Admin-only routes
    path('create/', views.ProgramCreateView.as_view(), name='program_create'),
    path('<int:pk>/edit/', views.ProgramUpdateView.as_view(), name='program_edit'),
    path('<int:pk>/delete/', views.ProgramDeleteView.as_view(), name='program_delete'),
]
