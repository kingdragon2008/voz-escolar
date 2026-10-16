from django.conf import settings
from django.db import models
from django.utils.text import slugify


class School(models.Model):
    class SchoolType(models.TextChoices):
        PUBLIC_STATE = 'ESTADUAL', 'Pública Estadual'
        PUBLIC_MUNICIPAL = 'MUNICIPAL', 'Pública Municipal'
        PUBLIC_FEDERAL = 'FEDERAL', 'Pública Federal'
        PRIVATE = 'PRIVADA', 'Privada'

    name = models.CharField(max_length=255, verbose_name='Nome da Instituição')
    slug = models.SlugField(max_length=255, unique=True, blank=True, verbose_name='Slug/URL')
    inep_code = models.CharField(max_length=20, blank=True, null=True, unique=True, verbose_name='Código INEP/MEC')
    city = models.CharField(max_length=120, verbose_name='Cidade')
    state = models.CharField(max_length=2, verbose_name='UF')
    address = models.CharField(max_length=255, blank=True, verbose_name='Endereço Completo')
    school_type = models.CharField(
        max_length=20,
        choices=SchoolType.choices,
        default=SchoolType.PUBLIC_STATE,
        verbose_name='Esfera/Tipo'
    )
    is_verified = models.BooleanField(default=True, verbose_name='Instituição Verificada')
    min_quorum = models.PositiveIntegerField(
        default=10,
        verbose_name='Quórum Mínimo de Respostas',
        help_text='Número mínimo de avaliações necessárias para liberar os dados publicamente.'
    )
    about = models.TextField(blank=True, verbose_name='Sobre a Escola / Apresentação')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Cadastrada em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizada em')

    class Meta:
        verbose_name = 'Escola'
        verbose_name_plural = 'Escolas'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.city}/{self.state}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while School.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class SchoolMember(models.Model):
    class MemberRole(models.TextChoices):
        DIRECTOR = 'DIRECTOR', 'Diretor(a)'
        COORDINATOR = 'COORDINATOR', 'Coordenador(a) Pedagógico(a)'
        SECRETARY = 'SECRETARY', 'Secretaria Escolar'
        TEACHER_REP = 'TEACHER_REP', 'Representante Docente'

    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='members', verbose_name='Escola')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='school_memberships',
        verbose_name='Usuário'
    )
    role = models.CharField(
        max_length=20,
        choices=MemberRole.choices,
        default=MemberRole.DIRECTOR,
        verbose_name='Cargo na Escola'
    )
    is_primary_contact = models.BooleanField(default=False, verbose_name='Contato Principal')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Vinculado em')

    class Meta:
        verbose_name = 'Membro da Gestão Escolar'
        verbose_name_plural = 'Membros da Gestão Escolar'
        unique_together = ('school', 'user')

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.get_role_display()} ({self.school.name})"


class Campaign(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='campaigns', verbose_name='Escola')
    title = models.CharField(max_length=120, verbose_name='Título da Campanha (ex: 2026.1)')
    description = models.TextField(blank=True, verbose_name='Descrição / Orientações')
    start_date = models.DateField(verbose_name='Data de Início')
    end_date = models.DateField(verbose_name='Data de Encerramento')
    is_active = models.BooleanField(default=True, verbose_name='Campanha Ativa')
    min_quorum = models.PositiveIntegerField(
        default=10,
        verbose_name='Quórum Específico da Campanha'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criada em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizada em')

    class Meta:
        verbose_name = 'Campanha de Avaliação'
        verbose_name_plural = 'Campanhas de Avaliação'
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.school.name} - {self.title}"
