"""
Parser de comandos - MINIMALISTA
Apenas regex simples, sem NLP complexo.
"""
import re
import logging

logger = logging.getLogger(__name__)


def parse_command(text: str) -> tuple[str, dict]:
    """
    Parse comando do usuário.

    Args:
        text: Mensagem do usuário

    Returns:
        (command_type, data) ou (None, {})
    """
    text = text.strip().lower()

    # Listar tarefas
    if re.match(r"^(minhas?\s+tarefas?|lista|tasks?)$", text):
        return "list_tasks", {}

    # Marcar como feito
    match = re.match(r"^(feito|conclu[ií]|terminei?)\s+(\d+)$", text)
    if match:
        return "mark_done", {"task_number": int(match.group(2))}

    # Marcar em andamento
    match = re.match(r"^(andamento|fazendo|começando)\s+(\d+)$", text)
    if match:
        return "mark_progress", {"task_number": int(match.group(2))}

    # Ver progresso
    if re.match(r"^(progresso|status)$", text):
        return "show_progress", {}

    # Ajuda
    if re.match(r"^(ajuda|help|\?)$", text):
        return "help", {}

    # Não reconhecido
    return None, {}
