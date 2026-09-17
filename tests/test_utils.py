import json
import os
from unittest.mock import mock_open, patch

from src.utils import LOG_FILE_PATH, load_transactions


def test_load_transactions_valid_json() -> None:
    """Проверка успешной загрузки валидного списка транзакций из JSON."""
    mock_data = [{"id": 1, "amount": "100"}, {"id": 2, "amount": "200"}]
    mock_json = json.dumps(mock_data)

    with patch("os.path.exists", return_value=True):
        with patch("builtins.open", mock_open(read_data=mock_json)):
            result = load_transactions("data/operations.json")
            assert result == mock_data


def test_load_transactions_file_not_found() -> None:
    """Проверка возврата пустого списка, если файл не существует."""
    with patch("os.path.exists", return_value=False):
        result = load_transactions("data/non_existing.json")
        assert result == []


def test_load_transactions_invalid_json() -> None:
    """Проверка возврата пустого списка при поврежденном JSON-файле."""
    invalid_json = "{ invalid json content "

    with patch("os.path.exists", return_value=True):
        with patch("builtins.open", mock_open(read_data=invalid_json)):
            result = load_transactions("data/corrupted.json")
            assert result == []


def test_load_transactions_not_a_list() -> None:
    """Проверка возврата пустого списка, если JSON содержит словарь вместо списка."""
    mock_dict = {"id": 1, "amount": "100"}
    mock_json = json.dumps(mock_dict)

    with patch("os.path.exists", return_value=True):
        with patch("builtins.open", mock_open(read_data=mock_json)):
            result = load_transactions("data/dict_operations.json")
            assert result == []


def test_load_transactions_empty_file() -> None:
    """Проверка возврата пустого списка при пустом файле."""
    with patch("os.path.exists", return_value=True):
        with patch("builtins.open", mock_open(read_data="")):
            result = load_transactions("data/empty.json")
            assert result == []


# Тесты для проверки логирования (logging)


def test_load_transactions_logging_success() -> None:
    """Проверяет создание файла логов и записи успешной загрузки (INFO)."""
    mock_data = [{"id": 1, "amount": "100"}]
    mock_json = json.dumps(mock_data)

    with patch("os.path.exists", return_value=True):
        with patch("builtins.open", mock_open(read_data=mock_json)):
            load_transactions("data/operations.json")

    assert os.path.exists(LOG_FILE_PATH)
    with open(LOG_FILE_PATH, "r", encoding="utf-8") as f:
        log_content = f.read()
        assert "utils" in log_content
        assert "INFO" in log_content
        assert "Успешно загружено 1 транзакций" in log_content


def test_load_transactions_logging_error_not_found() -> None:
    """Проверяет запись ошибки уровня ERROR при отсутствии файла."""
    with patch("os.path.exists", return_value=False):
        load_transactions("data/missing.json")

    with open(LOG_FILE_PATH, "r", encoding="utf-8") as f:
        log_content = f.read()
        assert "ERROR" in log_content
        assert "Файл не найден по пути" in log_content
