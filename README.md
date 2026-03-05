# Проект по маскированию банковских реквизитов

## 📋 Описание

Проект предназначен для безопасного маскирования конфиденциальной финансовой информации — номеров банковских карт и счетов — с сохранением возможности идентификации записей. 

### Основные возможности:
- ✅ Маскировка номеров карт в формате XXXX XX** **** XXXX
- ✅ Маскировка номеров счетов в формате **XXXX
- ✅ Обработка структурированных данных (списков пользователей, транзакций)
- ✅ Форматирование дат
- ✅ Фильтрация и сортировка транзакций
- ✅ Генерация номеров банковских карт
- ✅ Обработка больших объемов данных через генераторы

## 🚀 Установка

1. **Клонируйте репозиторий:**
```bash
git clone https://github.com/bezza8418/pythonProject_Masker
cd pythonProject_Masker
```

2.** Установите зависимости:**
```bash
pip install -r requirements.txt
```
Или с использованием Poetry:
```bash
poetry install
```

## 📚 Использование

### 1. Маскировка номера карты (`get_mask_card_number`)
```python
from src.masks import get_mask_card_number

masked = get_mask_card_number("7000792289606361")
print(masked)  # 7000 79** **** 6361
```

### 2. Маскировка номера счёта (`get_mask_account`)
```python
from src.masks import get_mask_account

masked = get_mask_account("73654108430135874305")
print(masked)  # **4305
```

### 3. Маскировка персональных данных (`mask_personal_data`)
```python
from src.masks import mask_personal_data

data = {
    "name": "Иван Петров",
    "card": "7000792289606361",
    "account": "73654108430135874305"
}
masked_data = mask_personal_data(data)
print(masked_data)
# {
#     "name": "Иван Петров",
#     "card": "7000 79** **** 6361",
#     "account": "**4305"
# }
```

### 4. Обработка списка пользователей (`process_user_data`)
```python
from src.masks import process_user_data

users = [
    {"name": "Иван", "card": "7000792289606361"},
    {"name": "Петр", "account": "73654108430135874305"}
]
result = process_user_data(users)
print(result)
```

### 5. Универсальная маскировка (`mask_financial_info`)
```python
from src.masks import mask_financial_info

# Маскировка карты
print(mask_financial_info("card", "7000792289606361"))  # 7000 79** **** 6361
# Маскировка счета
print(mask_financial_info("account", "73654108430135874305"))  # **4305
```

### 6. Обработка строки с информацией о карте/счёте (`mask_account_card`)
```python
from src.widget import mask_account_card

print(mask_account_card("Счет 73654108430135874305"))  # Счет **4305
print(mask_account_card("Visa Platinum 7000792289606361"))  # Visa Platinum 7000 79** **** 6361
```

### 7. Форматирование даты (`get_date`)
```python
from src.widget import get_date

date = get_date("2024-03-11T02:26:18.671407")
print(date)  # 11.03.2024
```

### 8. Фильтрация транзакций (`filter_by_state`)
```python
from src.processing import filter_by_state

transactions = [
    {"id": 1, "state": "EXECUTED", "amount": 100},
    {"id": 2, "state": "PENDING", "amount": 200},
]
executed = filter_by_state(transactions, "EXECUTED")
print(executed)  # [{"id": 1, "state": "EXECUTED", "amount": 100}]
```

### 9. Сортировка транзакций (`sort_by_date`)
```python
from src.processing import sort_by_date

transactions = [
    {"id": 1, "date": "2024-03-11T02:26:18.671407"},
    {"id": 2, "date": "2024-03-10T15:30:00.000000"},
]
sorted_trans = sort_by_date(transactions, reverse=True)
```

### 10. Фильтрация по валюте (`filter_by_currency`)
```python
from src.generators import filter_by_currency

transactions = [
    {"id": 1, "operationAmount": {"currency": {"code": "USD"}}},
    {"id": 2, "operationAmount": {"currency": {"code": "EUR"}}},
    {"id": 3, "operationAmount": {"currency": {"code": "USD"}}},
]

usd_transactions = list(filter_by_currency(transactions, "USD"))
print([t["id"] for t in usd_transactions])  # [1, 3]
```

### 11. Получение описаний транзакций (`transaction_descriptions`)
```python
from src.generators import transaction_descriptions

# Пример списка транзакций
transactions = [
    {"description": "Перевод организации"},
    {"description": "Перевод со счета на счет"},
    {"description": "Перевод с карты на карту"},
]

descriptions = transaction_descriptions(transactions)
for desc in descriptions:
    print(desc)
# Вывод:
# Перевод организации
# Перевод со счета на счет
# Перевод с карты на карту
```

