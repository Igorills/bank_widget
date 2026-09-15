import json
import logging
import os
from typing import Any, Dict, List

# 1. Формирование пути к папке logs в корне проекта
LOGS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
os.makedirs(LOGS_DIR, exist_ok=True)
LOG_FILE_PATH = os.path.join(LOGS_DIR, "utils.log")

# 2. Создание отдельного объекта логгера для модуля utils
logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)  # Уровень не меньше, чем DEBUG

# 3. Настройка file_handler (режим 'w' перезаписывает файл при каждом запуске)
file_handler = logging.FileHandler(LOG_FILE_PATH, mode="w", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

# 4. Настройка file_formatter: метка времени, название модуля, уровень, сообщение
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# 5. Установка форматера и добавление хендлера в логгер
file_handler.setFormatter(file_formatter)

if not logger.handlers:
    logger.addHandler(file_handler)


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """Принимает путь к JSON-файлу и возвращает список словарей с данными о транзакциях.
    Если файл пустой, содержит не список или не найден, возвращает пустой список.

    `param file_path` Путь до JSON-файла.
    `return` Список словарей с транзакциями или пустой список.
    """
    logger.debug(f"Попытка загрузки транзакций из файла: '{file_path}'")

    if not os.path.exists(file_path):
        logger.error(f"Файл не найден по пути: '{file_path}'")
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                logger.info(f"Успешно загружено {len(data)} транзакций из файла '{file_path}'")
                return data
            else:
                logger.error(f"Файл '{file_path}' содержит не список, а тип {type(data).__name__}")
                return []
    except (json.JSONDecodeError, OSError) as e:
        logger.error(f"Ошибка при чтении или декодировании файла '{file_path}': {e}")
        return []
