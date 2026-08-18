import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    "data, expected",
    [
        ("Visa 1234567890123456", "Visa 1234 56** **** 3456"),
        ("MasterCard 9876543210987654", "MasterCard 9876 54** **** 7654"),
        ("Счет 1234567890", "Счет **7890"),
        ("Счет 1234", "Счет **1234"),
    ],
)
def test_mask_account_card(data: str, expected: str) -> None:
    """Проверяет маскирование карт и счетов."""
    assert mask_account_card(data) == expected


@pytest.mark.parametrize(
    "data",
    [
        "",
        "   ",
        "Visa",
        "Счет",
        "Visa abcdef1234567890",
    ],
)
def test_mask_account_card_invalid(data: str) -> None:
    """Проверяет обработку некорректных входных данных."""
    with pytest.raises(ValueError):
        mask_account_card(data)


@pytest.mark.parametrize(
    "date_string, expected",
    [
        ("2024-01-15T10:30:00", "15.01.2024"),
        ("2023-12-31T23:59:59", "31.12.2023"),
        ("2020-02-29T12:00:00", "29.02.2020"),
    ],
)
def test_get_date(date_string: str, expected: str) -> None:
    """Проверяет преобразование даты."""
    assert get_date(date_string) == expected


@pytest.mark.parametrize(
    "date_string",
    [
        "2024-13-01",
        "2024-01-32",
        "неверная дата",
        "",
    ],
)
def test_get_date_invalid(date_string: str) -> None:
    """Проверяет обработку некорректных дат."""
    with pytest.raises(ValueError):
        get_date(date_string)
