"""Тесты для модуля generators."""

# from typing import Dict, List, Any
from typing import Any, Dict, List, Optional, Union

import pytest

from src.generators import (
    card_number_generator,
    filter_by_currency,
    transaction_descriptions,
)


@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    """Фикстура с тестовыми транзакциями."""
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {"name": "руб.", "code": "RUB"},
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160",
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {
                "amount": "56883.54",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229",
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {
                "amount": "67314.70",
                "currency": {"name": "руб.", "code": "RUB"},
            },
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657",
        },
    ]


@pytest.fixture
def empty_transactions() -> List:
    """Фикстура с пустым списком транзакций."""
    return []


@pytest.fixture
# def invalid_transactions() -> List[Dict[str, Any]]:
def invalid_transactions() -> List[Optional[Union[Dict[str, Any], str]]]:
    """Фикстура с транзакциями некорректной структуры."""
    return [
        {"id": 1, "description": "Тест"},  # Нет operationAmount
        {"id": 2, "operationAmount": {}},  # Пустой operationAmount
        {"id": 3, "operationAmount": {"currency": {}}},  # Пустая валюта
        None,  # None вместо словаря
        "not a dict",  # Строка вместо словаря
    ]


class TestFilterByCurrency:
    """Тесты для функции filter_by_currency."""

    def test_filter_by_currency_usd(self, sample_transactions):
        """Тест фильтрации транзакций по USD."""
        usd_transactions = list(filter_by_currency(sample_transactions, "USD"))

        assert len(usd_transactions) == 3
        for transaction in usd_transactions:
            currency_code = transaction["operationAmount"]["currency"]["code"]
            assert currency_code == "USD"

    def test_filter_by_currency_rub(self, sample_transactions):
        """Тест фильтрации транзакций по RUB."""
        rub_transactions = list(filter_by_currency(sample_transactions, "RUB"))

        assert len(rub_transactions) == 2
        for transaction in rub_transactions:
            currency_code = transaction["operationAmount"]["currency"]["code"]
            assert currency_code == "RUB"

    def test_filter_by_currency_no_matches(self, sample_transactions):
        """Тест фильтрации, когда нет транзакций с указанной валютой."""
        eur_transactions = list(filter_by_currency(sample_transactions, "EUR"))
        assert eur_transactions == []

    def test_filter_by_currency_empty_list(self, empty_transactions):
        """Тест фильтрации пустого списка."""
        result = list(filter_by_currency(empty_transactions, "USD"))
        assert result == []

    def test_filter_by_currency_invalid_transactions(self, invalid_transactions):
        """Тест фильтрации с некорректными транзакциями."""
        # Должен просто пропустить некорректные и не вызвать ошибку
        result = list(filter_by_currency(invalid_transactions, "USD"))
        assert result == []

    @pytest.mark.parametrize(
        "currency, expected_count",
        [
            ("USD", 3),
            ("RUB", 2),
            ("EUR", 0),
            ("", 0),
        ],
    )
    def test_filter_by_currency_parametrized(
        self, sample_transactions, currency, expected_count
    ):
        """Параметризованный тест фильтрации."""
        result = list(filter_by_currency(sample_transactions, currency))
        assert len(result) == expected_count

    def test_filter_by_currency_iterator(self, sample_transactions):
        """Тест, что функция возвращает итератор."""
        result = filter_by_currency(sample_transactions, "USD")

        # Проверяем, что это итератор
        assert hasattr(result, "__iter__")
        assert hasattr(result, "__next__")

        # Проверяем, что можно получить элементы по одному
        first = next(result)
        assert first["id"] == 939719570

        second = next(result)
        assert second["id"] == 142264268


