import re
from collections import Counter
from typing import Any, Dict, List


def process_bank_search(data: List[Dict[str, Any]], search: str) -> List[Dict[str, Any]]:
    """Ищет операции, у которых в описании (description) встречается заданная строка (паттерн).

    Поиск регистронезависимый и использует библиотеку re.

    `param data` Список словарей с данными о банковских операциях.
    `param search` Строка или регулярное выражение для поиска.
    `return` Список словарей с найденными операциями.
    """
    if not search or not data:
        return []

    pattern = re.compile(re.escape(search), re.IGNORECASE)
    matched_operations = []

    for operation in data:
        description = operation.get("description", "")
        if isinstance(description, str) and pattern.search(description):
            matched_operations.append(operation)

    return matched_operations


def process_bank_operations(data: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """Считает количество операций для каждой категории из заданного списка.

    Подсчет выполняется на основе поля description с использованием Counter.

    `param data` Список словарей с данными о банковских операциях.
    `param categories` Список категорий операций для подсчета.
    `return` Словарь, где ключи — названия категорий, значения — количество операций.
    """
    if not data or not categories:
        return {category: 0 for category in categories} if categories else {}

    # Извлекаем все описания из списка транзакций
    descriptions = [
        operation.get("description") for operation in data if isinstance(operation.get("description"), str)
    ]

    # Используем Counter из модуля collections
    description_counts = Counter(descriptions)

    # Формируем итоговый словарь только по запрошенным категориям
    return {category: description_counts[category] for category in categories}
