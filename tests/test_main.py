from unittest.mock import MagicMock, patch

from src.main import format_transaction, main, mask_payment_info

# Тесты для mask_payment_info и format_transaction


def test_mask_payment_info_card() -> None:
    """Проверяет маскирование карты."""
    result = mask_payment_info("Visa Platinum 7000792289606361")
    assert "7000 79** **** 6361" in result


def test_mask_payment_info_account() -> None:
    """Проверяет маскирование счета."""
    result = mask_payment_info("Счет 73654108430135874305")
    assert "**4305" in result


def test_mask_payment_info_empty() -> None:
    """Проверяет обработку пустой строки или нестрокового аргумента."""
    assert mask_payment_info("") == ""
    assert mask_payment_info(123) == ""  # type: ignore


def test_format_transaction_json_structure() -> None:
    """Проверяет форматирование транзакции с вложенной структурой operationAmount (JSON)."""
    tx = {
        "date": "2019-12-08T22:46:21.935582",
        "description": "Открытие вклада",
        "to": "Счет 41030927182030584288",
        "operationAmount": {
            "amount": "41595.41",
            "currency": {"name": "руб.", "code": "RUB"},
        },
    }
    result = format_transaction(tx)
    assert "08.12.2019 Открытие вклада" in result
    assert "**4288" in result
    assert "Сумма: 41595.41 руб." in result


def test_format_transaction_flat_structure() -> None:
    """Проверяет форматирование транзакции с плоской структурой (CSV/Excel)."""
    tx = {
        "date": "2021-04-12",
        "description": "Перевод со счета на счет",
        "from": "Счет 73654108430135874305",
        "to": "Счет 41030927182030584288",
        "amount": "1000",
        "currency_name": "руб.",
    }
    result = format_transaction(tx)
    assert "12.04.2021 Перевод со счета на счет" in result
    assert "-> " in result
    assert "Сумма: 1000 руб." in result


# Тесты для main()


@patch("builtins.input", side_effect=["4"])
@patch("builtins.print")
def test_main_invalid_menu_choice(_mock_print: MagicMock, _mock_input: MagicMock) -> None:
    """Проверяет завершение работы при неверном выборе меню."""
    main()
    _mock_print.assert_any_call("\nПрограмма: Некорректный выбор пункта меню.")


@patch("src.main.load_transactions", return_value=[])
@patch("builtins.input", side_effect=["1", "EXECUTED", "нет", "нет", "нет"])
@patch("builtins.print")
def test_main_empty_transactions(_mock_print: MagicMock, _mock_input: MagicMock, _mock_load: MagicMock) -> None:
    """Проверяет сценарий, когда в выборке нет транзакций."""
    main()
    _mock_print.assert_any_call("Программа: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")


@patch("src.main.process_bank_search")
@patch("src.main.filter_by_currency")
@patch("src.main.sort_by_date")
@patch("src.main.filter_by_state")
@patch("src.main.load_transactions")
@patch("builtins.input", side_effect=["1", "INVALID_STATUS", "EXECUTED", "да", "по убыванию", "да", "да", "Перевод"])
@patch("builtins.print")
def test_main_full_flow_json(
    _mock_print: MagicMock,
    _mock_input: MagicMock,
    mock_load: MagicMock,
    mock_filter_state: MagicMock,
    mock_sort_date: MagicMock,
    mock_filter_curr: MagicMock,
    mock_search: MagicMock,
) -> None:
    """Проверяет полный успешный цикл выполнения main с JSON-файлом."""
    sample_tx = {
        "date": "2019-12-08T22:46:21.935582",
        "description": "Перевод организации",
        "amount": "100",
        "currency_name": "руб.",
    }

    mock_load.return_value = [sample_tx]
    mock_filter_state.return_value = [sample_tx]
    mock_sort_date.return_value = [sample_tx]
    mock_filter_curr.return_value = [sample_tx]
    mock_search.return_value = [sample_tx]

    main()

    mock_load.assert_called_once()
    mock_filter_state.assert_called_once_with([sample_tx], "EXECUTED")
    mock_sort_date.assert_called_once_with([sample_tx], reverse=True)
    mock_filter_curr.assert_called_once_with([sample_tx], "RUB")
    mock_search.assert_called_once_with([sample_tx], "Перевод")


@patch("src.main.read_transactions_csv")
@patch("builtins.input", side_effect=["2", "CANCELED", "нет", "нет", "нет"])
@patch("builtins.print")
def test_main_csv_choice(_mock_print: MagicMock, _mock_input: MagicMock, mock_read_csv: MagicMock) -> None:
    """Проверяет выбор CSV-файла."""
    mock_read_csv.return_value = []
    main()
    mock_read_csv.assert_called_once()


@patch("src.main.read_transactions_excel")
@patch("builtins.input", side_effect=["3", "PENDING", "нет", "нет", "нет"])
@patch("builtins.print")
def test_main_excel_choice(_mock_print: MagicMock, _mock_input: MagicMock, mock_read_excel: MagicMock) -> None:
    """Проверяет выбор Excel-файла."""
    mock_read_excel.return_value = []
    main()
    mock_read_excel.assert_called_once()
