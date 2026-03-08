"""
Модуль для поиска и категоризации банковских транзакций.
Использует регулярные выражения для гибкого поиска.
"""

import re
from typing import Dict, List


def filter_by_description(transactions: List[Dict], search_string: str) -> List[Dict]:
    """
    Фильтрует транзакции по наличию строки поиска в описании.
    Использует регулярные выражения для регистронезависимого поиска.

    Args:
        transactions: Список словарей с транзакциями
        search_string: Строка для поиска в описании

    Returns:
        Список транзакций, в описании которых найдена искомая строка
    """
    if not transactions or not search_string:
        return []

    # Создаем регистронезависимое регулярное выражение
    pattern = re.compile(re.escape(search_string), re.IGNORECASE)

    result = []
    for transaction in transactions:
        description = transaction.get("description", "")
        if pattern.search(description):
            result.append(transaction)

    return result


def count_by_categories(transactions: List[Dict], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество транзакций в каждой категории.

    Args:
        transactions: Список словарей с транзакциями
        categories: Список категорий для подсчета

    Returns:
        Словарь с количеством транзакций по каждой категории
    """
    result = {category: 0 for category in categories}

    for transaction in transactions:
        description = transaction.get("description", "")
        for category in categories:
            # Регистронезависимый поиск категории в описании
            if re.search(re.escape(category), description, re.IGNORECASE):
                result[category] += 1

    return result
