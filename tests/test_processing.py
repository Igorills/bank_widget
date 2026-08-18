import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.fixture
def transactions() -> list[dict[str, str]]:
    """Возвращает тестовые данные о транзакциях."""
    return [
        {"id": "1", "state": "EXECUTED", "date": "2024-03-15T10:00:00"},
        {"id": "2", "state": "CANCELED", "date": "2024-01-10T12:00:00"},
        {"id": "3", "state": "EXECUTED", "date": "2024-05-20T15:30:00"},
        {"id": "4", "state": "PENDING", "date": "2024-02-25T09:00:00"},
        {"id": "5", "state": "EXECUTED", "date": "2024-03-15T18:00:00"},
    ]


@pytest.mark.parametrize(
    "state, expected_ids",
    [
        ("EXECUTED", ["1", "3", "5"]),
        ("CANCELED", ["2"]),
        ("PENDING", ["4"]),
        ("UNKNOWN", []),
    ],
)
def test_filter_by_state(
    transactions: list[dict[str, str]],
    state: str,
    expected_ids: list[str],
) -> None:
    """Проверяет фильтрацию транзакций по статусу."""
    result = filter_by_state(transactions, state)

    assert [item["id"] for item in result] == expected_ids


def test_filter_by_state_default(transactions: list[dict[str, str]]) -> None:
    """Проверяет фильтрацию по статусу EXECUTED по умолчанию."""
    result = filter_by_state(transactions)

    assert all(item["state"] == "EXECUTED" for item in result)
    assert len(result) == 3


@pytest.mark.parametrize(
    "reverse, expected_ids",
    [
        (True, ["3", "5", "1", "4", "2"]),
        (False, ["2", "4", "1", "5", "3"]),
    ],
)
def test_sort_by_date(
    transactions: list[dict[str, str]],
    reverse: bool,
    expected_ids: list[str],
) -> None:
    """Проверяет сортировку транзакций по дате."""
    result = sort_by_date(transactions, reverse)

    assert [item["id"] for item in result] == expected_ids


def test_sort_by_date_default(transactions: list[dict[str, str]]) -> None:
    """Проверяет сортировку по убыванию по умолчанию."""
    result = sort_by_date(transactions)

    assert result[0]["date"] == "2024-05-20T15:30:00"
    assert result[-1]["date"] == "2024-01-10T12:00:00"


def test_sort_by_date_missing_date() -> None:
    """Проверяет сортировку при отсутствии даты."""
    data = [
        {"id": "1", "state": "EXECUTED"},
        {"id": "2", "state": "EXECUTED", "date": "2024-01-01"},
    ]

    result = sort_by_date(data, reverse=False)

    assert result[0]["id"] == "1"
    assert result[1]["id"] == "2"
