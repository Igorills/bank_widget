import os
from typing import Any, Dict

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")


def convert_to_rub(transaction: Dict[str, Any]) -> float:
    """Принимает словарь с транзакцией и возвращает сумму операции в рублях (float).
    Если транзакция в USD или EUR, запрашивает курс через внешний API.

    `param transaction` Словарь с данными о транзакции.
    `return` Сумма транзакции в рублях (float).
    """
    if not isinstance(transaction, dict):
        return 0.0

    operation_amount = transaction.get("operationAmount", {})
    if not isinstance(operation_amount, dict):
        return 0.0

    amount_str = operation_amount.get("amount", "0")
    currency = operation_amount.get("currency", {})

    # Безопасное получение кода валюты
    currency_code = currency.get("code") if isinstance(currency, dict) else "RUB"
    if not currency_code:
        currency_code = "RUB"

    try:
        amount = float(amount_str)
    except ValueError, TypeError:
        return 0.0

    # Если уже рубли
    if currency_code in ("RUB", "руб."):
        return amount

    # Конвертация для USD и EUR
    if currency_code in ("USD", "EUR"):
        if not API_KEY:
            # Если API_KEY не найден в .env, возвращаем 0.0 или исходный amount
            return amount

        url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={currency_code}&amount={amount}"
        headers = {"apikey": API_KEY}

        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                result = data.get("result")
                if result is not None:
                    return float(result)
        except requests.RequestException, ValueError:
            return amount

    return amount
