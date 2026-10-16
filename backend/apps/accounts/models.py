from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrador Geral'
        MODERATOR = 'MODERATOR', 'Moderador Ético'
        SCHOOL_MANAGER = 'SCHOOL_MANAGER', 'Gestor Escolar'

    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.SCHOOL_MANAGER,
        verbose_name='Perfil de Acesso'
    )
    phone = models.CharField(max_length=20, blank=True, verbose_name='Telefone/WhatsApp')
    is_verified = models.BooleanField(default=False, verbose_name='Conta Verificada')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última Atualização')

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['-date_joined']

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"

    @property
    def is_school_manager(self):
        return self.role == self.Roles.SCHOOL_MANAGER or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.Roles.MODERATOR or self.is_superuser
