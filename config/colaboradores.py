"""
Mapeamento telefone → nome da pessoa no Notion.
MINIMALISTA: apenas o essencial.
"""

# Mapeamento: Telefone → Nome no Notion
PHONE_TO_NAME = {
    "554191851256": "Estevao Antunes",
    "5511999322027": "Julio Inoue",
    "554888428246": "Arthur Leuzzi",
    "551191095230": "Leticia",
    "5511980992410": "Joaquim",
    "554792054701": "Kevin",
    "552498117033": "Leo Confettura",
    "55448428260": "Luna Machado",
    "559991244030": "Rebeca Figueredo",
    "551998100715": "Sami Monteleone",
    "551199143605": "Saraiva",
}


def get_name_by_phone(phone: str) -> str:
    """
    Retorna nome da pessoa pelo telefone.

    Args:
        phone: Telefone (com ou sem +, com ou sem formatação)

    Returns:
        Nome da pessoa ou None
    """
    # Limpar telefone (remover +, espaços, hífen)
    clean_phone = phone.replace('+', '').replace('-', '').replace(' ', '')
    return PHONE_TO_NAME.get(clean_phone)
