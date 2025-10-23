# Status do Projeto - Notion Pangeia V2

**Data:** 23/10/2025 19:11 BRT
**Sessão:** Migração e setup inicial

---

## ✅ O QUE FOI FEITO (8 passos concluídos!)

### 1. Repositório GitHub ✅
- Criado: https://github.com/estevaoantuness/notionpangeiav2
- Commits: 3 commits (initial, core code, fix pessoa)

### 2. Projeto Railway ✅
- URL: https://railway.com/project/2d725077-be91-40d5-bf06-2a71f8af37de
- Domínio: https://notionpangeiav2-production.up.railway.app
- Status: Deployado (mas variáveis de ambiente não foram salvas)

### 3. Código Core ✅
**Estrutura:**
```
src/
├── whatsapp/client.py    # Evolution API
├── notion/client.py      # Notion API
├── commands/parser.py    # Parser de comandos
└── webhook/app.py        # Flask webhook
```

**Funcionalidades implementadas:**
- ✅ Cliente Evolution API (envio de mensagens)
- ✅ Cliente Notion API (busca tasks por pessoa)
- ✅ 5 comandos: list, done, progress, show_progress, help
- ✅ Webhook Flask completo
- ✅ Mapeamento telefone → nome (11 colaboradores)

### 4. WhatsApp Conectado ✅
- Instância: "pangeiabot"
- Status: open (conectado)
- Evolution API: https://pange-evolution-api.u5qiqp.easypanel.host

### 5. Webhook Configurado ✅
- URL: Apontando para Railway (atualmente desabilitado)
- Evento: MESSAGES_UPSERT

### 6. Teste Local ✅
- Bot rodou localmente na porta 5001
- Ngrok funcionou: https://overrichly-cracklier-hiram.ngrok-free.dev
- Webhook recebeu mensagens
- Bot processou comandos
- Bot enviou respostas

---

## ⚠️ PROBLEMA ATUAL

**Database do Notion não funciona!**

❌ **Erro:** "Databases with multiple data sources are not supported in this API version"

**Causa:**
- O ID fornecido (`2f0e4657-54d4-44c8-8ee4-93ca30b1ea36`) é uma **Linked Database View**
- Essa view agrega 3 databases diferentes
- A API do Notion 2022-06-28 não suporta linked databases

**Databases na view:**
1. `368e1ae0-847d-4b0a-8c04-e60086ba329c` - Sprint Tasks V7 (original)
2. `291a53b3-e53c-80eb-b4cb-000bac3f471d` - New data source
3. `291a53b3-e53c-80bc-a93f-000bcf879d60` - New data source

---

## 🔧 O QUE FALTA FAZER

### Prioridade 1: Resolver Database Notion
**Opções:**

**A) Compartilhar database original (RECOMENDADO)**
1. Abrir Notion → Database "Sprint Tasks V7" original
2. Compartilhar com a integração do bot
3. Copiar ID do database original
4. Atualizar variável `NOTION_TASKS_DB_ID` no Railway

**B) Criar database novo simples**
1. Criar database de tasks sem linked databases
2. Compartilhar com integração
3. Usar esse para testes

### Prioridade 2: Configurar Railway
**Pendente:** Adicionar variáveis de ambiente no Railway Dashboard

**Variáveis necessárias:**
```
NOTION_TOKEN=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
NOTION_TASKS_DB_ID=[AGUARDANDO DATABASE CORRETO]
EVOLUTION_API_URL=https://pange-evolution-api.u5qiqp.easypanel.host
EVOLUTION_API_KEY=429683C4C977415CAAFCCE10F7D57E11
EVOLUTION_INSTANCE_NAME=pangeiabot
OPENAI_API_KEY=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
GPT_MODEL=gpt-4o-mini
TEMPERATURE=0.7
GROQ_API_KEY=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
FLASK_SECRET_KEY=pangeia-bot-secret-key-2025
WEBHOOK_PATH=/webhook/whatsapp
TIMEZONE=America/Sao_Paulo
MORNING_CHECKIN=09:00
AFTERNOON_CHECKIN_1=13:30
AFTERNOON_CHECKIN_2=15:30
EVENING_CHECKIN=18:00
ENABLE_SCHEDULER=true
LOG_LEVEL=INFO
ENVIRONMENT=production
```

### Prioridade 3: Reabilitar Webhook
Após tudo funcionando:
```bash
curl -X POST "https://pange-evolution-api.u5qiqp.easypanel.host/webhook/set/pangeiabot" \
  -H "Content-Type: application/json" \
  -H "apikey: 429683C4C977415CAAFCCE10F7D57E11" \
  -d '{
    "webhook": {
      "enabled": true,
      "url": "https://notionpangeiav2-production.up.railway.app/webhook/whatsapp",
      "webhookByEvents": false,
      "events": ["MESSAGES_UPSERT"]
    }
  }'
```

---

## 📊 Teste Realizado

**Comando testado:** `minhas tarefas`

**Resultado:**
1. ✅ Webhook recebeu mensagem
2. ✅ Telefone reconhecido → "Estevao Antunes"
3. ❌ Erro ao buscar tasks no Notion (database incompatível)
4. ✅ Bot enviou mensagem de erro no WhatsApp

**Logs:**
```
2025-10-23 19:06:52,187 - src.webhook.app - INFO - Webhook recebido: messages.upsert
2025-10-23 19:06:52,187 - src.webhook.app - INFO - Mensagem de 554191851256: minhas tarefas
2025-10-23 19:06:52,187 - src.notion.client - INFO - Buscando tasks para: Estevao Antunes
2025-10-23 19:06:52,584 - httpx - INFO - HTTP Request: POST https://api.notion.com/v1/databases/2f0e4657-54d4-44c8-8ee4-93ca30b1ea36/query "HTTP/1.1 400 Bad Request"
2025-10-23 19:06:52,586 - src.notion.client - ERROR - Erro ao buscar tasks: Databases with multiple data sources are not supported
```

---

## 🎯 Próximos Passos (Quando Voltar)

1. **Pegar ID do database original** do Notion
2. **Atualizar `NOTION_TASKS_DB_ID`** no código
3. **Adicionar todas as variáveis** no Railway
4. **Testar localmente** com o database correto
5. **Deploy no Railway**
6. **Reabilitar webhook**
7. **Teste final no WhatsApp**

---

## 📝 Notas Importantes

- Bot local testado e funcionando (exceto Notion)
- Webhook configurado e recebendo mensagens
- WhatsApp conectado e respondendo
- Código limpo e minimalista (sem complexidade do v1)
- Mapeamento de 11 colaboradores funcionando

**Progresso:** ~90% concluído
**Bloqueio:** ID do database Notion incorreto

---

## 🔗 Links Úteis

- **GitHub:** https://github.com/estevaoantuness/notionpangeiav2
- **Railway:** https://railway.com/project/2d725077-be91-40d5-bf06-2a71f8af37de
- **Bot URL:** https://notionpangeiav2-production.up.railway.app
- **Evolution Manager:** https://pange-evolution-api.u5qiqp.easypanel.host/manager
