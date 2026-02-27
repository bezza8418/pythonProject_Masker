"""
Модуль для работы с внешними API для конвертации валют.
"""

import os
from typing import Union

import requests
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Получаем API ключ из переменных окружения
API_KEY = os.getenv("EXCHANGE_RATES_API_KEY")
API_URL = "https://api.apilayer.com/exchangerates_data/latest"


def get_exchange_rate(base_currency: str, target_currency: str = "RUB") -> float:
    """
    Получает текущий курс обмена валют через внешнее API.

    Args:
        base_currency: Базовая валюта (например, USD, EUR)
        target_currency: Целевая валюта (по умолчанию RUB)

    Returns:
        float: Курс обмена

    Raises:
        Exception: При ошибке запроса к API или отсутствии API ключа
    """
    if not API_KEY:
        raise ValueError("API ключ не найден. Проверьте файл .env")

    headers = {"apikey": API_KEY}

    params = {"base": base_currency, "symbols": target_currency}

    try:
        response = requests.get(API_URL, headers=headers, params=params)
        response.raise_for_status()

        data = response.json()

        if not data.get("success", False):
            raise Exception(
                f"API вернул ошибку: {data.get('error', {}).get('info', 'Неизвестная ошибка')}"
            )

        rates = data.get("rates", {})
        rate = rates.get(target_currency)

        if rate is None:
            raise Exception(f"Не удалось получить курс для {target_currency}")

        return float(rate)

    except requests.RequestException as e:
        raise Exception(f"Ошибка при запросе к API: {str(e)}")


def convert_amount(amount: Union[str, float, int], from_currency: str) -> float:
    """
    Конвертирует сумму в рубли.

    Args:
        amount: Сумма для конвертации
        from_currency: Валюта исходной суммы (USD, EUR или RUB)

    Returns:
        float: Сумма в рублях
    """
    # Преобразуем сумму в float
    try:
        amount_float = float(amount)
    except (ValueError, TypeError):
        raise ValueError(f"Некорректная сумма: {amount}")

    # Если валюта уже рубли, возвращаем как есть
    if from_currency.upper() == "RUB":
        return amount_float

    # Для USD и EUR получаем курс и конвертируем
    if from_currency.upper() in ["USD", "EUR"]:
        try:
            rate = get_exchange_rate(from_currency.upper())
            return round(amount_float * rate, 2)
        except Exception as e:
            raise Exception(f"Ошибка конвертации {from_currency} в RUB: {str(e)}")

    # Для других валют выбрасываем исключение
    raise ValueError(f"Неподдерживаемая валюта для конвертации: {from_currency}")


def get_transaction_amount_in_rub(transaction: dict) -> float:
    """
    Принимает на вход транзакцию и возвращает сумму транзакции в рублях.

    Args:
        transaction: Словарь с данными о транзакции

    Returns:
        float: Сумма транзакции в рублях

    Raises:
        ValueError: При некорректной структуре транзакции
        Exception: При ошибках конвертации валют
    """
    try:
        # Проверяем наличие operationAmount
        if "operationAmount" not in transaction:
            raise ValueError(
                "Некорректная структура транзакции: отсутствует operationAmount"
            )

        operation_amount = transaction.get("operationAmount", {})

        # Проверяем наличие amount
        amount = operation_amount.get("amount")
        if amount is None:
            raise ValueError("Некорректная структура транзакции: отсутствует сумма")

        # Проверяем наличие currency
        currency_info = operation_amount.get("currency", {})
        if not currency_info:
            raise ValueError(
                "Некорректная структура транзакции: отсутствует информация о валюте"
            )

        currency_code = currency_info.get("code", "RUB")

        # Пытаемся конвертировать сумму
        try:
            return convert_amount(amount, currency_code)
        except Exception as e:
            # Для ошибок конвертации используем Exception с русским сообщением
            raise Exception(f"Ошибка конвертации: {str(e)}")

    except (KeyError, AttributeError, TypeError) as e:
        raise ValueError(f"Некорректная структура транзакции: {str(e)}")