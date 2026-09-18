import os
from typing import Any, Dict, List

import pandas as pd


def read_transactions_csv(file_path: str) -> List[Dict[str, Any]]:
    """Считывает финансовые операции из CSV-файла и возвращает список словарей.

    `param file_path` Путь к CSV-файлу.
    `return` Список словарей с данными о транзакциях или пустой список.
    """
    if not os.path.exists(file_path):
        return []

    try:
        df = pd.read_csv(file_path)
        return df.to_dict(orient="records")
    except pd.errors.EmptyDataError, pd.errors.ParserError, FileNotFoundError, ValueError:
        return []


def read_transactions_excel(file_path: str) -> List[Dict[str, Any]]:
    """Считывает финансовые операции из Excel-файла (.xlsx) и возвращает список словарей.

    `param file_path` Путь к Excel-файлу.
    `return` Список словарей с данными о транзакциях или пустой список.
    """
    if not os.path.exists(file_path):
        return []

    try:
        df = pd.read_excel(file_path)
        return df.to_dict(orient="records")
    except FileNotFoundError, ValueError, ImportError:
        return []
