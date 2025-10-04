from django.contrib import admin
from .models import Donation
from django.db import models

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('donor', 'donation_type', 'amount', 'program', 'date')
    list_filter = ('donation_type', 'date', 'program')
    search_fields = ('donor__email', 'description')
    ordering = ('-date',)
    readonly_fields = ('date',)

    fieldsets = (
        ("Donor Details", {
            "fields": ("donor", "program")
        }),
        ("Donation Info", {
            "fields": ("donation_type", "amount", "description")
        }),
        ("Timestamps", {
            "fields": ("date",),
        }),
    )
    date_hierarchy = 'date'
    autocomplete_fields = ('donor', 'program')
    raw_id_fields = ('donor', 'program')
    # Pagination
    list_per_page = 25
    # Enable saving as new
    save_as = True
    save_on_top = True
    # Actions
    actions = ['mark_as_reviewed']
    def mark_as_reviewed(self, request, queryset):
        updated = queryset.update(description=models.F('description') + " [Reviewed]")
        self.message_user(request, f"{updated} donations marked as reviewed.")
    mark_as_reviewed.short_description = "Mark selected donations as reviewed"
    # Date hierarchy for easy navigation
    