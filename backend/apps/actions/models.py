from django.core.validators import MaxValueValidator
from django.db import models
from apps.schools.models import School, Campaign


class ActionPlan(models.Model):
    class Axis(models.TextChoices):
        TEACHING = 'ENSINO', 'Ensino e Didática'
        INFRASTRUCTURE = 'INFRAESTRUTURA', 'Infraestrutura'
        HYGIENE = 'HIGIENE', 'Higiene e Conservação'
        FOOD = 'ALIMENTACAO', 'Alimentação e Cantina'
        COEXISTENCE = 'CONVIVENCIA', 'Convivência e Acolhimento'
        GENERAL = 'GERAL', 'Geral / Institucional'

    class Status(models.TextChoices):
        PLANNED = 'PLANNED', 'Planejado'
        IN_PROGRESS = 'IN_PROGRESS', 'Em Andamento'
        COMPLETED = 'COMPLETED', 'Concluído'
        CANCELLED = 'CANCELLED', 'Cancelado'

    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name='action_plans',
        verbose_name='Escola'
    )
    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='action_plans',
        verbose_name='Campanha de Origem (opcional)'
    )
    axis = models.CharField(
        max_length=25,
        choices=Axis.choices,
        default=Axis.GENERAL,
        verbose_name='Eixo Prioritário'
    )
    title = models.CharField(max_length=200, verbose_name='Título do Plano de Melhoria')
    description = models.TextField(verbose_name='Descrição e Ações Concretas')
    responsible_department = models.CharField(
        max_length=150,
        verbose_name='Responsável / Setor',
        help_text='Ex: Coordenação de Infraestrutura, Direção Pedagógica, etc.'
    )
    deadline = models.DateField(verbose_name='Prazo Estimado de Entrega')
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PLANNED,
        verbose_name='Status de Execução'
    )
    progress_percentage = models.PositiveSmallIntegerField(
        default=0,
        validators=[MaxValueValidator(100)],
        verbose_name='Progresso (%)'
    )
    is_public = models.BooleanField(
        default=True,
        verbose_name='Visível na Página Pública da Escola'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        verbose_name = 'Plano de Melhoria'
        verbose_name_plural = 'Planos de Melhoria'
        ordering = ['status', 'deadline']

    def __str__(self):
        return f"[{self.get_axis_display()}] {self.title} - {self.get_status_display()} ({self.school.name})"
