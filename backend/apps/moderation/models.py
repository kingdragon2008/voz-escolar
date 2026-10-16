from django.conf import settings
from django.db import models
from apps.evaluations.models import EvaluationComment


class ModerationLog(models.Model):
    class Action(models.TextChoices):
        AUTO_APPROVED = 'AUTO_APPROVED', 'Aprovação Automática (Filtro Ético)'
        HUMAN_APPROVED = 'HUMAN_APPROVED', 'Aprovação por Moderador Humano'
        HUMAN_REJECTED = 'HUMAN_REJECTED', 'Retenção por Moderador Humano'
        AUTO_FLAGGED = 'AUTO_FLAGGED', 'Sinalizado pelo Filtro para Revisão'

    comment = models.ForeignKey(
        EvaluationComment,
        on_delete=models.CASCADE,
        related_name='moderation_logs',
        verbose_name='Comentário'
    )
    moderator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='moderation_actions',
        verbose_name='Moderador Responsável'
    )
    action = models.CharField(
        max_length=25,
        choices=Action.choices,
        verbose_name='Ação de Moderação'
    )
    reason = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Motivo / Justificativa'
    )
    ai_confidence_score = models.FloatField(
        null=True,
        blank=True,
        verbose_name='Score de Confiança Heurístico/IA'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data da Ação')

    class Meta:
        verbose_name = 'Log de Moderação Ética'
        verbose_name_plural = 'Logs de Moderação Ética'
        ordering = ['-created_at']

    def __str__(self):
        return f"Moderação #{self.pk} - {self.get_action_display()} (Comentário #{self.comment_id})"
