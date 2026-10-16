from decimal import Decimal
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from apps.schools.models import Campaign
from .utils import generate_protocol_number


class Evaluation(models.Model):
    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.CASCADE,
        related_name='evaluations',
        verbose_name='Campanha'
    )
    protocol = models.CharField(
        max_length=32,
        unique=True,
        db_index=True,
        verbose_name='Número de Protocolo'
    )
    # 5 Eixos Quantitativos (Notas 1 a 5)
    score_teaching = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='1. Ensino e Didática (1-5)'
    )
    score_infrastructure = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='2. Infraestrutura e Ambientes (1-5)'
    )
    score_hygiene = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='3. Higiene e Conservação (1-5)'
    )
    score_food = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='4. Alimentação e Cantina (1-5)'
    )
    score_coexistence = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='5. Convivência e Acolhimento (1-5)'
    )
    overall_score = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Média Geral'
    )
    # 6º Eixo: Sugestões e Propostas Gerais
    general_suggestions = models.TextField(
        blank=True,
        verbose_name='6. Propostas e Sugestões Gerais'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Enviada em')

    class Meta:
        verbose_name = 'Avaliação Discente'
        verbose_name_plural = 'Avaliações Discentes'
        ordering = ['-created_at']

    def __str__(self):
        return f"Protocolo {self.protocol} - {self.campaign.school.name} (Média: {self.overall_score})"

    def calculate_overall_score(self):
        scores = [
            self.score_teaching,
            self.score_infrastructure,
            self.score_hygiene,
            self.score_food,
            self.score_coexistence,
        ]
        avg = sum(scores) / len(scores)
        return Decimal(str(round(avg, 2)))

    def save(self, *args, **kwargs):
        if not self.protocol:
            proto = generate_protocol_number()
            while Evaluation.objects.filter(protocol=proto).exists():
                proto = generate_protocol_number()
            self.protocol = proto
        self.overall_score = self.calculate_overall_score()
        super().save(*args, **kwargs)


class EvaluationComment(models.Model):
    class Axis(models.TextChoices):
        TEACHING = 'ENSINO', 'Ensino e Didática'
        INFRASTRUCTURE = 'INFRAESTRUTURA', 'Infraestrutura'
        HYGIENE = 'HIGIENE', 'Higiene e Conservação'
        FOOD = 'ALIMENTACAO', 'Alimentação e Cantina'
        COEXISTENCE = 'CONVIVENCIA', 'Convivência e Acolhimento'
        SUGGESTION = 'SUGESTAO', 'Sugestões Gerais'

    class ModerationStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pendente de Moderação'
        APPROVED = 'APPROVED', 'Aprovado para Exibição Pública'
        REJECTED = 'REJECTED', 'Retido por Diretrizes Éticas'
        FLAGGED = 'FLAGGED', 'Sinalizado para Revisão Humana'

    evaluation = models.ForeignKey(
        Evaluation,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Avaliação'
    )
    axis = models.CharField(
        max_length=25,
        choices=Axis.choices,
        verbose_name='Eixo Temático'
    )
    comment = models.TextField(verbose_name='Texto do Comentário')
    moderation_status = models.CharField(
        max_length=20,
        choices=ModerationStatus.choices,
        default=ModerationStatus.PENDING,
        db_index=True,
        verbose_name='Status de Moderação'
    )
    rejection_reason = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Motivo de Retenção (se aplicável)'
    )
    moderated_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Moderado em'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')

    class Meta:
        verbose_name = 'Comentário de Avaliação'
        verbose_name_plural = 'Comentários de Avaliação'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_axis_display()} [{self.get_moderation_status_display()}] - {self.evaluation.protocol}"


class SchoolReply(models.Model):
    comment = models.OneToOneField(
        EvaluationComment,
        on_delete=models.CASCADE,
        related_name='school_reply',
        verbose_name='Comentário Moderado'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='school_replies',
        verbose_name='Autor da Resposta (Gestor)'
    )
    reply_text = models.TextField(verbose_name='Resposta Oficial da Direção')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Respondido em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        verbose_name = 'Resposta da Gestão Escolar'
        verbose_name_plural = 'Respostas da Gestão Escolar'
        ordering = ['-created_at']

    def __str__(self):
        return f"Resposta ao comentário #{self.comment_id} ({self.created_at.strftime('%d/%m/%Y')})"
