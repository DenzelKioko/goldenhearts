from django.contrib import admin
from .models import Program


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_active', 'start_date', 'end_date')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'description')
    date_hierarchy = 'start_date'
    ordering = ('-start_date',)
    prepopulated_fields = {"name": ("category",)}  # optional if you want slug-style auto fill
    readonly_fields = ('date_created',)

    fieldsets = (
        ("Program Info", {
            "fields": ("name", "description", "category")
        }),
        ("Schedule", {
            "fields": ("start_date", "end_date")
        }),
        ("Management", {
            "fields": ("created_by", "is_active", "date_created")
        }),
    )
