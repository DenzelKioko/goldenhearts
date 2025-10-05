from django.contrib import admin
from .models import Feedback
from django.db import models
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'program', 'rating', 'date')
    list_filter = ('rating', 'date', 'program')
    search_fields = ('user__email', 'program__name', 'message')
    autocomplete_fields = ['user', 'program']
    readonly_fields = ('date',)
    
    # Custom admin action
    actions = ['mark_as_reviewed']

    def mark_as_reviewed(self, request, queryset):
        updated = queryset.update(message=models.F('message') + " [Reviewed]")
        self.message_user(request, f"{updated} feedback messages marked as reviewed.")
    mark_as_reviewed.short_description = "Mark selected feedback as reviewed"
