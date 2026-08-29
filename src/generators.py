from typing import Any, Dict, Iterator, List


def filter_by_currency(transactions: List[Dict[str, Any]], currency_code: str = "USD") -> Iterator[Dict[str, Any]]:
    """Принимает список транзакций и возвращает итератор,
    который выдает транзакции с указанной валютой.

    `param transactions` Список словарей с данными о транзакциях.
    `param currency_code` Код валюты для фильтрации (по умолчанию 'USD').
    `return` Итератор по отфильтрованным транзакциям.
    """
    for transaction in transactions:
        operation_amount = transaction.get("operationAmount")
        if isinstance(operation_amount, dict):
            currency = operation_amount.get("currency")
            if isinstance(currency, dict) and currency.get("code") == currency_code:
                yield transaction


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Iterator[str]:
    """Принимает список транзакций и возвращает итератор,
    который поочередно выдает описание (description) каждой операции.

    `param transactions` Список словарей с данными о транзакциях.
    `return` Итератор по строкам с описаниями операций.
    """
    for transaction in transactions:
        description = transaction.get("description")
        if isinstance(description, str):
            yield description
        else:
            yield ""


def card_number_generator(start: int, stop: int) -> Iterator[str]:
    """Генерирует номера банковских карт в формате XXXX XXXX XXXX XXXX
    в заданном диапазоне включительно.

    `param start` Начальное число диапазона (например, 1).
    `param stop` Конечное число диапазона включительно (например, 5).
    `return` Итератор со строками заформатированных номеров карт.
    """
    for number in range(start, stop + 1):
        card_str = f"{number:016d}"
        formatted_card = f"{card_str[:4]} {card_str[4:8]} {card_str[8:12]} {card_str[12:]}"
        yield formatted_card
