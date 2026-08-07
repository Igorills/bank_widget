from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number

def mask_account_card(data: str) -> str:
    """Возвращает строку с замаскированным номером карты или счета."""

    if not data.strip():
        raise ValueError("Входная строка не должна быть пустой.")

    parts = data.rsplit(" ", 1)

    if len(parts) < 2:
        raise ValueError("Некорректный формат входной строки.")

    name, number = parts

    if not number.isdigit():
        raise ValueError("Номер карты или счета должен содержать только цифры.")

    if name == "Счет":
        return f"{name} {get_mask_account(number)}"

    return f"{name} {get_mask_card_number(number)}"

def get_date(date_string: str) -> str:
    """Преобразует дату из ISO-формата в формат ДД.ММ.ГГГГ."""

    return datetime.fromisoformat(date_string).strftime("%d.%m.%Y")