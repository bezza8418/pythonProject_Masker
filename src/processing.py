from typing import List, Dict
from datetime import datetime


def filter_by_state(
    transactions: List[Dict],
    state: str = "EXECUTED"
) -> List[Dict]:
    """
    Фильтр списка транзакций по значению ключа 'state'.
    """
    return [
        transaction for transaction in transactions
        if transaction.get("state") == state
    ]


def sort_by_date(
    transactions: List[Dict],
    reverse: bool = True
) -> List[Dict]:
    """
    Сортирует список транзакций по дате (ключ 'date').
    """
    def parse_date(date_str: str) -> datetime:
        return datetime.fromisoformat(date_str.replace("Z", "+00:00"))

    return sorted(
        transactions,
        key=lambda x: parse_date(x.get("date", "")),
        reverse=reverse
    )

