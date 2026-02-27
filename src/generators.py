"""Модуль с генераторами для обработки транзакций."""

from typing import List, Dict, Iterator

def filter_by_currency(
    transactions: List[Dict], currency: str = "USD"
) -> Iterator[Dict]:
    """
    Фильтрует транзакции по валюте.

    Args:
        transactions: Список словарей с транзакциями
        currency: Код валюты для фильтрации (по умолчанию USD)

    Yields:
        Транзакции с указанной валютой
    """
    for transaction in transactions:
        try:
            operation_amount = transaction.get("operationAmount", {})
            currency_info = operation_amount.get("currency", {})
            transaction_currency = currency_info.get("code")

            if transaction_currency == currency:
                yield transaction
        except (KeyError, AttributeError, TypeError):
            # Пропускаем транзакции с некорректной структурой
            continue


from typing import List, Dict, Generator

def transaction_descriptions(transactions: List[Dict]) -> Generator[str, None, None]:
    """
    Возвращает описания транзакций по очереди.

    Args:
        transactions: Список словарей с транзакциями

    Yields:
        Описание каждой транзакции
    """
    for transaction in transactions:
        try:
            description = transaction.get("description", "")
            if description:
                yield description
        except (KeyError, AttributeError, TypeError):  # Правильно: скобки
            continue


def card_number_generator(start: int, end: int) -> Generator[str, None, None]:
    """
    Генерирует номера банковских карт в заданном диапазоне.

    Args:
        start: Начальное значение (от 1 до 9999999999999999)
        end: Конечное значение (от 1 до 9999999999999999)

    Yields:
        Номер карты в формате "XXXX XXXX XXXX XXXX"
    """
    for number in range(start, end + 1):
        # Форматируем номер с ведущими нулями до 16 цифр
        number_str = str(number).zfill(16)
        # Разбиваем на группы по 4 цифры
        formatted = (
            f"{number_str[:4]} {number_str[4:8]} {number_str[8:12]} {number_str[12:16]}"
        )
        yield formatted
