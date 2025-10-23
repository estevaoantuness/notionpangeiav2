"""
Flask webhook handler - COMPLETO E MINIMALISTA
"""
from flask import Flask, request, jsonify
import logging
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from config.settings import settings
from src.whatsapp.client import whatsapp_client
from src.notion.client import notion_client
from src.commands.parser import parse_command

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = settings.FLASK_SECRET_KEY

# Cache de tasks por usuário (simples dict em memória)
user_tasks_cache = {}


@app.route('/')
def index():
    """Root endpoint."""
    return jsonify({
        "bot": "Notion Pangeia V2",
        "version": "2.0.0",
        "status": "online"
    })


@app.route('/health')
def health():
    """Health check para Railway."""
    return jsonify({"status": "healthy"}), 200


@app.route('/webhook/whatsapp', methods=['POST'])
def webhook_whatsapp():
    """
    Webhook Evolution API.
    """
    try:
        data = request.json
        logger.info(f"Webhook recebido: {data.get('event')}")

        # Apenas processar mensagens
        if data.get('event') != 'messages.upsert':
            return jsonify({"status": "ignored"}), 200

        message_data = data.get('data', {})
        key = message_data.get('key', {})
        message = message_data.get('message', {})

        # Ignorar mensagens do próprio bot
        if key.get('fromMe'):
            return jsonify({"status": "ignored", "reason": "fromMe"}), 200

        # Extrair telefone e texto
        phone = key.get('remoteJid', '').split('@')[0]
        text = (
            message.get('conversation') or
            message.get('extendedTextMessage', {}).get('text') or
            ''
        ).strip()

        if not text:
            return jsonify({"status": "ignored", "reason": "no_text"}), 200

        logger.info(f"Mensagem de {phone}: {text}")

        # Parsear comando
        command_type, command_data = parse_command(text)

        if not command_type:
            # Comando não reconhecido
            response = (
                "🤔 Não entendi esse comando.\n\n"
                "**Comandos disponíveis:**\n"
                "• minhas tarefas\n"
                "• feito N\n"
                "• andamento N\n"
                "• progresso\n"
                "• ajuda"
            )
            whatsapp_client.send_message(phone, response)
            return jsonify({"status": "unknown_command"}), 200

        # Processar comando
        response = process_command(phone, command_type, command_data)

        # Enviar resposta
        whatsapp_client.send_message(phone, response)

        return jsonify({"status": "processed"}), 200

    except Exception as e:
        logger.error(f"Erro no webhook: {e}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500


def process_command(phone: str, command_type: str, data: dict) -> str:
    """
    Processa comando e retorna resposta.

    Args:
        phone: Telefone do usuário
        command_type: Tipo do comando
        data: Dados do comando

    Returns:
        Texto da resposta
    """
    try:
        if command_type == "list_tasks":
            return handle_list_tasks(phone)

        elif command_type == "mark_done":
            return handle_mark_done(phone, data["task_number"])

        elif command_type == "mark_progress":
            return handle_mark_progress(phone, data["task_number"])

        elif command_type == "show_progress":
            return handle_show_progress(phone)

        elif command_type == "help":
            return handle_help()

        else:
            return "Comando não implementado."

    except Exception as e:
        logger.error(f"Erro ao processar comando: {e}", exc_info=True)
        return "⚠️ Erro ao processar comando. Tente novamente."


def handle_list_tasks(phone: str) -> str:
    """Lista tarefas do usuário."""
    tasks = notion_client.get_user_tasks(phone)

    if not tasks:
        return "🎉 Você não tem tarefas pendentes!"

    # Salvar no cache
    user_tasks_cache[phone] = tasks

    # Formatar resposta
    response = "📋 **Suas tarefas:**\n\n"
    for i, task in enumerate(tasks, 1):
        status_emoji = "🔵" if task["status"] == "To Do" else "🟢"
        response += f"{i}. {status_emoji} {task['title']}\n"

    response += "\n💬 Para atualizar:\n• feito N\n• andamento N"

    return response


def handle_mark_done(phone: str, task_number: int) -> str:
    """Marca tarefa como concluída."""
    tasks = user_tasks_cache.get(phone, [])

    if not tasks:
        return "⚠️ Você precisa listar as tarefas primeiro.\nDigite: minhas tarefas"

    if task_number < 1 or task_number > len(tasks):
        return f"⚠️ Tarefa {task_number} não existe.\nVocê tem {len(tasks)} tarefas."

    task = tasks[task_number - 1]

    # Atualizar no Notion
    success = notion_client.update_task_status(task["id"], "Done")

    if success:
        return f"✅ Tarefa {task_number} concluída!\n\n\"{task['title']}\" ✓"
    else:
        return "⚠️ Erro ao atualizar tarefa. Tente novamente."


def handle_mark_progress(phone: str, task_number: int) -> str:
    """Marca tarefa como em andamento."""
    tasks = user_tasks_cache.get(phone, [])

    if not tasks:
        return "⚠️ Você precisa listar as tarefas primeiro.\nDigite: minhas tarefas"

    if task_number < 1 or task_number > len(tasks):
        return f"⚠️ Tarefa {task_number} não existe.\nVocê tem {len(tasks)} tarefas."

    task = tasks[task_number - 1]

    # Atualizar no Notion
    success = notion_client.update_task_status(task["id"], "In Progress")

    if success:
        return f"🔄 Tarefa {task_number} em andamento!\n\n\"{task['title']}\"\n\nQuando terminar: feito {task_number}"
    else:
        return "⚠️ Erro ao atualizar tarefa. Tente novamente."


def handle_show_progress(phone: str) -> str:
    """Mostra progresso do dia."""
    tasks = user_tasks_cache.get(phone, [])

    if not tasks:
        return "⚠️ Liste suas tarefas primeiro.\nDigite: minhas tarefas"

    # Por enquanto só mostra quantidade (pode melhorar depois)
    return f"📊 Você tem {len(tasks)} tarefas pendentes.\n\nDigite 'minhas tarefas' para ver a lista."


def handle_help() -> str:
    """Mostra ajuda."""
    return (
        "💬 **Comandos disponíveis:**\n\n"
        "📋 **Ver tarefas**\n"
        "• minhas tarefas\n\n"
        "✅ **Atualizar**\n"
        "• feito 2\n"
        "• andamento 3\n\n"
        "📊 **Progresso**\n"
        "• progresso\n\n"
        "❓ **Ajuda**\n"
        "• ajuda"
    )


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
