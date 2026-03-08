"""
Тесты для модуля search.
"""

import pytest

from src.search import count_by_categories, filter_by_description


@pytest.fixture
def sample_transactions():
    """Фикстура с тестовыми транзакциями."""
    return [
        {"id": 1, "description": "Перевод организации", "amount": 100},
        {"id": 2, "description": "Перевод со счета на счет", "amount": 200},
    {"id": 3, "description": "Перевод с карты на карту", "amount": 300},
    {"id": 4, "description": "Оплата услуг", "amount": 400},
    {"id": 5, "description": "Перевод организации", "amount": 500},
    ]

class TestFilterByDescription:
    """Тесты для функции filter_by_description."""

    def test_filter_by_description_found(self, sample_transactions):
        """Тест поиска существующего описания."""
        result = filter_by_description(sample_transactions, "Перевод")
        assert len(result) == 3
        assert all("Перевод" in t["description"] for t in result)

    def test_filter_by_description_case_insensitive(self, sample_transactions):
        """Тест регистронезависимого поиска."""
        result = filter_by_description(sample_transactions, "перевод")
        assert len(result) == 3
        assert all("Перевод" in t["description"] for t in result)

    def test_filter_by_description_not_found(self, sample_transactions):
        """Тест поиска несуществующего описания."""
        result = filter_by_description(sample_transactions, "Космос")
        assert result == []

    def test_filter_by_description_empty_list(self):
        """Тест с пустым списком транзакций."""
        result = filter_by_description([], "Перевод")
        assert result == []

    def test_filter_by_description_empty_string(self, sample_transactions):
        """Тест с пустой строкой поиска."""
        result = filter_by_description(sample_transactions, "")
        assert result == []

    def test_filter_by_description_special_chars(self, sample_transactions):
        """Тест поиска со специальными символами."""
        result = filter_by_description(sample_transactions, "организации")
        assert len(result) == 2

class TestCountByCategories:
    """Тесты для функции count_by_categories."""

    def test_count_by_categories_basic(self, sample_transactions):
        """Тест подсчета по категориям."""
        categories = ["Перевод", "Оплата"]
        result = count_by_categories(sample_transactions, categories)

        assert result["Перевод"] == 3
        assert result["Оплата"] == 1

    def test_count_by_categories_case_insensitive(self, sample_transactions):
        """Тест регистронезависимого подсчета."""
        categories = ["перевод", "оплата"]
        result = count_by_categories(sample_transactions, categories)

        assert result["перевод"] == 3
        assert result["оплата"] == 1

    def test_count_by_categories_empty_list(self):
        """Тест с пустым списком транзакций."""
        categories = ["Перевод", "Оплата"]
        result = count_by_categories([], categories)

        assert result["Перевод"] == 0
        assert result["Оплата"] == 0

    def test_count_by_categories_empty_categories(self, sample_transactions):
        """Тест с пустым списком категорий."""
        result = count_by_categories(sample_transactions, [])
        assert result == {}

    def test_count_by_categories_no_matches(self, sample_transactions):
        """Тест с категориями, которых нет в описаниях."""
        categories = ["Космос", "Еда"]
        result = count_by_categories(sample_transactions, categories)

        assert result["Космос"] == 0
        assert result["Еда"] == 0
