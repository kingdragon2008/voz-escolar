from django.contrib import admin
from .models import Evaluation, EvaluationComment, SchoolReply


class EvaluationCommentInline(admin.StackedInline):
    model = EvaluationComment
    extra = 0
    readonly_fields = ('created_at',)


class SchoolReplyInline(admin.StackedInline):
    model = SchoolReply
    extra = 0
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = (
        'protocol',
        'campaign',
        'overall_score',
        'score_teaching',
        'score_infrastructure',
        'score_hygiene',
        'score_food',
        'score_coexistence',
        'created_at'
    )
    list_filter = ('campaign__school', 'campaign', 'overall_score')
    search_fields = ('protocol', 'campaign__school__name')
    readonly_fields = ('protocol', 'overall_score', 'created_at')
    inlines = [EvaluationCommentInline]


@admin.register(EvaluationComment)
class EvaluationCommentAdmin(admin.ModelAdmin):
    list_display = (
        'evaluation',
        'axis',
        'moderation_status',
        'moderated_at',
        'created_at'
    )
    list_filter = ('axis', 'moderation_status', 'evaluation__campaign__school')
    search_fields = ('comment', 'evaluation__protocol', 'rejection_reason')
    readonly_fields = ('created_at',)
    inlines = [SchoolReplyInline]


@admin.register(SchoolReply)
class SchoolReplyAdmin(admin.ModelAdmin):
    list_display = ('comment', 'author', 'created_at')
    search_fields = ('reply_text', 'comment__comment', 'author__username')
