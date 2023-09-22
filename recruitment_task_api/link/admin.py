from django.contrib import admin

from .generate_expiring_link import is_link_expired
from .models import ExpiringLink


@admin.register(ExpiringLink)
class ExpiringLinkAdmin(admin.ModelAdmin):
    list_filter = ['expires_at']
    list_display = ('object_str', 'expires_at', 'is_expired')

    def is_expired(self, obj):
        return is_link_expired(obj)

    def object_str(self, obj):
        return str(obj)

    is_expired.boolean = True  # Display as a boolean (checkbox)
    is_expired.short_description = 'Expired'  # Custom column header
    object_str.short_description = 'Link'
