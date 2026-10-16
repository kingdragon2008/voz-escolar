from django.contrib import admin
from .models import CodeBatch, AccessCode


class AccessCodeInline(admin.TabularInline):
    model = AccessCode
    extra = 0
    readonly_fields = ('code', 'is_used', 'used_at', 'created_at')
    can_delete = False


@admin.register(CodeBatch)
class CodeBatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'campaign', 'quantity', 'target_group', 'generated_by', 'created_at')
    list_filter = ('campaign__school', 'campaign')
    search_fields = ('target_group', 'campaign__title', 'campaign__school__name')
    readonly_fields = ('created_at',)
    inlines = [AccessCodeInline]

    def save_model(self, request, obj, form, change):
        if not change and not obj.generated_by:
            obj.generated_by = request.user
        super().save_model(request, obj, form, change)
        if not change:
            # Gerar os códigos automaticamente na criação do lote
            obj.generate_codes()


@admin.register(AccessCode)
class AccessCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'campaign', 'is_used', 'used_at', 'created_at')
    list_filter = ('is_used', 'campaign__school', 'campaign')
    search_fields = ('code', 'campaign__school__name')
    readonly_fields = ('code', 'is_used', 'used_at', 'created_at')
