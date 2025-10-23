"""
LLM Agent para processar comandos com linguagem natural.
Usa GPT-4o-mini para entender intenção do usuário.
"""
import json
import logging
from openai import OpenAI
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from config.settings import settings
from src.llm.prompts import get_system_prompt

logger = logging.getLogger(__name__)


class LLMAgent:
    """Agent que usa LLM para entender linguagem natural."""

    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.GPT_MODEL
        self.temperature = settings.TEMPERATURE

    def parse_natural_language(self, text: str, context: dict) -> dict:
        """
        Usa LLM para entender comando em linguagem natural.

        Args:
            text: Mensagem do usuário
            context: {
                "user_name": "João",
                "tasks": [...],
                "task_count": 3
            }

        Returns:
            {
                "command": "list_tasks" | "mark_done" | etc,
                "params": {"task_number": 1},
                "confidence": 0.95,
                "reasoning": "explicação"
            }
        """
        try:
            # Montar prompt do sistema
            system_prompt = get_system_prompt(context)

            # Chamar LLM
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": text}
                ],
                temperature=self.temperature,
                response_format={"type": "json_object"}
            )

            # Parsear resposta
            result_text = response.choices[0].message.content
            result = json.loads(result_text)

            logger.info(f"LLM parsed '{text}' → {result['command']} (confidence: {result['confidence']})")

            return {
                "command": result.get("command"),
                "params": result.get("params", {}),
                "confidence": float(result.get("confidence", 0)),
                "reasoning": result.get("reasoning", "")
            }

        except Exception as e:
            logger.error(f"Erro ao processar LLM: {e}", exc_info=True)
            return {
                "command": None,
                "params": {},
                "confidence": 0.0,
                "reasoning": f"Erro: {e}"
            }

    def format_response(self, command_result: dict, context: dict) -> str:
        """
        Usa LLM para formatar resposta de forma natural e humanizada.

        Args:
            command_result: Resultado do comando executado
            context: Contexto do usuário

        Returns:
            Resposta humanizada e contextualizada
        """
        try:
            prompt = f"""
Você é um assistente de produtividade. Reformule a resposta abaixo de forma natural e amigável.

**Contexto:**
Usuário: {context.get('user_name', 'Usuário')}
Comando: {command_result.get('command')}

**Resposta original:**
{command_result.get('result')}

**Regras:**
- Seja breve e direto
- Mantenha emojis se houver
- Tom profissional mas amigável
- Máximo 3 linhas

Responda apenas com o texto reformulado (sem aspas ou formatação extra).
"""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=200
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            logger.error(f"Erro ao formatar resposta: {e}")
            # Fallback: retorna resposta original
            return command_result.get('result', '')


# Instância global
llm_agent = LLMAgent()
