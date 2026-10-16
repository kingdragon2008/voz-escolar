from django.conf import settings
from django.db import models
from apps.schools.models import Campaign
from .utils import generate_single_code


class CodeBatch(models.Model):
    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.CASCADE,
        related_name='code_batches',
        verbose_name='Campanha'
    )
    generated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='generated_batches',
        verbose_name='Gerado por'
    )
    quantity = models.PositiveIntegerField(verbose_name='Quantidade de Códigos')
    target_group = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Turma/Segmento Destino',
        help_text='Ex: 3º Ano Ensino Médio - Turma A (Apenas para controle de entrega física, sem vínculo nominal)'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Gerado em')

    class Meta:
        verbose_name = 'Lote de Códigos'
        verbose_name_plural = 'Lotes de Códigos'
        ordering = ['-created_at']

    def __str__(self):
        return f"Lote #{self.pk} - {self.quantity} códigos ({self.campaign.title})"

    def generate_codes(self):
        """
        Gera os códigos associados a este lote em massa de forma segura e não colidente.
        """
        codes_to_create = []
        created_count = 0
        attempts = 0
        max_attempts = self.quantity * 5

        while created_count < self.quantity and attempts < max_attempts:
            code_str = generate_single_code()
            if not AccessCode.objects.filter(code=code_str).exists() and not any(c.code == code_str for c in codes_to_create):
                codes_to_create.append(
                    AccessCode(
                        batch=self,
                        campaign=self.campaign,
                        code=code_str
                    )
                )
                created_count += 1
            attempts += 1

        AccessCode.objects.bulk_create(codes_to_create)
        return len(codes_to_create)


class AccessCode(models.Model):
    batch = models.ForeignKey(
        CodeBatch,
        on_delete=models.CASCADE,
        related_name='codes',
        null=True,
        blank=True,
        verbose_name='Lote'
    )
    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.CASCADE,
        related_name='access_codes',
        verbose_name='Campanha'
    )
    code = models.CharField(
        max_length=32,
        unique=True,
        db_index=True,
        verbose_name='Código de Acesso'
    )
    is_used = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name='Já Utilizado'
    )
    used_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Utilizado em'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Criado em'
    )

    class Meta:
        verbose_name = 'Código de Acesso Anônimo'
        verbose_name_plural = 'Códigos de Acesso Anônimos'
        ordering = ['-created_at']

    def __str__(self):
        status = "Utilizado" if self.is_used else "Disponível"
        return f"{self.code} [{status}] ({self.campaign.school.name})"