class TestTransactionDescriptions:
    """Тесты для функции transaction_descriptions."""

    def test_transaction_descriptions_basic(self, sample_transactions):
        """Базовый тест получения описаний."""
        descriptions = list(transaction_descriptions(sample_transactions))

        expected = [
            "Перевод организации",
            "Перевод со счета на счет",
            "Перевод со счета на счет",
            "Перевод с карты на карту",
            "Перевод организации",
        ]
        assert descriptions == expected

    def test_transaction_descriptions_empty_list(self, empty_transactions):
        """Тест с пустым списком."""
        descriptions = list(transaction_descriptions(empty_transactions))
        assert descriptions == []

    def test_transaction_descriptions_invalid_transactions(self, invalid_transactions):
        """Тест с некорректными транзакциями."""
        descriptions = list(transaction_descriptions(invalid_transactions))
        # Должен вернуть только описание от первой валидной транзакции
        assert descriptions == ["Тест"]

    def test_transaction_descriptions_iterator(self, sample_transactions):
        """Тест, что функция возвращает итератор."""
        result = transaction_descriptions(sample_transactions)

        assert hasattr(result, "__iter__")
        assert hasattr(result, "__next__")

        first = next(result)
        assert first == "Перевод организации"

        second = next(result)
        assert second == "Перевод со счета на счет"

    def test_transaction_descriptions_no_description(self):
        """Тест транзакций без описания."""
        transactions = [
            {"id": 1},  # Нет поля description
            {"id": 2, "description": ""},  # Пустое описание
            {"id": 3, "description": None},  # None
            {"id": 4, "description": "Есть описание"},
        ]

        descriptions = list(transaction_descriptions(transactions))
        assert descriptions == ["Есть описание"]


class TestCardNumberGenerator:
    """Тесты для генератора card_number_generator."""

    def test_card_number_generator_basic(self):
        """Базовый тест генерации номеров карт."""
        cards = list(card_number_generator(1, 5))

        expected = [
            "0000 0000 0000 0001",
            "0000 0000 0000 0002",
            "0000 0000 0000 0003",
            "0000 0000 0000 0004",
            "0000 0000 0000 0005",
        ]
        assert cards == expected

    def test_card_number_generator_single_number(self):
        """Тест генерации одного номера."""
        cards = list(card_number_generator(42, 42))
        assert cards == ["0000 0000 0000 0042"]

    def test_card_number_generator_start_end_equal(self):
        """Тест, когда начальное значение равно конечному."""
        cards = list(card_number_generator(100, 100))
        assert cards == ["0000 0000 0000 0100"]

    def test_card_number_generator_large_numbers(self):
        """Тест с большими числами."""
        cards = list(card_number_generator(9999999999999995, 9999999999999999))

        expected = [
            "9999 9999 9999 9995",
            "9999 9999 9999 9996",
            "9999 9999 9999 9997",
            "9999 9999 9999 9998",
            "9999 9999 9999 9999",
        ]
        assert cards == expected

    def test_card_number_generator_format(self):
        """Тест формата номеров карт."""
        cards = list(card_number_generator(1234567890123456, 1234567890123456))

        # Проверяем формат XXXX XXXX XXXX XXXX
        card = cards[0]
        assert len(card) == 19  # 16 цифр + 3 пробела
        assert card.count(" ") == 3

        parts = card.split()
        assert len(parts) == 4
        assert all(len(part) == 4 for part in parts)
        assert all(part.isdigit() for part in parts)

    def test_card_number_generator_range(self):
        """Тест генерации в заданном диапазоне."""
        start, end = 10, 20
        cards = list(card_number_generator(start, end))

        assert len(cards) == end - start + 1

        # Проверяем, что номера идут по порядку
        for i, card in enumerate(cards):
            expected_num = start + i
            expected_str = str(expected_num).zfill(16)
            expected_formatted = f"{expected_str[:4]} {expected_str[4:8]} {expected_str[8:12]} {expected_str[12:16]}"
            assert card == expected_formatted

    def test_card_number_generator_invalid_range(self):
        """Тест с некорректным диапазоном."""
        # start > end должен вернуть пустой список
        cards = list(card_number_generator(10, 5))
        assert cards == []

    @pytest.mark.parametrize(
        "start, end, expected_count",
        [
            (1, 1, 1),
            (1, 10, 10),
            (100, 200, 101),
            (1000, 1005, 6),
        ],
    )
    def test_card_number_generator_parametrized(self, start, end, expected_count):
        """Параметризованный тест генератора."""
        cards = list(card_number_generator(start, end))
        assert len(cards) == expected_count

    def test_card_number_generator_zero_start(self):
        """Тест с началом от 0."""
        cards = list(card_number_generator(0, 2))
        expected = [
            "0000 0000 0000 0000",
            "0000 0000 0000 0001",
            "0000 0000 0000 0002",
        ]
        assert cards == expected
