# Банковский виджет
Виджет для обработки и форматирования данных банковских операций. Проект предоставляет функции для маскирования номеров карт и счетов, форматирования дат, а также фильтрации и сортировки транзакций.

## Технологии
- Python 3.10+

## Основные функции
### Модуль src/maskc.py
- get_mask_card_number(card_number): принимает номер карты (16 цифр) и возвращает маску в формате XXXX XX **** XXXX.
- Настроен отдельный объект логгера masks с уровнем логирования DEBUG.
- Добавлен FileHandler с записью в файл logs/masks.log в корне проекта (в режиме 'w' для перезаписи при каждом запуске).
- Настроен Formatter с записью: метки времени, имени модуля, уровня серьезности и текстового сообщения (%(asctime)s - %(name)s - %(levelname)s - %(message)s).
- Добавлено логирование успешных операций маскирования номеров карт и счетов (INFO/DEBUG).
- Добавлено логирование ошибочных сценариев при передаче невалидных данных с уровнем ERROR.
### Модуль src/widget.py
- mask_account_card(data): определяет тип (карта или счет) во входной строке и маскирует номер.
- get_date(date_string): преобразует дату из формата ISO (YYYY-MM-DDTHH:MM:SS.ms) в формат ДД.ММ.ГГГГ.
### Модуль src/processing.py
- filter_by_state(data, state='EXECUTED'): фильтрует список транзакций по заданному статусу (EXECUTED, CANCELED и т. д.).
- sort_by_date(data, reverse=True): сортирует список транзакций по дате (по умолчанию — от самых свежих к старым).
### Модуль src/generators.py
- filter_by_currency(transactions, currency_code): итератор, поочередно выдающий транзакции с указанной валютой (по умолчанию 'USD').
- transaction_descriptions(transactions): итератор, поочередно выдающий текстовое описание каждой операции.
- card_number_generator(start, stop): генератор номеров банковских карт в формате XXXX XXXX XXXX XXXX в заданном диапазоне.
### Модуль src/decorators.py
- Принимает необязательный аргумент filename: Optional[str] = None.
- При успешном выполнении записывает: <имя_функции> ok.
- При ошибке записывает: <имя_функции> error: <тип_ошибки>. Inputs: <args>, <kwargs> и повторно вызывает исключение (raise).
- Направляет вывод в файл (при указании filename) или в консоль (если filename не задан).
### Модуль src/utils.py
- Обработка данных из JSON-файлов и поддержка конвертации валют через внешний API.
- Загрузка транзакций из JSON (`src/utils.py`)
- Функция `load_transactions(file_path)` отвечает за безопасное чтение данных:
    * Принимает путь к `.json` файлу и возвращает список словарей с транзакциями.
    * Устойчива к ошибкам: если файл пустой, поврежден или содержит не список, функция возвращает пустой список `[]`.
- Настроен отдельный объект логера utils с уровнем логирования DEBUG.
- Добавлен FileHandler с записью в файл logs/utils.log в корне проекта (режим перезаписи 'w').
- Применен аналогичный формат логов (%(asctime)s - %(name)s - %(levelname)s - %(message)s).
- Добавлено логирование успешной загрузки транзакций из JSON с указанием количества обработанных элементов (INFO/DEBUG).
- Добавлено логирование ошибок с уровнем ERROR (отсутствие файла по указанному пути, некорректная структура JSON, повреждение содержимого файла).
### Модуль src/external_api.py
- Принимает словарь с транзакцией и возвращает сумму (тип float).
- Для операций в USD и EUR делает запрос к внешнему API (APILayer/Exchange Rates Data) и пересчитывает сумму в рубли по текущему курсу.
- Для рублевых операций возвращает исходную сумму без сетевых запросов.
- Безопасно обрабатывает ошибки сети и отсутствующие ключи.
### Модуль src/file_readers.py
- `read_transactions_csv(file_path: str) -> list[dict]`
  Считывает финансовые операции из CSV-файла. Принимает путь к файлу и возвращает список словарей. В случае отсутствия файла, повреждения данных или ошибок синтаксиса возвращает пустой список `[]`.

- `read_transactions_excel(file_path: str) -> list[dict]`
  Считывает финансовые операции из файлов формата Excel (`.xlsx`, `.xls`). Возвращает данные в виде списка словарей. Корректно обрабатывает ошибки отсутствия файла или отсутствия необходимых зависимостей.

