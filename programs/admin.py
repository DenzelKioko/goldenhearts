from django.contrib import admin
from .models import Program

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'created_by', 'start_date', 'is_active', 'date_created')
    list_filter = ('category', 'is_active', 'created_by')
    search_fields = ('name', 'description')
    ordering = ('-date_created',)
    
    fieldsets = (
        ('Program Information', {
            'fields': ('name', 'description', 'category', 'created_by', 'is_active')
        }),
        ('Schedule', {
            'fields': ('start_date', 'end_date')
        }),
    )
    
    readonly_fields = ('date_created',)
