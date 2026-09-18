from src.services import process_bank_operations, process_bank_search


def test_process_bank_search_success() -> None:
    """Проверяет поиск операций по строке с помощью re."""
    mock_data = [
        {"id": 1, "description": "Перевод организации"},
        {"id": 2, "description": "Открытие вклада"},
        {"id": 3, "description": "Перевод частному лицу"},
    ]
    result = process_bank_search(mock_data, "перевод")
    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[1]["id"] == 3


def test_process_bank_search_not_found() -> None:
    """Проверяет возврат пустого списка при отсутствии совпадений."""
    mock_data = [{"id": 1, "description": "Перевод организации"}]
    assert process_bank_search(mock_data, "Оплата") == []


def test_process_bank_operations_counting() -> None:
    """Проверяет корректность подсчета категорий через Counter."""
    mock_data = [
        {"description": "Перевод организации"},
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
        {"description": "Оплата услуг"},
    ]
    categories = ["Перевод организации", "Открытие вклада", "Снятие наличных"]
    result = process_bank_operations(mock_data, categories)

    assert result == {
        "Перевод организации": 2,
        "Открытие вклада": 1,
        "Снятие наличных": 0,
    }
