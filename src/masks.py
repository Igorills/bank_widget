import logging
import os

# 1. Путь к папке и файлу логов в корне проекта
LOGS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
os.makedirs(LOGS_DIR, exist_ok=True)
LOG_FILE_PATH = os.path.join(LOGS_DIR, "masks.log")

# 2. Создание отдельного объекта логгера
logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)  # Уровень не меньше, чем DEBUG

# 3. Настройка file_handler (режим 'w' обеспечит перезапись при каждом запуске)
file_handler = logging.FileHandler(LOG_FILE_PATH, mode="w", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

# 4. Настройка file_formatter: метка времени, название модуля, уровень, сообщение
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# 5. Установка форматера и добавление хендлера в логгер
file_handler.setFormatter(file_formatter)

# Избегаем дублирования хендлеров при повторных импортах
if not logger.handlers:
    logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер банковской карты."""
    logger.debug(f"Начало маскирования карты: {card_number}")

    if not isinstance(card_number, str) or not card_number.isdigit() or len(card_number) != 16:
        error_msg = f"Некорректный номер карты: '{card_number}'. Номер карты должен содержать 16 цифр."
        logger.error(error_msg)  # Ошибочные случаи с уровнем ERROR
        raise ValueError("Номер карты должен содержать 16 цифр.")

    masked_card = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
    logger.info("Номер карты успешно замаскирован")  # Успешный случай
    return masked_card


def get_mask_account(account_number: str) -> str:
    """Маскирует номер банковского счета."""
    logger.debug(f"Начало маскирования счета: {account_number}")

    if not isinstance(account_number, str) or not account_number.isdigit() or len(account_number) < 4:
        error_msg = f"Некорректный номер счета: '{account_number}'. Номер счета должен содержать не менее 4 цифр."
        logger.error(error_msg)  # Ошибочные случаи с уровнем ERROR
        raise ValueError("Номер счета должен содержать не менее 4 цифр.")

    masked_account = f"**{account_number[-4:]}"
    logger.info("Номер счета успешно замаскирован")  # Успешный случай
    return masked_account