## Тестирование
Реализованы unit-тесты с использованием: `pytest`, `capsys`, `tmp_path`.
В проекте реализовано 83 теста, которые проверяют работу функций модулей `masks`, `widget`, `processing`, `generators`, `decorators`,`utils`,`external_api`, `file_readers`.

Добавлены unit-тесты для проверки создания файлов masks.log и utils.log в директории logs/.
Написаны проверки записи сообщений успешного выполнения (INFO) и корректного перехвата ошибок (ERROR).

Проведено успешное тестирование всего набора тестов через `pytest --cov=src` с сохранением высокого процента покрытия кода.
Также проект проверяется с помощью линтеров и форматеров:
`flake8`
`mypy`
`isort`
Все тесты успешно проходят, ошибок `Flake8` и `mypy` нет.

## Установка и запуск
1. Клонируйте репозиторий:
```
https://github.com/Igorills/bank_widget.git
```
2. Установите зависимости:
```
pip install -r requirements.txt
```

## Примеры использования

### Работа с базовыми модулями проекта
```
from src.generators import filter_by_currency, transaction_descriptions, card_number_generator
from src.widget import mask_account_card, get_date
from src.processing import filter_by_state, sort_by_date

transactions = [
{
"id": 939719570,
"state": "EXECUTED",
"date": "2018-06-30T02:08:58.425572",
"operationAmount": {
"amount": "9824.07",
"currency": {"name": "USD", "code": "USD"}
},
"description": "Перевод организации",
"from": "Счет 75106830613657916952",
"to": "Счет 11776614605963066702"
},
{
"id": 142264268,
"state": "EXECUTED",
"date": "2019-04-04T23:20:05.206878",
"operationAmount": {
"amount": "79114.93",
"currency": {"name": "USD", "code": "USD"}
},
"description": "Перевод со счета на счет",
"from": "Счет 19708645243227258542",
"to": "Счет 75651667383060284188"
},
{
"id": 873106923,
"state": "EXECUTED",
"date": "2019-03-23T01:09:46.296404",
"operationAmount": {
"amount": "43318.34",
"currency": {"name": "руб.", "code": "RUB"}
},
"description": "Перевод со счета на счет",
"from": "Счет 44812258784861134719",
"to": "Счет 74489636417521191160"
},
{
"id": 895315941,
"state": "EXECUTED",
"date": "2018-08-19T04:27:37.904916",
"operationAmount": {
"amount": "56883.54",
"currency": {"name": "USD", "code": "USD"}
},
"description": "Перевод с карты на карту",
"from": "Visa Classic 6831982476737658",
"to": "Visa Platinum 8990922113665229"
},
{
"id": 594226727,
"state": "CANCELED",
"date": "2018-09-12T21:27:25.241689",
"operationAmount": {
"amount": "67314.70",
"currency": {"name": "руб.", "code": "RUB"}
},
"description": "Перевод организации",
"from": "Visa Platinum 1246377376343588",
"to": "Счет 14211924144426031657"
}
]
```

#### 1. Фильтрация по валюте USD
```
usd_transactions = filter_by_currency(transactions, "USD")
print(next(usd_transactions)["id"])  # 939719570
```

#### 2. Перебор описаний операций по очереди
```
descriptions = transaction_descriptions(transactions)
for desc in descriptions:
print(desc)
```

#### 3. Генерация заформатированных номеров карт
```
for card_num in card_number_generator(1, 3):
print(card_num)

Вывод:
0000 0000 0000 0001
0000 0000 0000 0002
0000 0000 0000 0003
```

### Логирование в файл
```
from src.decorators import log


# Логирование в файл
@log(filename="mylog.txt")
def my_function(x: int, y: int) -> int:
    return x + y


my_function(1, 2)
# В mylog.txt запишется: my_function ok


# Логирование в консоль с ошибкой
@log()
def divide(x: int, y: int) -> float:
    return x / y


divide(1, 0)
# В консоль выведется: divide error: ZeroDivisionError. Inputs: (1, 0), {}
```

## ⚙️ Настройка переменных окружения

Создайте файл `.env` в корневой директории проекта, скопировав шаблон:
   ```
   cp .env.example .env
   ```
