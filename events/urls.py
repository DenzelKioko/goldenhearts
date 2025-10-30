from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    # Public routes
    path('', views.event_list, name='event_list'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('program/<int:program_id>/events/', views.events_by_program, name='events_by_program'),
    
    # Patron routes
    path('my-registrations/', views.my_registrations, name='my_registrations'),
    path('registration/<int:reg_id>/cancel/', views.cancel_registration, name='cancel_registration'),
    
    # Admin routes
    path('event/add/', views.event_create, name='event_create'),
    path('event/<int:event_id>/edit/', views.event_edit, name='event_edit'),
    path('event/<int:event_id>/registrations/', views.manage_registrations, name='manage_registrations'),
    path('registration/<int:reg_id>/approve/', views.approve_registration, name='approve_registration'),
    path('registration/<int:reg_id>/reject/', views.reject_registration, name='reject_registration'),
    path('registration/<int:reg_id>/checkin/', views.check_in_registration, name='check_in_registration'),
]