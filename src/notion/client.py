"""
Cliente Notion API - MINIMALISTA
Busca tasks por NOME DA PESSOA (não por telefone).
"""
from notion_client import Client
import logging
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from config.settings import settings
from config.colaboradores import get_name_by_phone

logger = logging.getLogger(__name__)


class NotionClient:
    """Cliente simples para Notion API."""

    def __init__(self):
        self.client = Client(auth=settings.NOTION_TOKEN)
        self.tasks_db_id = settings.NOTION_TASKS_DB_ID

    def get_user_tasks(self, phone: str) -> list[dict]:
        """
        Busca tasks pendentes do usuário por telefone.
        Converte telefone → nome → busca tasks dessa pessoa.

        Args:
            phone: Telefone do usuário

        Returns:
            Lista de tasks: [{"id": "", "title": "", "status": ""}, ...]
        """
        try:
            # Converter telefone para nome
            person_name = get_name_by_phone(phone)

            if not person_name:
                logger.warning(f"Telefone {phone} não encontrado na lista de colaboradores")
                return []

            logger.info(f"Buscando tasks para: {person_name} (telefone: {phone})")

            # Tentar buscar tasks - vai tentar diferentes nomes de propriedade
            # Primeiro tenta buscar todas as tasks e filtrar depois
            response = self.client.databases.query(
                database_id=self.tasks_db_id
            )

            # Filtrar tasks manualmente
            tasks = []
            for page in response.get("results", []):
                # Verificar se a task pertence à pessoa
                person_prop = self._get_person(page)
                status = self._get_status(page)

                # Filtrar: mesma pessoa E não "Done"
                if person_prop and person_name.lower() in person_prop.lower() and status != "Done":
                    task = {
                        "id": page["id"],
                        "title": self._get_title(page),
                        "status": status
                    }
                    tasks.append(task)

            logger.info(f"Encontradas {len(tasks)} tasks para {person_name}")
            return tasks

        except Exception as e:
            logger.error(f"Erro ao buscar tasks: {e}", exc_info=True)
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

    def _get_person(self, page: dict) -> str:
        """
        Extrai nome da pessoa da página.
        Tenta diferentes propriedades comuns.
        """
        try:
            props = page["properties"]

            # Tentar diferentes nomes de propriedade
            for prop_name in ["Pessoa", "Assignee", "Owner", "Responsável", "Assigned To", "Nome"]:
                if prop_name in props:
                    prop = props[prop_name]

                    # Tipo: People
                    if prop.get("people"):
                        people = prop["people"]
                        if people:
                            return people[0].get("name", "")

                    # Tipo: Select
                    if prop.get("select"):
                        return prop["select"].get("name", "")

                    # Tipo: Text
                    if prop.get("rich_text"):
                        texts = prop["rich_text"]
                        if texts:
                            return texts[0].get("plain_text", "")

        except Exception as e:
            logger.debug(f"Erro ao extrair pessoa: {e}")

        return ""


# Instância global
notion_client = NotionClient()
