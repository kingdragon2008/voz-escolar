from django.contrib import admin
from .models import ModerationLog


@admin.register(ModerationLog)
class ModerationLogAdmin(admin.ModelAdmin):
    list_display = ('comment', 'action', 'moderator', 'reason', 'ai_confidence_score', 'created_at')
    list_filter = ('action', 'created_at')
    search_fields = ('comment__comment', 'reason', 'moderator__username')
    readonly_fields = ('created_at',)