### 12. Генератор номеров карт (`card_number_generator`)
```python
from src.generators import card_number_generator

for card in card_number_generator(1, 5):
    print(card)
# 0000 0000 0000 0001
# 0000 0000 0000 0002
# 0000 0000 0000 0003
# 0000 0000 0000 0004
# 0000 0000 0000 0005
```

### 13. Логирование функций с декоратором `log`

Декоратор для автоматического логирования вызовов функций.

```python
from src.decorators import log

# Логирование в консоль
@log()
def divide(a: int, b: int) -> float:
    return a / b

divide(10, 2)  # В консоль выведется: "divide ok"
divide(10, 0)  # В консоль выведется: "divide error: ZeroDivisionError. Inputs: (10, 0), {}"

# Логирование в файл
@log(filename="mylog.txt")
def add(a: int, b: int) -> int:
    return a + b

add(5, 3)  # В файл mylog.txt запишется: "add ok"
```

## 🧪 Тестирование

### Запуск всех тестов
```bash
pytest -v
```

### Запуск с отчетом о покрытии
```bash
pytest --cov=src --cov-report=term-missing
```

### Запуск тестов для конкретного модуля
```bash
pytest tests/test_generators.py -v
pytest tests/test_masks.py -v
pytest tests/test_widget.py -v
pytest tests/test_processing.py -v
pytest tests/test_decorators.py -v
```

### Статистика покрытия (98%)
| Модуль          | Строк   | Пропущено | Покрытие |
|-----------------|---------|-----------|----------|
| `__init__.py`   | 5       | 0         | 100%     |
| `decorators.py` | 24      | 0         | 100%     |
| `generators.py` | 24      | 0         | 100%     |
| `masks.py`      | 45      | 0         | 100%     |
| `processing.py` | 8       | 0         | 100%     |
| `widget.py`     | 25      | 2         | 92%      |
| **ИТОГО**       | **131** | **2**     | **98%**  |

### Генерация HTML-отчета
```bash
pytest --cov=src --cov-report=html
```
Откройте `htmlcov/index.html` в браузере

## 🔧 Инструменты качества кода

В проекте используются следующие линтеры и форматтеры:

| Инструмент | Тип        | Назначение                    |
|------------|------------|-------------------------------|
| flake8     | Линтер     | Проверка стиля кода (PEP8)    |
| mypy       | Линтер     | Статическая проверка типов    |
| black      | Форматтер  | Автоматическое форматирование |
| isort      | Форматтер  | Сортировка импортов           |
| pytest     | Тестер     | Запуск тестов                 |
| pytest-cov | Измеритель | Оценка покрытия кода          |

### Запуск проверок
```bash
# Линтеры
flake8 src/ tests/
mypy src/

# Форматтеры (проверка)
black src/ tests/ --check
isort src/ tests/ --check-only

# Форматтеры (исправление)
black src/ tests/
isort src/ tests/
```

## 📁 Структура проекта

```
pythonProject_Masker/
├── htmlcov/                # Отчет о покрытии тестами
├── src/                    # Исходный код
│   ├── __init__.py         # Экспорт функций
│   ├── masks.py            # Маскировка карт/счетов
│   ├── processing.py       # Фильтрация и сортировка транзакций
│   ├── widget.py           # Обработка строк карт/счетов
│   ├── generators.py       # Генераторы для работы с транзакциями
│   └── decorators.py       # Декораторы для логирования
├── tests/                  # Тесты
│   ├── __init__.py
│   ├── test_masks.py       # Тесты для masks.py
│   ├── test_widget.py      # Тесты для widget.py
│   ├── test_processing.py  # Тесты для processing.py
│   ├── test_generators.py  # Тесты для generators.py
│   └── test_decorators.py  # Тесты для decorators.py
├── .flake8                 # Конфигурация flake8
├── .gitignore              # Игнорируемые файлы
├── .coverage               # Данные о покрытии
├── main.py                 # Точка входа
├── pyproject.toml          # Конфигурация проекта
├── poetry.lock             # Зависимости poetry
├── requirements.txt        # Зависимости pip
└── README.md               # Документация
```

## 📄 Лицензия

Этот проект лицензирован по [лицензии MIT].

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку (`git checkout -b feature/amazing-feature`)
3. Закоммитьте изменения (`git commit -m 'Add amazing feature'`)
4. Запушьте ветку (`git push origin feature/amazing-feature`)
5. Создайте Pull Request

## 📞 Контакты

Автор: [bezza8418](https://github.com/bezza8418)

---

*Примечание: Проект разработан в учебных целях для демонстрации навыков тестирования, типизации и работы с финансовыми данными.*