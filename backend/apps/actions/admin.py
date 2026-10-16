from django.contrib import admin
from .models import ActionPlan


@admin.register(ActionPlan)
class ActionPlanAdmin(admin.ModelAdmin):
    list_display = ('title', 'school', 'axis', 'responsible_department', 'deadline', 'status', 'progress_percentage', 'is_public')
    list_filter = ('axis', 'status', 'is_public', 'school')
    search_fields = ('title', 'description', 'responsible_department', 'school__name')
