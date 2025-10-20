from django.contrib import admin
from .models import Event, Registration

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'date', 'time', 'location', 'capacity', 
        'registered_count', 'approved_registrations_count', 'available_spots', 'is_full'
    ]
    list_filter = ['date', 'location', 'created_at']
    search_fields = ['title', 'description', 'location']
    readonly_fields = ['created_at', 'updated_at', 'registered_count', 'approved_registrations_count']
    date_hierarchy = 'date'
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # If creating a new event
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'event', 'registration_date', 'approved', 
        'is_checked_in', 'can_check_in'
    ]
    list_filter = ['approved', 'is_checked_in', 'registration_date', 'event']
    search_fields = ['user__email', 'user__first_name', 'user__last_name', 'event__title']
    list_editable = ['approved', 'is_checked_in']
    readonly_fields = ['registration_date']
    raw_id_fields = ['user', 'event']