from typing import Any, Dict, List

import pytest

from src.generators import (
    card_number_generator,
    filter_by_currency,
    transaction_descriptions,
)


@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    """Фикстура с тестовым списком транзакций."""
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 873106592,
            "state": "EXECUTED",
            "date": "2019-07-15T11:47:45.820984",
            "operationAmount": {
                "amount": "41095.81",
                "currency": {"name": "руб.", "code": "RUB"},
            },
            "description": "Перевод организации",
            "from": "Счет 71967851379963886561",
            "to": "Счет 30739092040656752003",
        },
    ]


# Тестирование filter_by_currency

@pytest.mark.parametrize(
    "currency_code, expected_count",
    [
        ("USD", 2),
        ("RUB", 1),
        ("EUR", 0),
    ],
)
def test_filter_by_currency_valid(
    sample_transactions: List[Dict[str, Any]], currency_code: str, expected_count: int
) -> None:
    """Проверка корректной фильтрации транзакций по заданным валютам."""
    result = list(filter_by_currency(sample_transactions, currency_code))
    assert len(result) == expected_count
    for item in result:
        assert item["operationAmount"]["currency"]["code"] == currency_code


def test_filter_by_currency_empty_list() -> None:
    """Проверка работы функции с пустым списком транзакций."""
    result = list(filter_by_currency([]))
    assert result == []


def test_filter_by_currency_invalid_structure() -> None:
    """Проверка устойчивости при некорректной структуре словарей."""
    bad_data = [
        {"id": 1},  # нет operationAmount
        {"id": 2, "operationAmount": "invalid"},  # operationAmount не словарь
        {"id": 3, "operationAmount": {"currency": "invalid"}},  # currency не словарь
    ]
    result = list(filter_by_currency(bad_data, "USD"))
    assert result == []


# Тестирование transaction_descriptions

def test_transaction_descriptions_correct(sample_transactions: List[Dict[str, Any]]) -> None:
    """Проверка выдачи корректных описаний операций."""
    descriptions = list(transaction_descriptions(sample_transactions))
    expected = [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод организации",
    ]
    assert descriptions == expected


def test_transaction_descriptions_empty_list() -> None:
    """Проверка работы с пустым списком."""
    descriptions = list(transaction_descriptions([]))
    assert descriptions == []


def test_transaction_descriptions_missing_key() -> None:
    """Проверка обработки транзакций без ключа description или с некорректным типом."""
    bad_data = [
        {"id": 1},  # нет ключа description
        {"id": 2, "description": 123},  # не строка
    ]
    descriptions = list(transaction_descriptions(bad_data))
    assert descriptions == ["", ""]


# Тестирование card_number_generator

@pytest.mark.parametrize(
    "start, stop, expected",
    [
        (1, 3, ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003"]),
        (5, 5, ["0000 0000 0000 0005"]),
    ],
)
def test_card_number_generator_formatting_and_range(start: int, stop: int, expected: List[str]) -> None:
    """Проверка формирования номеров карт в заданном диапазоне и их формата."""
    result = list(card_number_generator(start, stop))
    assert result == expected


def test_card_number_generator_invalid_range() -> None:
    """Проверка, что при start > stop генератор корректно ничего не выдает."""
    result = list(card_number_generator(5, 1))
    assert result == []


def test_card_number_generator_boundary() -> None:
    """Проверка работы с близкими к 16 цифрам границами."""
    gen = card_number_generator(9999999999999999, 9999999999999999)
    assert next(gen) == "9999 9999 9999 9999"
    with pytest.raises(StopIteration):
        next(gen)
