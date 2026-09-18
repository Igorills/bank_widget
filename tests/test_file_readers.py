from unittest.mock import MagicMock, patch

import pandas as pd

from src.file_readers import read_transactions_csv, read_transactions_excel

# Тесты для read_transactions_csv


@patch("pandas.read_csv")
@patch("os.path.exists", return_value=True)
def test_read_transactions_csv_success(mock_exists: MagicMock, mock_read_csv: MagicMock) -> None:
    """Проверяет успешное считывание данных из CSV-файла."""
    mock_df = MagicMock()
    mock_data = [{"id": 1, "amount": 100.0, "currency": "RUB"}]
    mock_df.to_dict.return_value = mock_data
    mock_read_csv.return_value = mock_df

    result = read_transactions_csv("data/transactions.csv")

    assert result == mock_data
    mock_exists.assert_called_once_with("data/transactions.csv")
    mock_read_csv.assert_called_once_with("data/transactions.csv")
    mock_df.to_dict.assert_called_once_with(orient="records")


@patch("os.path.exists", return_value=False)
def test_read_transactions_csv_file_not_found(mock_exists: MagicMock) -> None:
    """Проверяет возврат пустого списка, если CSV-файл не существует."""
    result = read_transactions_csv("data/non_existing.csv")

    assert result == []
    mock_exists.assert_called_once_with("data/non_existing.csv")


@patch("pandas.read_csv", side_effect=pd.errors.EmptyDataError)
@patch("os.path.exists", return_value=True)
def test_read_transactions_csv_empty_data_error(_mock_exists: MagicMock, _mock_read_csv: MagicMock) -> None:
    """Проверяет обработку ошибки пустой структуры данных CSV."""
    result = read_transactions_csv("data/empty.csv")

    assert result == []


@patch("pandas.read_csv", side_effect=pd.errors.ParserError)
@patch("os.path.exists", return_value=True)
def test_read_transactions_csv_parser_error(_mock_exists: MagicMock, _mock_read_csv: MagicMock) -> None:
    """Проверяет обработку ошибки синтаксического анализа CSV."""
    result = read_transactions_csv("data/corrupted.csv")

    assert result == []


# Тесты для read_transactions_excel


@patch("pandas.read_excel")
@patch("os.path.exists", return_value=True)
def test_read_transactions_excel_success(mock_exists: MagicMock, mock_read_excel: MagicMock) -> None:
    """Проверяет успешное считывание данных из Excel-файла."""
    mock_df = MagicMock()
    mock_data = [{"id": 2, "amount": 250.5, "currency": "USD"}]
    mock_df.to_dict.return_value = mock_data
    mock_read_excel.return_value = mock_df

    result = read_transactions_excel("data/transactions_excel.xlsx")

    assert result == mock_data
    mock_exists.assert_called_once_with("data/transactions_excel.xlsx")
    mock_read_excel.assert_called_once_with("data/transactions_excel.xlsx")
    mock_df.to_dict.assert_called_once_with(orient="records")


@patch("os.path.exists", return_value=False)
def test_read_transactions_excel_file_not_found(mock_exists: MagicMock) -> None:
    """Проверяет возврат пустого списка, если Excel-файл не существует."""
    result = read_transactions_excel("data/non_existing.xlsx")

    assert result == []
    mock_exists.assert_called_once_with("data/non_existing.xlsx")


@patch("pandas.read_excel", side_effect=ValueError)
@patch("os.path.exists", return_value=True)
def test_read_transactions_excel_value_error(_mock_exists: MagicMock, _mock_read_excel: MagicMock) -> None:
    """Проверяет обработку исключения ValueError при чтении Excel-файла."""
    result = read_transactions_excel("data/invalid.xlsx")

    assert result == []


@patch("pandas.read_excel", side_effect=ImportError)
@patch("os.path.exists", return_value=True)
def test_read_transactions_excel_import_error(_mock_exists: MagicMock, _mock_read_excel: MagicMock) -> None:
    """Проверяет обработку исключения ImportError."""
    result = read_transactions_excel("data/no_engine.xlsx")

    assert result == []
