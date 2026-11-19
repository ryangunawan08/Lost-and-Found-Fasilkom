from django.contrib import admin
from .models import Item

# Register your models here.

# Dekorator
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "report_type",
        "category",
        "location",
        "location_detail",
        "status",
        "reporter",
        "incident_date",
        "created_at",
    )
    list_filter = ("report_type", "status", "category", "location", "incident_date")
    search_fields = (
        "name",
        "description",
        "location_detail",
        "reporter__username",
        "reporter__email",
    )
    list_editable = ("status",)
    readonly_fields = ("created_at", "updated_at")