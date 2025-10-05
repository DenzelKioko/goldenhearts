from django.contrib import admin
from .models import Program
from events.models import Event
from donations.models import Donation
from feedback.models import Feedback


# --- Inline models for related content ---
class EventInline(admin.TabularInline):
    model = Event
    extra = 0
    fields = ('title', 'date', 'location', 'organizer')
    show_change_link = True


class DonationInline(admin.TabularInline):
    model = Donation
    extra = 0
    fields = ('donor', 'donation_type', 'amount', 'date')
    readonly_fields = ('date',)
    show_change_link = True


class FeedbackInline(admin.TabularInline):
    model = Feedback
    extra = 0
    fields = ('user', 'rating', 'message', 'date')
    readonly_fields = ('date',)
    show_change_link = True


# --- Main Program Admin ---
@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'created_by', 'start_date', 'end_date', 'is_active', 'total_donations', 'average_rating')
    list_filter = ('category', 'is_active', 'created_by')
    search_fields = ('name', 'description', 'created_by__email')
    ordering = ('-date_created',)
    autocomplete_fields = ['created_by']

    inlines = [EventInline, DonationInline, FeedbackInline]

    fieldsets = (
        ('Program Information', {
            'fields': ('name', 'description', 'category', 'created_by', 'is_active')
        }),
        ('Schedule', {
            'fields': ('start_date', 'end_date')
        }),
        ('Metadata', {
            'fields': ('date_created',),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('date_created', 'total_donations', 'average_rating')

    def total_donations(self, obj):
        """Sum all monetary donations linked to this program."""
        donations = obj.donations.filter(donation_type='money')
        total = sum(d.amount or 0 for d in donations)
        return f"${total:,.2f}"
    total_donations.short_description = "Total Donations"

    def average_rating(self, obj):
        """Compute average feedback rating."""
        feedbacks = obj.feedback.all()
        if not feedbacks.exists():
            return "No feedback yet"
        avg = sum(f.rating for f in feedbacks) / feedbacks.count()
        return f"{avg:.1f}/10"
    average_rating.short_description = "Average Rating"

    actions = ['deactivate_programs', 'activate_programs']

    def deactivate_programs(self, request, queryset):
        """Deactivate selected programs."""
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} program(s) deactivated.")
    deactivate_programs.short_description = "Deactivate selected programs"

    def activate_programs(self, request, queryset):
        """Reactivate selected programs."""
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} program(s) reactivated.")
    activate_programs.short_description = "Reactivate selected programs"
