from typing import List

import pytest

from src.widget import mask_account_card, get_date


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


@pytest.fixture
def sample_dates() -> List[str]:
    """Фикстура с тестовыми датами."""
    return [
        "2024-03-11T02:26:18.671407",
        "2023-12-31T23:59:59.999999",
        "2024-01-01T00:00:00.000000",
        "2024-02-29T12:30:45.123456",  # Високосный год
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

    @pytest.mark.parametrize("input_string, expected", [
        ("Счет 7365 4108 4301 3587 4305", "Счет **4305"),
        ("Visa Platinum 7000 7922 8960 6361", "Visa Platinum 7000 79** **** 6361"),
        ("MasterCard 5555-5555-5555-4444", "MasterCard 5555 55** **** 4444"),
    ])
    def test_strings_with_separators(self, input_string: str, expected: str) -> None:
        """Тестирование строк с разделителями в номерах."""
        result = mask_account_card(input_string)
        assert result == expected

    @pytest.mark.parametrize("invalid_input", [
        "Счет",  # только тип
        "1234567890",  # только номер
        "",  # пустая строка
        "   ",  # пробелы
        "Invalid String",  # некорректный формат
        "Счет 123",  # слишком короткий номер счета
        "Карта 12345",  # слишком короткий номер карты
        "Счет abcdefghijklmnopqrst",  # не цифры в счете
        "Карта abcdefghijklmnop",  # не цифры в карте
    ])
    def test_invalid_inputs(self, invalid_input: str) -> None:
        """Тестирование некорректных входных данных."""
        result = mask_account_card(invalid_input)
        # Функция должна вернуть оригинальную строку или строку с пометкой об ошибке
        assert invalid_input in result or "ошибка" in result

    def test_case_insensitive_account_type(self) -> None:
        """Тестирование нечувствительности к регистру типа счета."""
        inputs = ["счет 73654108430135874305", "СЧЕТ 73654108430135874305", "Account 73654108430135874305"]
        expected = "**4305"

        for input_str in inputs:
            result = mask_account_card(input_str)
            assert expected in result

    @pytest.mark.parametrize("input_string", [
        "Счет 7365410843013587430",  # 19 цифр
        "Карта 123456789012345",  # 15 цифр
    ])
    def test_incorrect_length_numbers(self, input_string: str) -> None:
        """Тестирование номеров с некорректной длиной."""
        result = mask_account_card(input_string)
        assert "ошибка" in result


class TestGetDate:
    """Тесты для функции get_date."""

    @pytest.mark.parametrize("input_date, expected", [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2023-12-31T23:59:59.999999", "31.12.2023"),
        ("2024-01-01T00:00:00.000000", "01.01.2024"),
        ("2024-02-29T12:30:45.123456", "29.02.2024"),  # Високосный год
        ("2000-02-29T00:00:00.000000", "29.02.2000"),  # Високосный год 2000
    ])
    def test_valid_dates(self, input_date: str, expected: str) -> None:
        """Тестирование корректных дат."""
        result = get_date(input_date)
        assert result == expected

    def test_date_without_time(self) -> None:
        """Тестирование даты без времени."""
        result = get_date("2024-03-11")
        assert result == "11.03.2024"

    @pytest.mark.parametrize("invalid_date", [
        "2024/03/11T02:26:18",  # неправильный разделитель
        "",  # пустая строка
        "not-a-date",  # не дата
        "2024-13-11T02:26:18",  # неверный месяц
        "2024-02-30T02:26:18",  # неверный день
    ])
    def test_invalid_dates(self, invalid_date: str) -> None:
        """Тестирование некорректных дат."""
        with pytest.raises((ValueError, IndexError)):
            get_date(invalid_date)

    def test_date_with_z_suffix(self) -> None:
        """Тестирование даты с Z-суффиксом."""
        result = get_date("2024-03-11T02:26:18.671407Z")
        assert result == "11.03.2024"

    def test_edge_case_dates(self) -> None:
        """Тестирование граничных случаев с датами."""
        # Минимальная дата
        result = get_date("0001-01-01T00:00:00.000000")
        assert result == "01.01.0001"

        # Максимальная дата (в разумных пределах)
        result = get_date("9999-12-31T23:59:59.999999")
        assert result == "31.12.9999"