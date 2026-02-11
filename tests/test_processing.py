from typing import Any, Dict, List

import pytest

from src.processing import filter_by_state, sort_by_date


# Фикстуры для test_processing.py
@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    """Фикстура с тестовыми транзакциями."""
    return [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2024-03-11T02:26:18.671407",
            "amount": "100.00",
            "currency": "RUB",
            "description": "Пополнение счета",
            "from": "Счет 73654108430135874305",
            "to": "Карта 7000792289606361",
        },
        {
            "id": 2,
            "state": "PENDING",
            "date": "2024-03-10T15:30:00.000000",
            "amount": "50.00",
            "currency": "USD",
            "description": "Оплата услуг",
            "from": "Карта 5555555555554444",
            "to": "Счет 40817810099910004321",
        },
        {
            "id": 3,
            "state": "EXECUTED",
            "date": "2024-03-09T10:15:45.123456",
            "amount": "200.00",
            "currency": "EUR",
            "description": "Перевод",
            "from": "Счет 12345678901234567890",
            "to": "Счет 73654108430135874305",
        },
        {
            "id": 4,
            "state": "CANCELED",
            "date": "2024-03-08T20:45:30.987654",
            "amount": "75.50",
            "currency": "RUB",
            "description": "Возврат",
            "from": "Карта 4111111111111111",
            "to": "Карта 1234567890123456",
        },
        {
            "id": 5,
            "state": "EXECUTED",
            "date": "2024-03-07T08:00:00.000000",
            "amount": "150.00",
            "currency": "RUB",
            "description": "Покупка",
        },
    ]


class TestFilterByState:
    """Тесты для функции filter_by_state."""

    @pytest.mark.parametrize(
        "state, expected_count",
        [
            ("EXECUTED", 3),
            ("PENDING", 1),
            ("CANCELED", 1),
            ("UNKNOWN", 0),
        ],
    )
    def test_filter_by_state(
        self, sample_transactions: List[Dict[str, Any]], state: str, expected_count: int
    ) -> None:
        """Тестирование фильтрации по различным статусам."""
        result = filter_by_state(sample_transactions, state)
        assert len(result) == expected_count

        # Проверяем, что все транзакции имеют нужный статус
        for transaction in result:
            assert transaction["state"] == state

    def test_filter_by_state_default(
        self, sample_transactions: List[Dict[str, Any]]
    ) -> None:
        """Тестирование фильтрации со значением по умолчанию."""
        result = filter_by_state(sample_transactions)  # По умолчанию "EXECUTED"
        assert len(result) == 3

        for transaction in result:
            assert transaction["state"] == "EXECUTED"

    def test_filter_by_state_empty_list(self) -> None:
        """Тестирование фильтрации пустого списка."""
        result = filter_by_state([], "EXECUTED")
        assert result == []

    def test_filter_by_state_no_state_field(self) -> None:
        """Тестирование фильтрации транзакций без поля state."""
        transactions = [
            {"id": 1, "amount": "100"},
            {"id": 2, "state": "EXECUTED", "amount": "200"},
            {"id": 3, "amount": "300"},
        ]

        result = filter_by_state(transactions, "EXECUTED")
        assert len(result) == 1
        assert result[0]["id"] == 2


class TestSortByDate:
    """Тесты для функции sort_by_date."""

    def test_sort_by_date_descending(
        self, sample_transactions: List[Dict[str, Any]]
    ) -> None:
        """Тестирование сортировки по убыванию даты (по умолчанию)."""
        result = sort_by_date(sample_transactions)

        # Проверяем, что список отсортирован по убыванию даты
        dates = [transaction["date"] for transaction in result]
        assert dates == sorted(dates, reverse=True)

        # Первая транзакция должна быть самой новой
        assert result[0]["date"] == "2024-03-11T02:26:18.671407"
        assert result[0]["id"] == 1

        # Последняя транзакция должна быть самой старой
        assert result[-1]["date"] == "2024-03-07T08:00:00.000000"
        assert result[-1]["id"] == 5

    def test_sort_by_date_ascending(
        self, sample_transactions: List[Dict[str, Any]]
    ) -> None:
        """Тестирование сортировки по возрастанию даты."""
        result = sort_by_date(sample_transactions, reverse=False)

        # Проверяем, что список отсортирован по возрастанию даты
        dates = [transaction["date"] for transaction in result]
        assert dates == sorted(dates, reverse=False)

        # Первая транзакция должна быть самой старой
        assert result[0]["date"] == "2024-03-07T08:00:00.000000"
        assert result[0]["id"] == 5

        # Последняя транзакция должна быть самой новой
        assert result[-1]["date"] == "2024-03-11T02:26:18.671407"
        assert result[-1]["id"] == 1

    def test_sort_by_date_empty_list(self) -> None:
        """Тестирование сортировки пустого списка."""
        result = sort_by_date([])
        assert result == []

    def test_sort_by_date_single_element(self) -> None:
        """Тестирование сортировки списка с одним элементом."""
        transactions = [
            {
                "id": 1,
                "date": "2024-03-11T10:00:00.000000",
                "amount": "100",
                "state": "EXECUTED",
            }
        ]

        result = sort_by_date(transactions)
        assert len(result) == 1
        assert result[0]["id"] == 1

    def test_sort_by_date_invalid_format(self) -> None:
        """Тестирование сортировки с неверным форматом даты."""
        transactions = [
            {"id": 1, "date": "2024/03/11", "amount": "100", "state": "EXECUTED"},
        ]

        with pytest.raises(ValueError):
            sort_by_date(transactions)
