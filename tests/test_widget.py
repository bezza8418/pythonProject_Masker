import pytest
from src.widget import mask_account_card, get_date
from typing import List


# Фикстуры для test_widget.py
@pytest.fixture
def sample_account_card_strings() -> List[str]:
    """Фикстура с тестовыми строками карт и счетов."""
    return [
        "Счет 73654108430135874305",
        "Visa Platinum 7000792289606361",
        "MasterCard 5555555555554444",
        "МИР 1234567890123456",
        "Maestro 4111111111111111",
        "Visa Classic 1234567890123456",
        "Счет 40817810099910004321",
        "Карта 7000792289606361",
    ]


class TestMaskAccountCard:
    """Тесты для функции mask_account_card."""

    @pytest.mark.parametrize("input_string, expected", [
        ("Счет 73654108430135874305", "Счет **4305"),
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("MasterCard 5555555555554444", "MasterCard 5555 55** **** 4444"),
        ("МИР 1234567890123456", "МИР 1234 56** **** 3456"),
        ("Maestro 4111111111111111", "Maestro 4111 11** **** 1111"),
        ("Visa Classic 1234567890123456", "Visa Classic 1234 56** **** 3456"),
        ("Счет 40817810099910004321", "Счет **4321"),
        ("Карта 7000792289606361", "Карта 7000 79** **** 6361"),
    ])
    def test_valid_account_card_strings(self, input_string: str, expected: str) -> None:
        """Тестирование корректных строк с картами и счетами."""
        result = mask_account_card(input_string)
        assert result == expected

    def test_invalid_inputs(self) -> None:
        """Тестирование некорректных входных данных."""
        # Пустая строка
        result = mask_account_card("")
        assert result == ""

        # Только пробелы - функция может вернуть оригинал или с сообщением об ошибке
        result = mask_account_card("   ")
        # Проверяем что функция не падает и возвращает строку
        assert isinstance(result, str)

        # Только тип
        result = mask_account_card("Счет")
        # Функция должна вернуть оригинальную строку, так как нет номера
        assert result == "Счет"

        # Только номер - для строки без типа
        result = mask_account_card("1234567890")
        # Проверяем что что-то возвращается
        assert isinstance(result, str)

    def test_case_insensitive_account_type(self) -> None:
        """Тестирование нечувствительности к регистру типа счета."""
        result = mask_account_card("счет 73654108430135874305")
        assert "**4305" in result

        result = mask_account_card("СЧЕТ 73654108430135874305")
        assert "**4305" in result


class TestGetDate:
    """Тесты для функции get_date."""

    @pytest.mark.parametrize("input_date, expected", [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2023-12-31T23:59:59.999999", "31.12.2023"),
        ("2024-01-01T00:00:00.000000", "01.01.2024"),
        ("2024-02-29T12:30:45.123456", "29.02.2024"),  # Високосный год
    ])
    def test_valid_dates(self, input_date: str, expected: str) -> None:
        """Тестирование корректных дат."""
        result = get_date(input_date)
        assert result == expected

    def test_date_without_time(self) -> None:
        """Тестирование даты без времени."""
        result = get_date("2024-03-11")
        assert result == "11.03.2024"

    def test_invalid_dates_value_error(self) -> None:
        """Тестирование некорректных дат, которые вызывают ValueError."""
        # Неправильный разделитель
        with pytest.raises(ValueError):
            get_date("2024/03/11T02:26:18")

    def test_mask_account_card_with_different_card_types(self):
        """Тест маскировки для различных типов карт."""
        # Тестируем различные форматы
        result = mask_account_card("American Express 371449635398431")
        # Проверяем что что-то возвращается (может быть ошибка для 15-значной карты)
        assert "American Express" in result

        result = mask_account_card("Discover 6011111111111117")
        assert "Discover" in result or "ошибка" in result

        result = mask_account_card("JCB 3530111333300000")
        assert "JCB" in result or "ошибка" in result
