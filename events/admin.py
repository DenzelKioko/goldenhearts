from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'program', 'date', 'location', 'organizer', 'is_upcoming')
    list_filter = ('program', 'date')
    search_fields = ('title', 'description', 'location', 'organizer__email')
    ordering = ('-date',)
    autocomplete_fields = ['program', 'organizer']
    date_hierarchy = 'date'

    # Read-only fields for audit clarity
    readonly_fields = ('is_upcoming',)

    fieldsets = (
        ("Event Details", {
            'fields': ('title', 'program', 'description', 'date', 'location')
        }),
        ("Organizer Information", {
            'fields': ('organizer',)
        }),
    )

    def is_upcoming(self, obj):
        """Display whether the event is upcoming or past."""
        from django.utils import timezone
        return "✅ Upcoming" if obj.date > timezone.now() else "🕒 Past"
    is_upcoming.short_description = "Status"

    actions = ['mark_as_past']

    def mark_as_past(self, request, queryset):
        """Mark selected events as completed (adds text to title)."""
        updated = 0
        for event in queryset:
            if not event.title.endswith(" (Completed)"):
                event.title += " (Completed)"
                event.save()
                updated += 1
        self.message_user(request, f"{updated} event(s) marked as completed.")
    mark_as_past.short_description = "Mark selected events as completed"
