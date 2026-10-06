# 🎓 Voz Escolar

> **"Sua voz transforma a escola"**  
> *Plataforma web de avaliação, ouvidoria e participação estudantil com governança, anonimato protegido e planos de melhoria acompanháveis.*

---

## 📌 Sobre o Projeto

O **Voz Escolar** é uma plataforma desenvolvida para proporcionar um canal seguro, transparente e estruturado de escuta ativa para a comunidade escolar. 

A proposta permite que estudantes avaliem eixos fundamentais da instituição através de **códigos de participação anônimos**, protegendo os alunos contra retaliações ao mesmo tempo em que oferece às escolas dados precisos para criar **planos de ação concretos**.

---

## 🌟 Principais Pilares do Produto

### 1. 🛡️ Anonimato Protegido e Conformidade com a LGPD
* **Desacoplamento de Dados:** As informações de matrícula e elegibilidade são separadas do banco de respostas.
* **Códigos Únicos:** Os estudantes participam por meio de códigos alfanuméricos aleatórios de uso único por campanha.
* **Quórum Mínimo:** Resultados públicos só são divulgados após atingir um número mínimo de respostas por categoria (evitando inferências sobre grupos pequenos).

### 2. 📊 Os 6 Eixos de Avaliação
1. 📚 **Ensino:** Didática dos professores, apoio pedagógico, clareza e material de estudo.
2. 🏢 **Infraestrutura:** Salas de aula, climatização, laboratórios, biblioteca e quadras esportivas.
3. 🧼 **Higiene:** Limpeza dos banheiros, conservação predial e saneamento.
4. 🍎 **Alimentação:** Qualidade da merenda escolar, cantina e nutrição.
5. 🤝 **Convivência:** Clima escolar, acolhimento, inclusão e combate ativo ao bullying.
6. 💡 **Sugestões:** Ideias e projetos de iniciativa dos próprios estudantes.

### 3. ⚖️ Moderação Ética e Semiautomática
* Triagem para retenção de ofensas gratuitas, termos discriminatórios ou vazamento de dados pessoais.
* Preservação integral do direito à crítica legítima e construtiva.
* Emissão de **Protocolo Aleatório** para o aluno acompanhar o status da sua avaliação de forma confidencial.

### 4. 🎯 Ciclo Fechado de Melhorias
* O painel da gestão escolar permite que a direção responda publicamente a comentários aprovados e cadastre **Planos de Melhoria** com prazos, responsáveis e status de execução.

---

## 👥 Perfis de Acesso

| Perfil | Descrição | Principais Permissões |
| :--- | :--- | :--- |
| **Visitante Público** | Comunidade externa e responsáveis | Consulta médias, indicadores públicos, comentários moderados e planos de ação. |
| **Estudante Elegível** | Aluno matriculado | Valida código anônimo, avalia os 6 pilares e acompanha seu envio via protocolo. |
| **Responsável Escolar** | Equipe de gestão e direção | Analisa relatórios da unidade, responde feedbacks e publica planos de ação. |
| **Moderador** | Equipe de moderação ética | Realiza a triagem de mensagens sinalizadas e analisa denúncias. |
| **Administrador Geral** | Gestão da plataforma | Homologa escolas, audita ações administrativas e gerencia convites institucionais. |

---

## 🛠️ Tecnologias Utilizadas

* **Backend:** [Python](https://www.python.org/) & [Django](https://www.djangoproject.com/)
* **Frontend:** HTML5 Semântico, CSS3 Moderno (Design System customizado) e JavaScript Vanilla
* **Banco de Dados:** SQLite (Desenvolvimento) / PostgreSQL (Produção)
* **Tipografia:** Google Fonts (*Plus Jakarta Sans*)

---

## 📁 Estrutura de Pastas

```text
voz-escolar/
├── backend/                  # Servidor Django
│   ├── config/               # Configurações centrais do Django (settings, urls, wsgi)
│   ├── db.sqlite3            # Banco de dados local
│   ├── manage.py             # CLI de gerenciamento do Django
│   └── .venv/                # Ambiente virtual Python
│
├── frontend/                 # Interface Web
│   ├── css/
│   │   └── style.css         # Design System, variáveis e responsividade
│   ├── js/
│   │   └── main.js           # Lógica do modal de código, busca e interatividade
│   ├── pages/
│   │   ├── avaliar.html      # Fluxo de avaliação dos 6 pilares e geração de protocolo
│   │   ├── escola.html       # Página pública da instituição com gráficos e planos
│   │   ├── protocolo.html    # Consulta de status ético da avaliação
│   │   └── painel.html       # Dashboard da gestão escolar e emissão de códigos
│   └── index.html            # Landing page principal e busca pública
│
├── .gitignore
└── README.md
```

---

## 🚀 Como Executar o Projeto Localmente

### 1. Clonar o Repositório
```bash
git clone https://github.com/kingdragon2008/voz-escolar.git
cd voz-escolar
```

### 2. Executar o Frontend
Basta abrir o arquivo `frontend/index.html` diretamente em seu navegador (Google Chrome, Edge, Firefox) ou utilizar uma extensão de servidor local como o *Live Server* no VS Code.

### 3. Executar o Backend (Django)
```bash
# Acessar a pasta do backend
cd backend

# Ativar o ambiente virtual (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Executar as migrações do banco de dados
python manage.py migrate

# Iniciar o servidor de desenvolvimento
python manage.py runserver
```
O servidor estará disponível em `http://127.0.0.1:8000/`.

---

## 📄 Licença e Uso

Este projeto está em fase ativa de ideação e desenvolvimento sob a **Versão 0.2** do Documento de Ideação. Todos os direitos reservados.
