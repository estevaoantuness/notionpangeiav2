"""
Configurações centralizadas do Notion Pangeia V2.
"""
import os
import logging
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Configurações gerais do sistema."""

    # Notion
    NOTION_TOKEN: str = os.getenv("NOTION_TOKEN", "")
    NOTION_TASKS_DB_ID: str = os.getenv("NOTION_TASKS_DB_ID", "")

    # Evolution API
    EVOLUTION_API_URL: str = os.getenv("EVOLUTION_API_URL", "")
    EVOLUTION_API_KEY: str = os.getenv("EVOLUTION_API_KEY", "")
    EVOLUTION_INSTANCE_NAME: str = os.getenv("EVOLUTION_INSTANCE_NAME", "pangeiabot")

    # OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GPT_MODEL: str = os.getenv("GPT_MODEL", "gpt-4o-mini")
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.7"))

    # Flask
    FLASK_SECRET_KEY: str = os.getenv("FLASK_SECRET_KEY", "dev-secret-key")
    PORT: int = int(os.getenv("PORT", "5000"))
    WEBHOOK_PATH: str = os.getenv("WEBHOOK_PATH", "/webhook/whatsapp")

    # Scheduler
    TIMEZONE: str = os.getenv("TIMEZONE", "America/Sao_Paulo")
    MORNING_CHECKIN: str = os.getenv("MORNING_CHECKIN", "09:00")
    AFTERNOON_CHECKIN_1: str = os.getenv("AFTERNOON_CHECKIN_1", "13:30")
    AFTERNOON_CHECKIN_2: str = os.getenv("AFTERNOON_CHECKIN_2", "15:30")
    EVENING_CHECKIN: str = os.getenv("EVENING_CHECKIN", "18:00")

    # Features
    ENABLE_SCHEDULER: bool = os.getenv("ENABLE_SCHEDULER", "true").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "production")
    MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "3"))

    @classmethod
    def validate(cls) -> tuple[bool, list[str]]:
        """Valida configurações obrigatórias."""
        errors = []

        if not cls.NOTION_TOKEN:
            errors.append("NOTION_TOKEN não configurado")
        if not cls.NOTION_TASKS_DB_ID:
            errors.append("NOTION_TASKS_DB_ID não configurado")
        if not cls.EVOLUTION_API_URL:
            errors.append("EVOLUTION_API_URL não configurado")
        if not cls.EVOLUTION_API_KEY:
            errors.append("EVOLUTION_API_KEY não configurado")

        return len(errors) == 0, errors

    @classmethod
    def setup_logging(cls):
        """Configura logging."""
        log_level = getattr(logging, cls.LOG_LEVEL.upper(), logging.INFO)

        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler()
            ]
        )

        logging.getLogger('urllib3').setLevel(logging.WARNING)
        logging.getLogger('requests').setLevel(logging.WARNING)


settings = Settings()
settings.setup_logging()


def get_settings() -> Settings:
    """Retorna instância de configurações."""
    return settings
