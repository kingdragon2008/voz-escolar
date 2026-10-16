from datetime import date
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.accounts.models import User
from apps.schools.models import School, SchoolMember, Campaign
from apps.access_codes.models import CodeBatch, AccessCode
from apps.evaluations.models import Evaluation, EvaluationComment, SchoolReply
from apps.moderation.models import ModerationLog
from apps.actions.models import ActionPlan


class Command(BaseCommand):
    help = 'Popula o banco de dados com dados de demonstracao realistas do Voz Escolar.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("[*] Iniciando populacao de dados demo do Voz Escolar..."))

        # 1. Usuarios
        admin_user, _ = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@vozescolar.com.br',
                'first_name': 'Admin',
                'last_name': 'Geral',
                'role': User.Roles.ADMIN,
                'is_staff': True,
                'is_superuser': True,
                'is_verified': True,
            }
        )
        admin_user.set_password('admin123')
        admin_user.save()

        manager_user, _ = User.objects.get_or_create(
            username='diretoria',
            defaults={
                'email': 'diretoria@colegiomodelo.edu.br',
                'first_name': 'Helena',
                'last_name': 'Vasconcelos',
                'role': User.Roles.SCHOOL_MANAGER,
                'is_staff': True,
                'is_verified': True,
                'phone': '(11) 98765-4321',
            }
        )
        manager_user.set_password('diretoria123')
        manager_user.save()

        moderator_user, _ = User.objects.get_or_create(
            username='moderador',
            defaults={
                'email': 'moderacao@vozescolar.com.br',
                'first_name': 'Lucas',
                'last_name': 'Ferreira',
                'role': User.Roles.MODERATOR,
                'is_staff': True,
                'is_verified': True,
            }
        )
        moderator_user.set_password('moderador123')
        moderator_user.save()

        self.stdout.write(self.style.SUCCESS("[OK] Usuarios criados (admin, diretoria, moderador)."))

        # 2. Escolas
        escola_modelo, _ = School.objects.get_or_create(
            slug='colegio-estadual-modelo',
            defaults={
                'name': 'Colégio Estadual Modelo',
                'inep_code': '35012345',
                'city': 'São Paulo',
                'state': 'SP',
                'address': 'Av. Paulista, 1000 - Bela Vista',
                'school_type': School.SchoolType.PUBLIC_STATE,
                'is_verified': True,
                'min_quorum': 10,
                'about': 'Escola pública de ensino fundamental II e médio com foco em cidadania e inovação pedagógica.'
            }
        )

        escola_santos, _ = School.objects.get_or_create(
            slug='emef-santos-dumont',
            defaults={
                'name': 'EMEF Santos Dumont',
                'inep_code': '35098765',
                'city': 'Campinas',
                'state': 'SP',
                'address': 'Rua das Palmeiras, 350',
                'school_type': School.SchoolType.PUBLIC_MUNICIPAL,
                'is_verified': True,
                'min_quorum': 10,
            }
        )

        escola_darcy, _ = School.objects.get_or_create(
            slug='instituto-federal-darcy-ribeiro',
            defaults={
                'name': 'Instituto Federal Darcy Ribeiro',
                'inep_code': '33045678',
                'city': 'Rio de Janeiro',
                'state': 'RJ',
                'address': 'Rua Maracanã, 500',
                'school_type': School.SchoolType.PUBLIC_FEDERAL,
                'is_verified': True,
                'min_quorum': 15,
            }
        )

        # Vincular Gestor a Escola
        SchoolMember.objects.get_or_create(
            school=escola_modelo,
            user=manager_user,
            defaults={
                'role': SchoolMember.MemberRole.DIRECTOR,
                'is_primary_contact': True,
            }
        )

        self.stdout.write(self.style.SUCCESS("[OK] Escolas e membros cadastrados."))

        # 3. Campanhas
        campanha_2026, _ = Campaign.objects.get_or_create(
            school=escola_modelo,
            title='Campanha 2026.1',
            defaults={
                'description': 'Primeiro ciclo oficial de avaliação e escuta estudantil do ano letivo de 2026.',
                'start_date': date(2026, 2, 1),
                'end_date': date(2026, 12, 15),
                'is_active': True,
                'min_quorum': 10,
            }
        )

        # 4. Lotes e Codigos de Acesso Anonimos
        lote, _ = CodeBatch.objects.get_or_create(
            campaign=campanha_2026,
            target_group='3º Ano do Ensino Médio',
            defaults={
                'generated_by': manager_user,
                'quantity': 25,
            }
        )
        lote.generate_codes()

        # Garantir o codigo de teste padrao da interface
        AccessCode.objects.get_or_create(
            code='ESC-2026-X9K4',
            campaign=campanha_2026,
            defaults={
                'batch': lote,
                'is_used': False,
            }
        )

        self.stdout.write(self.style.SUCCESS("[OK] Campanha 2026.1 e Codigos de Acesso gerados."))

        # 5. Avaliacoes Discentes e Protocolos
        eval_1, _ = Evaluation.objects.get_or_create(
            protocol='PRT-2026-98X2F',
            defaults={
                'campaign': campanha_2026,
                'score_teaching': 4,
                'score_infrastructure': 2,
                'score_hygiene': 3,
                'score_food': 4,
                'score_coexistence': 5,
                'general_suggestions': 'Poderíamos criar um clube de robótica e debates no contraturno.',
            }
        )

        # Comentarios moderados
        com_infra, _ = EvaluationComment.objects.get_or_create(
            evaluation=eval_1,
            axis=EvaluationComment.Axis.INFRASTRUCTURE,
            defaults={
                'comment': 'As salas do 2º andar esquentam muito no período da tarde, alguns ventiladores estão com ruído forte.',
                'moderation_status': EvaluationComment.ModerationStatus.APPROVED,
                'moderated_at': timezone.now(),
            }
        )

        # Resposta da Direcao ao comentario
        SchoolReply.objects.get_or_create(
            comment=com_infra,
            defaults={
                'author': manager_user,
                'reply_text': 'Agradecemos o apontamento! Já incluímos no Plano de Ação a troca de ventiladores e a revisão da fiação elétrica para o próximo mês.',
            }
        )

        # Log de Moderacao
        ModerationLog.objects.get_or_create(
            comment=com_infra,
            action=ModerationLog.Action.AUTO_APPROVED,
            defaults={
                'reason': 'Linguagem respeitosa e crítica construtiva legítima.',
                'ai_confidence_score': 0.98,
            }
        )

        # Criar mais algumas avaliacoes para compor quorum
        sample_scores = [
            (5, 3, 4, 5, 4, "Ótimo acolhimento dos novos alunos."),
            (4, 2, 3, 3, 5, "Os professores de História e Física são excelentes."),
            (4, 3, 4, 4, 4, "A merenda melhorou bastante este ano."),
            (5, 4, 5, 4, 5, "Adoro os projetos culturais da escola."),
            (3, 2, 2, 3, 4, "Banheiros precisam de mais reposição de sabonete líquido."),
        ]

        for i, (t, inf, h, f, c, sug) in enumerate(sample_scores, start=2):
            Evaluation.objects.get_or_create(
                protocol=f'PRT-2026-DEMO{i:02d}',
                defaults={
                    'campaign': campanha_2026,
                    'score_teaching': t,
                    'score_infrastructure': inf,
                    'score_hygiene': h,
                    'score_food': f,
                    'score_coexistence': c,
                    'general_suggestions': sug,
                }
            )

        self.stdout.write(self.style.SUCCESS("[OK] Avaliacoes discentes e comentarios de exemplo registrados."))

        # 6. Planos de Melhoria (Ciclo Fechado)
        ActionPlan.objects.get_or_create(
            school=escola_modelo,
            title='Instalação de Novos Ventiladores e Reforma Elétrica',
            defaults={
                'campaign': campanha_2026,
                'axis': ActionPlan.Axis.INFRASTRUCTURE,
                'description': 'Com base nos feedbacks dos estudantes sobre a climatização das salas do 2º andar, foi autorizada a compra de 12 novos aparelhos e manutenção do quadro geral.',
                'responsible_department': 'Coordenação de Infraestrutura e Secretaria',
                'deadline': date(2026, 11, 15),
                'status': ActionPlan.Status.IN_PROGRESS,
                'progress_percentage': 60,
                'is_public': True,
            }
        )

        ActionPlan.objects.get_or_create(
            school=escola_modelo,
            title='Ampliação do Cardápio Nutricional e Frutas Frescas',
            defaults={
                'campaign': campanha_2026,
                'axis': ActionPlan.Axis.FOOD,
                'description': 'Inserção de novos tipos de frutas da estação e opções de lanches balanceados aprovados pela nutricionista da rede estadual.',
                'responsible_department': 'Nutrição e Equipe de Merenda',
                'deadline': date(2026, 9, 30),
                'status': ActionPlan.Status.COMPLETED,
                'progress_percentage': 100,
                'is_public': True,
            }
        )

        ActionPlan.objects.get_or_create(
            school=escola_modelo,
            title='Plantão Semanal de Dúvidas de Matemática e Redação',
            defaults={
                'campaign': campanha_2026,
                'axis': ActionPlan.Axis.TEACHING,
                'description': 'Criação de oficinas de reforço pedagógico às terças e quintas-feiras para auxílio no ENEM e vestibulares.',
                'responsible_department': 'Coordenação Pedagógica',
                'deadline': date(2026, 12, 10),
                'status': ActionPlan.Status.IN_PROGRESS,
                'progress_percentage': 40,
                'is_public': True,
            }
        )

        self.stdout.write(self.style.SUCCESS("[OK] Planos de Melhoria cadastrados com sucesso!"))
        self.stdout.write(self.style.SUCCESS("[SUCCESS] Base de dados populada com 100% de sucesso!"))
