# Python Project Masker

Проект для маскирования банковских реквизитов с полным покрытием тестами.

## 📋 Описание

Проект предоставляет функционал для маскировки:
- Номеров банковских карт
- Номеров банковских счетов  
- Персональных финансовых данных
- Форматирования дат

## 📁 Структура проекта
pythonProject_Masker/
├── src/ # Исходный код
│ ├── init.py # Экспорт функций
│ ├── masks.py # Маскировка карт/счетов
│ ├── processing.py # Фильтрация и сортировка транзакций
│ └── widget.py # Обработка строк карт/счетов
├── tests/ # Тесты
│ ├── init.py
│ ├── test_masks.py # Тесты для masks.py
│ ├── test_widget.py # Тесты для widget.py
│ └── test_processing.py # Тесты для processing.py
├── pyproject.toml # Конфигурация проекта
└── README.md # Документация


## 🚀 Быстрый старт

### Установка

# Клонирование репозитория
git clone https://github.com/bezza8418/pythonProject_Masker
cd pythonProject_Masker

# Установка зависимостей
poetry install

# Использование
from src.masks import get_mask_card_number, get_mask_account
from src.widget import mask_account_card, get_date
from src.processing import filter_by_state, sort_by_date

### Маскировка номера карты
card_masked = get_mask_card_number("7000792289606361")
print(card_masked)  # 7000 79** **** 6361

### Маскировка номера счета
account_masked = get_mask_account("73654108430135874305")
print(account_masked)  # **4305

### Обработка строки с картой/счетом
result = mask_account_card("Счет 73654108430135874305")
print(result)  # Счет **4305

### Форматирование даты
date_formatted = get_date("2024-03-11T02:26:18.671407")
print(date_formatted)  # 11.03.2024

# 🧪 Тестирование
Проект имеет полное тестовое покрытие с использованием современных инструментов тестирования.

Статистика тестирования
Всего тестов: 45

Процент прохождения: 100%

Покрытие кода: 98%

Требуемое покрытие: ≥80%

### Запуск всех тестов
poetry run pytest -v

### Запуск с отчетом о покрытии
poetry run pytest --cov=src --cov-report=term-missing

### Запуск с минимальным покрытием 80%
poetry run pytest --cov=src --cov-fail-under=80

### Запуск тестов для конкретного модуля
poetry run pytest tests/test_masks.py -v
poetry run pytest tests/test_widget.py -v
poetry run pytest tests/test_processing.py -v

# 📊 Отчеты о покрытии
Для генерации HTML-отчета о покрытии:

poetry run pytest --cov=src --cov-report=html
Отчет будет сгенерирован в папке htmlcov/. Откройте index.html в браузере для просмотра детальной информации о покрытии.

# 🛠️ Разработка
### Установка инструментов разработки
poetry add --dev pytest pytest-cov mypy black flake8 isort
Проверка кода перед коммитом

# Запуск всех проверок
poetry run pytest --cov=src --cov-fail-under=80
poetry run mypy src/
poetry run black src/ tests/ --check
poetry run flake8 src/ tests/
poetry run isort src/ tests/ --check-only
Автоматическое форматирование
bash
poetry run black src/ tests/
poetry run isort src/ tests/
# 📝 Документация функций
### Подробная документация доступна в docstrings каждой функции. Для просмотра:

help(get_mask_card_number)
help(mask_account_card)
help(filter_by_state)

# 📄 Лицензия
Проект распространяется под лицензией MIT.
