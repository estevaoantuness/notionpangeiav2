"""
Cliente Evolution API - MINIMALISTA
Apenas envia mensagens, sem complexidade.
"""
import requests
import logging
from config.settings import settings

logger = logging.getLogger(__name__)


class WhatsAppClient:
    """Cliente simples para Evolution API."""

    def __init__(self):
        self.api_url = settings.EVOLUTION_API_URL
        self.api_key = settings.EVOLUTION_API_KEY
        self.instance = settings.EVOLUTION_INSTANCE_NAME

    def send_message(self, phone: str, text: str) -> bool:
        """
        Envia mensagem de texto.

        Args:
            phone: Número no formato 5511999999999
            text: Texto da mensagem

        Returns:
            True se enviou com sucesso
        """
        try:
            # Remove caracteres especiais
            phone = phone.replace('+', '').replace('-', '').replace(' ', '')

            # Endpoint Evolution API
            url = f"{self.api_url}/message/sendText/{self.instance}"

            headers = {
                "Content-Type": "application/json",
                "apikey": self.api_key
            }

            payload = {
                "number": phone,
                "text": text
            }

            response = requests.post(url, json=payload, headers=headers, timeout=30)

            if response.status_code == 201:
                logger.info(f"Mensagem enviada para {phone}")
                return True
            else:
                logger.error(f"Erro ao enviar mensagem: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            logger.error(f"Exceção ao enviar mensagem: {e}")
            return False


# Instância global
whatsapp_client = WhatsAppClient()
