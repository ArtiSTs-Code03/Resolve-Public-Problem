from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Complaint

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('ticket_badge', 'complainant_name', 'category', 'status_badge', 'created_at', 'view_attachment')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('ticket_id', 'title', 'complainant_name', 'user__username')
    readonly_fields = ('ticket_id', 'created_at', 'updated_at', 'view_attachment')
    list_per_page = 15

    fieldsets = (
        ("Ticket Overview", {
            "fields": ("ticket_id", "complainant_name", "user", "category", "created_at", "updated_at")
        }),
        ("Grievance Details", {
            "fields": ("title", "description", "image", "view_attachment")
        }),
        ("Action & Resolution", {
            "fields": ("status", "admin_remark"),
            "classes": ("wide",)
        }),
    )

    def ticket_badge(self, obj):
        return format_html('<span style="font-weight: bold; color: #4f46e5;">{}</span>', obj.ticket_id)
    ticket_badge.short_description = "Ticket ID"

    def status_badge(self, obj):
        colors = {
            'Pending': '#b45309',
            'In Progress': '#0369a1',
            'Resolved': '#15803d',
            'Rejected': "#ba133d",
        }
        bg_colors = {
            'Pending': '#fef3c7',
            'In Progress': '#e0f2fe',
            'Resolved': '#dcfce7',
            'Rejected': '#ffe4e6',
        }
        color = colors.get(obj.status, '#333')
        bg = bg_colors.get(obj.status, '#eee')
        return format_html(
            '<span style="background-color: {}; color: {}; padding: 4px 10px; border-radius: 12px; font-weight: 600; font-size: 11px;">{}</span>',
            bg, color, obj.status
        )
    status_badge.short_description = "Current Status"

    def view_attachment(self, obj):
        if obj.image:
            return format_html('<a href="{}" target="_blank" style="color: #4f46e5; font-weight: 600;">Open Proof</a>', obj.image.url)
        return "—"
    view_attachment.short_description = "Attachment"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)