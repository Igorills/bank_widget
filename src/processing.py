from typing import Any, Dict, List


def filter_by_state(data: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """Фильтрует список словарей с транзакциями по заданному статусу state.

    :param data: Список словарей с данными о транзакциях.
    :param state: Значение статуса для фильтрации (по умолчанию 'EXECUTED').
    :return: Новый список словарей, соответствующих указанному статусу.
    """
    return [item for item in data if item.get("state") == state]


def sort_by_date(data: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
    """Сортирует список словарей с транзакциями по дате.

    :param data: Список словарей с данными о транзакциях.
    :param reverse: Порядок сортировки (True — по убыванию, False — по возрастанию).
    :return: Новый отсортированный список словарей.
    """
    return sorted(data, key=lambda x: x.get("date", ""), reverse=reverse)
