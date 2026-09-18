import os
from typing import Any, Dict, List

from src.file_readers import read_transactions_csv, read_transactions_excel
from src.generators import filter_by_currency
from src.masks import get_mask_account, get_mask_card_number
from src.processing import filter_by_state, sort_by_date
from src.services import process_bank_search
from src.utils import load_transactions


def mask_payment_info(payment_str: str) -> str:
    """Маскирует счет или номер карты в зависимости от формата исходной строки."""
    if not payment_str or not isinstance(payment_str, str):
        return ""

    parts = payment_str.split()
    if not parts:
        return ""

    number = parts[-1]
    name = " ".join(parts[:-1])

    if name.lower().startswith("счет") or name.lower().startswith("счёт"):
        masked_number = get_mask_account(number)
    else:
        masked_number = get_mask_card_number(number)

    return f"{name} {masked_number}".strip() if name else masked_number


def format_transaction(transaction: Dict[str, Any]) -> str:
    """Форматирует одну транзакцию для вывода в консоль."""
    raw_date = str(transaction.get("date", ""))
    date_formatted = ""
    if raw_date and len(raw_date) >= 10:
        date_parts = raw_date[:10].split("-")
        if len(date_parts) == 3:
            date_formatted = f"{date_parts[2]}.{date_parts[1]}.{date_parts[0]}"

    description = transaction.get("description", "")

    from_info = mask_payment_info(str(transaction.get("from", "")))
    to_info = mask_payment_info(str(transaction.get("to", "")))

    if from_info and to_info:
        route_info = f"{from_info} -> {to_info}"
    elif to_info:
        route_info = to_info
    else:
        route_info = from_info

    # Извлечение суммы и валюты без неиспользуемого предварительного присваивания
    operation_amount = transaction.get("operationAmount")

    if isinstance(operation_amount, dict):
        amount = operation_amount.get("amount", "")
        currency_info = operation_amount.get("currency", {})
        if isinstance(currency_info, dict):
            currency = currency_info.get("name", "") or currency_info.get("code", "")
        else:
            currency = ""
    else:
        amount = transaction.get("amount", "")
        currency = transaction.get("currency_name", "") or transaction.get("currency_code", "руб.")

    lines = [f"{date_formatted} {description}".strip()]
    if route_info:
        lines.append(route_info)
    lines.append(f"Сумма: {amount} {currency}".strip())

    return "\n".join(lines)


def main() -> None:
    """Основная функция управления пользовательским интерфейсом."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла\n")

    # 1. Выбор источника данных
    file_choice = input("Пользователь: ").strip()

    if file_choice == "1":
        print("\nПрограмма: Для обработки выбран JSON-файл.")
        json_path = os.path.join("data", "operations.json")
        transactions: List[Dict[str, Any]] = load_transactions(json_path)
    elif file_choice == "2":
        print("\nПрограмма: Для обработки выбран CSV-файл.")
        csv_path = os.path.join("data", "transactions.csv")
        transactions = read_transactions_csv(csv_path)
    elif file_choice == "3":
        print("\nПрограмма: Для обработки выбран XLSX-файл.")
        xlsx_path = os.path.join("data", "transactions_excel.xlsx")
        transactions = read_transactions_excel(xlsx_path)
    else:
        print("\nПрограмма: Некорректный выбор пункта меню.")
        return

    # 2. Фильтрация по статусу
    valid_statuses = {"EXECUTED", "CANCELED", "PENDING"}
    while True:
        print("\nПрограмма: Введите статус, по которому необходимо выполнить фильтрацию.")
        print("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\n")
        status_input = input("Пользователь: ").strip()
        status_upper = status_input.upper()

        if status_upper in valid_statuses:
            transactions = filter_by_state(transactions, status_upper)
            print(f'\nПрограмма: Операции отфильтрованы по статусу "{status_upper}"')
            break
        else:
            print(f'\nПрограмма: Статус операции "{status_input}" недоступен.')

    # 3. Сортировка по дате
    print("\nПрограмма: Отсортировать операции по дате? Да/Нет\n")
    sort_choice = input("Пользователь: ").strip().lower()

    if sort_choice == "да":
        print("\nПрограмма: Отсортировать по возрастанию или по убыванию?\n")
        order_choice = input("Пользователь: ").strip().lower()
        is_descending = order_choice == "по убыванию"
        transactions = sort_by_date(transactions, reverse=is_descending)

    # 4. Фильтрация по рублевым транзакциям
    print("\nПрограмма: Выводить только рублевые транзакции? Да/Нет\n")
    rub_choice = input("Пользователь: ").strip().lower()

    if rub_choice == "да":
        transactions = list(filter_by_currency(transactions, "RUB"))

    # 5. Фильтрация по слову в описании
    print("\nПрограмма: Отфильтровать список транзакций по определенному слову в описании? Да/Нет\n")
    search_choice = input("Пользователь: ").strip().lower()

    if search_choice == "да":
        search_query = input("\nВведите слово для поиска: ").strip()
        transactions = process_bank_search(transactions, search_query)

    # 6. Печать итогового списка
    print("\nПрограмма: Распечатываю итоговый список транзакций...\n")

    if not transactions:
        print("Программа: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print(f"Программа:\nВсего банковских операций в выборке: {len(transactions)}\n")
    for tx in transactions:
        print(format_transaction(tx))
        print()


if __name__ == "__main__":
    main()
