from django.contrib import admin
from apps.notifications.models import NotificationLog


class NotificationLogAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'sent_at', 'message')
    search_fields = ('message', 'recipient')
    date_hierarchy = 'sent_at'
    ordering = ('-sent_at',)
    readonly_fields = ('sent_at',)


admin.site.register(NotificationLog, NotificationLogAdmin)
