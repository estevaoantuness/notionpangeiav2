# 🚀 Notion Pangeia V2

**Bot WhatsApp de Produtividade - Gestão de Tarefas via Notion com IA**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Evolution API](https://img.shields.io/badge/WhatsApp-Evolution%20API%20v2-25D366)](https://github.com/EvolutionAPI/evolution-api)
[![Notion API](https://img.shields.io/badge/Notion-API%202.x-000000)](https://developers.notion.com/)
[![Railway](https://img.shields.io/badge/Deploy-Railway-blueviolet)](https://railway.app)

---

## 📊 Status

**Versão:** 2.0
**Status:** 🚧 Em Desenvolvimento
**Deploy:** Railway

---

## 🎯 Funcionalidades

### ✅ Gestão de Tarefas (Core)
- Listar tarefas pendentes do Notion
- Marcar tarefas como concluídas
- Atualizar status para "em andamento"
- Acompanhar progresso diário (%)
- Ver estatísticas do dia

### ✅ Check-ins Automáticos
- **09:00** - Bom dia + lista de tarefas
- **13:30** - Check-in: como estão as tasks?
- **15:30** - Status da tarde
- **18:00** - Fechamento do dia

### ✅ Comandos Disponíveis
| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| `minhas tarefas` | Lista tasks do Notion | `minhas tarefas` |
| `feito N` | Marca task como concluída | `feito 3` |
| `andamento N` | Marca task em progresso | `andamento 2` |
| `progresso` | Mostra % do dia | `progresso` |
| `ajuda` | Lista comandos | `ajuda` |

---

## 🏗️ Stack Tecnológica

- **WhatsApp:** Evolution API v2 (Baileys) - instância "pangeiabot"
- **IA/NLP:** OpenAI GPT-4o-mini
- **Database:** Notion API
- **Voz:** Groq API (TTS/Transcrição)
- **Backend:** Flask + Gunicorn
- **Deploy:** Railway
- **Scheduler:** APScheduler

---

## 🚀 Deploy Railway

### Pré-requisitos
1. Conta Railway
2. Evolution API rodando no Railway
3. Credenciais Notion API
4. Chave OpenAI API

### Passo a Passo

#### 1. Fork/Clone este repositório

#### 2. Criar projeto no Railway
- New Project → Deploy from GitHub
- Selecionar repositório `notionpangeiav2`

#### 3. Configurar variáveis de ambiente
Adicionar no Railway Dashboard:

```bash
# Notion
NOTION_TOKEN=secret_xxxxx
NOTION_TASKS_DB_ID=xxxxx

# Evolution API
EVOLUTION_API_URL=https://[seu-evolution].up.railway.app
EVOLUTION_API_KEY=xxxxx
EVOLUTION_INSTANCE_NAME=pangeiabot

# OpenAI
OPENAI_API_KEY=sk-proj-xxxxx
GPT_MODEL=gpt-4o-mini
TEMPERATURE=0.7

# Groq
GROQ_API_KEY=gsk_xxxxx

# Flask
FLASK_SECRET_KEY=random-key
PORT=5000
WEBHOOK_PATH=/webhook/whatsapp

# Scheduler
TIMEZONE=America/Sao_Paulo
MORNING_CHECKIN=09:00
AFTERNOON_CHECKIN_1=13:30
AFTERNOON_CHECKIN_2=15:30
EVENING_CHECKIN=18:00

# Features
ENABLE_SCHEDULER=true
LOG_LEVEL=INFO
ENVIRONMENT=production
```

#### 4. Deploy automático
Railway faz build e deploy automaticamente (~3-5 min)

#### 5. Verificar deploy
```bash
curl https://[seu-bot].up.railway.app/health
```

---

## 📱 Como Usar

### Exemplo de Conversa

```
📱 Você: "oi"
🤖 Bot: "Olá! 👋 Como posso ajudar?
• minhas tarefas
• progresso
• ajuda"

📱 Você: "minhas tarefas"
🤖 Bot: "📋 Suas tarefas de hoje:

1. [🔵 Fazer] Implementar login OAuth
2. [🟢 Andamento] Revisar PRs pendentes
3. [🔴 Bloqueada] Deploy em produção

Progresso: 0/3 concluídas (0%)"

📱 Você: "andamento 1"
🤖 Bot: "🔄 Boa! Tarefa 1 está rodando.

'Implementar login OAuth'

Quando terminar: 'feito 1'"

📱 Você: "feito 1"
🤖 Bot: "✅ Tarefa 1 marcada como concluída!

'Implementar login OAuth' ✓

Progresso: 33% 🚀"
```

---

## 📁 Estrutura do Projeto

```
notionpangeiav2/
├── src/
│   ├── whatsapp/          # Evolution API client
│   ├── notion/            # Notion API integration
│   ├── commands/          # Command parser + processor
│   ├── messaging/         # Message humanization
│   ├── scheduler/         # Check-ins automáticos
│   └── webhook/           # Flask webhook handler
├── config/
│   ├── settings.py        # Configurações centralizadas
│   ├── colaboradores.py   # Lista de usuários
│   └── replies.yaml       # Mensagens humanizadas
├── docs/                  # Documentação
├── tests/                 # Testes
├── app.py                 # Entry point
├── requirements.txt
├── Procfile
├── railway.json
└── README.md
```

---

## 🔧 Desenvolvimento Local

### Setup
```bash
# Clone
git clone https://github.com/estevaoantuness/notionpangeiav2.git
cd notionpangeiav2

# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate   # Windows

# Instalar dependências
pip install -r requirements.txt

# Configurar .env
cp .env.example .env
# Editar .env com suas credenciais

# Rodar servidor
python app.py
```

### Testar
```bash
# Health check
curl http://localhost:5000/health

# Webhook test (simular mensagem)
curl -X POST http://localhost:5000/webhook/whatsapp \
  -H "Content-Type: application/json" \
  -d '{
    "event": "messages.upsert",
    "instance": "pangeiabot",
    "data": {
      "key": {
        "remoteJid": "5511999999999@s.whatsapp.net",
        "fromMe": false
      },
      "message": {
        "conversation": "minhas tarefas"
      },
      "pushName": "Teste"
    }
  }'
```

---

## 📊 Métricas

- **Comandos:** 5 comandos core
- **Check-ins:** 4 automáticos/dia
- **Uptime:** 99%+ (Railway)
- **Response Time:** <500ms

---

## 📞 Suporte

- **Issues:** https://github.com/estevaoantuness/notionpangeiav2/issues
- **Email:** estevao@pangeia.com.br

---

## 📝 Changelog

### v2.0.0 (2025-10-23)
- ✨ Reescrita completa do zero
- ✨ Evolution API v2 (Baileys)
- ✨ Sistema de comandos simplificado
- ✨ Deploy Railway
- ✨ Instância "pangeiabot"

---

**Status:** 🚧 Em Desenvolvimento
**Última Atualização:** 23/10/2025
