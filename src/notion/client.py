"""
Cliente Notion API - MINIMALISTA
Apenas busca tasks e atualiza status.
"""
from notion_client import Client
import logging
from config.settings import settings

logger = logging.getLogger(__name__)


class NotionClient:
    """Cliente simples para Notion API."""

    def __init__(self):
        self.client = Client(auth=settings.NOTION_TOKEN)
        self.tasks_db_id = settings.NOTION_TASKS_DB_ID

    def get_user_tasks(self, phone: str) -> list[dict]:
        """
        Busca tasks pendentes do usuário por telefone.

        Args:
            phone: Telefone do usuário

        Returns:
            Lista de tasks: [{"id": "", "title": "", "status": ""}, ...]
        """
        try:
            # Query Notion database
            response = self.client.databases.query(
                database_id=self.tasks_db_id,
                filter={
                    "and": [
                        {
                            "property": "Telefone",  # AJUSTE SE NECESSÁRIO
                            "phone_number": {
                                "equals": phone
                            }
                        },
                        {
                            "property": "Status",
                            "status": {
                                "does_not_equal": "Done"
                            }
                        }
                    ]
                }
            )

            tasks = []
            for page in response.get("results", []):
                task = {
                    "id": page["id"],
                    "title": self._get_title(page),
                    "status": self._get_status(page)
                }
                tasks.append(task)

            logger.info(f"Encontradas {len(tasks)} tasks para {phone}")
            return tasks

        except Exception as e:
            logger.error(f"Erro ao buscar tasks: {e}")
            return []

    def update_task_status(self, task_id: str, status: str) -> bool:
        """
        Atualiza status da task.

        Args:
            task_id: ID da página no Notion
            status: Novo status ("Done", "In Progress", etc)

        Returns:
            True se atualizou com sucesso
        """
        try:
            self.client.pages.update(
                page_id=task_id,
                properties={
                    "Status": {
                        "status": {
                            "name": status
                        }
                    }
                }
            )

            logger.info(f"Task {task_id} atualizada para {status}")
            return True

        except Exception as e:
            logger.error(f"Erro ao atualizar task: {e}")
            return False

    def _get_title(self, page: dict) -> str:
        """Extrai título da página."""
        try:
            title_prop = page["properties"].get("Name") or page["properties"].get("Task")
            if title_prop and title_prop.get("title"):
                return title_prop["title"][0]["plain_text"]
        except:
            pass
        return "Sem título"

    def _get_status(self, page: dict) -> str:
        """Extrai status da página."""
        try:
            status_prop = page["properties"].get("Status")
            if status_prop and status_prop.get("status"):
                return status_prop["status"]["name"]
        except:
            pass
        return "Unknown"


# Instância global
notion_client = NotionClient()
