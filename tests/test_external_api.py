from typing import Any, Dict
from unittest.mock import Mock, patch

import requests

from src.external_api import convert_to_rub


def test_convert_to_rub_not_a_dict() -> None:
    """Проверка: если на вход передан не словарь, возвращается 0.0."""
    assert convert_to_rub("not a dict") == 0.0  # type: ignore[arg-type]


def test_convert_to_rub_invalid_operation_amount() -> None:
    """Проверка: если operationAmount не словарь, возвращается 0.0."""
    transaction = {"operationAmount": "invalid"}
    assert convert_to_rub(transaction) == 0.0


def test_convert_to_rub_invalid_amount_value() -> None:
    """Проверка: если amount не преобразуется во float, возвращается 0.0."""
    transaction = {"operationAmount": {"amount": "abc", "currency": {"code": "RUB"}}}
    assert convert_to_rub(transaction) == 0.0


def test_convert_to_rub_rub_currency() -> None:
    """Проверка: если валюта RUB или 'руб.', возвращается исходная сумма float без запроса к API."""
    transaction: Dict[str, Any] = {"operationAmount": {"amount": "1500.50", "currency": {"code": "RUB"}}}
    assert convert_to_rub(transaction) == 1500.50


def test_convert_to_rub_missing_currency_code() -> None:
    """Проверка: если код валюты отсутствует, по умолчанию используется RUB."""
    transaction: Dict[str, Any] = {"operationAmount": {"amount": "200.0", "currency": {}}}
    assert convert_to_rub(transaction) == 200.0


@patch("src.external_api.requests.get")
def test_convert_to_rub_usd_success(mock_get: Mock) -> None:
    """Проверка: успешный запрос к API для USD."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": 90500.0}
    mock_get.return_value = mock_response

    transaction: Dict[str, Any] = {"operationAmount": {"amount": "1000.00", "currency": {"code": "USD"}}}

    result = convert_to_rub(transaction)
    assert result == 90500.0
    mock_get.assert_called_once()


@patch("src.external_api.API_KEY", None)
def test_convert_to_rub_missing_api_key() -> None:
    """Проверка: если API_KEY отсутствует, возвращается исходный amount."""
    transaction: Dict[str, Any] = {"operationAmount": {"amount": "100.00", "currency": {"code": "USD"}}}
    assert convert_to_rub(transaction) == 100.00


@patch("src.external_api.requests.get")
def test_convert_to_rub_api_error_status(mock_get: Mock) -> None:
    """Проверка: если статус ответа не 200, возвращается исходный amount."""
    mock_response = Mock()
    mock_response.status_code = 500
    mock_get.return_value = mock_response

    transaction: Dict[str, Any] = {"operationAmount": {"amount": "100.00", "currency": {"code": "EUR"}}}

    assert convert_to_rub(transaction) == 100.00


@patch("src.external_api.requests.get")
def test_convert_to_rub_network_exception(mock_get: Mock) -> None:
    """Проверка: при сетевом исключении (RequestException) возвращается исходный amount."""
    mock_get.side_effect = requests.RequestException

    transaction: Dict[str, Any] = {"operationAmount": {"amount": "500.00", "currency": {"code": "USD"}}}

    assert convert_to_rub(transaction) == 500.00


def test_convert_to_rub_unsupported_currency() -> None:
    """Проверка: для не поддерживаемых валют (например, GBP) возвращается исходный amount."""
    transaction: Dict[str, Any] = {"operationAmount": {"amount": "300.00", "currency": {"code": "GBP"}}}
    assert convert_to_rub(transaction) == 300.00
