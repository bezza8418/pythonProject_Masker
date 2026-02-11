import pytest
from src.masks import (
    get_mask_card_number,
    get_mask_account,
    mask_personal_data,
    mask_financial_info,
    process_user_data,
)
from typing import Dict, Any, List


# Фикстуры для test_masks.py
@pytest.fixture
def sample_card_numbers() -> List[str]:
    """Фикстура с тестовыми номерами карт."""
    return [
        "7000792289606361",
        "7000 7922 8960 6361",
        "7000-7922-8960-6361",
        "1234567890123456",
        "5555555555554444",
        "4111111111111111",
    ]


@pytest.fixture
def sample_account_numbers() -> List[str]:
    """Фикстура с тестовыми номерами счетов."""
    return [
        "73654108430135874305",
        "7365 4108 4301 3587 4305",
        "40817810099910004321",
        "12345678901234567890",
    ]


@pytest.fixture
def sample_personal_data() -> List[Dict[str, Any]]:
    """Фикстура с тестовыми персональными данными."""
    return [
        {
            "name": "Иван Иванов",
            "card": "7000792289606361",
            "account": "73654108430135874305",
            "phone": "+7 999 123 45 67",
        },
        {
            "name": "Петр Петров",
            "card_number": "5555555555554444",
            "account_number": "40817810099910004321",
            "email": "petr@example.com",
        },
        {
            "name": "Сидор Сидоров",
            "bank_card": "4111111111111111",
            "bank_account": "12345678901234567890",
            "address": "Москва",
        },
        {
            "name": "Анна Аннова",
            "credit_card": "1234567890123456",
            "savings_account": "11112222333344445555",
        },
    ]


class TestGetMaskCardNumber:
    """Тесты для функции get_mask_card_number."""

    def test_valid_card_numbers(self, sample_card_numbers: List[str]) -> None:
        """Тестирование корректных номеров карт."""
        test_cases = [
            ("7000792289606361", "7000 79** **** 6361"),
            ("1234567890123456", "1234 56** **** 3456"),
            ("5555555555554444", "5555 55** **** 4444"),
            ("4111111111111111", "4111 11** **** 1111"),
        ]

        for card_number, expected in test_cases:
            result = get_mask_card_number(card_number)
            assert result == expected

    @pytest.mark.parametrize("card_number, expected", [
        ("7000 7922 8960 6361", "7000 79** **** 6361"),
        ("7000-7922-8960-6361", "7000 79** **** 6361"),
        ("7000_7922_8960_6361", "7000 79** **** 6361"),
    ])
    def test_card_numbers_with_separators(self, card_number: str, expected: str) -> None:
        """Тестирование номеров карт с разделителями."""
        result = get_mask_card_number(card_number)
        assert result == expected

    @pytest.mark.parametrize("invalid_card_number", [
        "123456789012345",  # 15 цифр
        "12345678901234567",  # 17 цифр
        "1234",  # слишком короткий
        "abcdefghijklmnop",  # не цифры
        "",  # пустая строка
        "1234 5678 9012 345",  # 15 цифр с пробелами
    ])
    def test_invalid_card_numbers(self, invalid_card_number: str) -> None:
        """Тестирование некорректных номеров карт."""
        with pytest.raises(ValueError, match="Номер карты должен содержать 16 цифр"):
            get_mask_card_number(invalid_card_number)

    def test_card_number_with_letters(self) -> None:
        """Тестирование номера карты с буквами."""
        with pytest.raises(ValueError):
            get_mask_card_number("7000ABCD89606361")


class TestGetMaskAccount:
    """Тесты для функции get_mask_account."""

    def test_valid_account_numbers(self, sample_account_numbers: List[str]) -> None:
        """Тестирование корректных номеров счетов."""
        test_cases = [
            ("73654108430135874305", "**4305"),
            ("40817810099910004321", "**4321"),
            ("12345678901234567890", "**7890"),
            ("11112222333344445555", "**5555"),
        ]

        for account_number, expected in test_cases:
            result = get_mask_account(account_number)
            assert result == expected

    @pytest.mark.parametrize("account_number, expected", [
        ("7365 4108 4301 3587 4305", "**4305"),
        ("7365-4108-4301-3587-4305", "**4305"),
        ("4081 7810 0999 1000 4321", "**4321"),
    ])
    def test_account_numbers_with_separators(self, account_number: str, expected: str) -> None:
        """Тестирование номеров счетов с разделителями."""
        result = get_mask_account(account_number)
        assert result == expected

    @pytest.mark.parametrize("invalid_account_number", [
        "1234567890123456789",  # 19 цифр
        "123456789012345678901",  # 21 цифра
        "12345",  # слишком короткий
        "abcdefghijklmnopqrst",  # не цифры
        "",  # пустая строка
        "1234 5678 9012 3456 789",  # 19 цифр с пробелами
    ])
    def test_invalid_account_numbers(self, invalid_account_number: str) -> None:
        """Тестирование некорректных номеров счетов."""
        with pytest.raises(ValueError, match="Номер счета должен содержать 20 цифр"):
            get_mask_account(invalid_account_number)


class TestMaskPersonalData:
    """Тесты для функции mask_personal_data."""

    def test_mask_personal_data_with_card_and_account(self) -> None:
        """Тестирование маскировки данных с картой и счетом."""
        data = {
            "name": "Иван Иванов",
            "card": "7000792289606361",
            "account": "73654108430135874305",
            "phone": "+7 999 123 45 67",
        }

        result = mask_personal_data(data)

        assert result["name"] == "Иван Иванов"
        assert result["card"] == "7000 79** **** 6361"
        assert result["account"] == "**4305"
        assert result["phone"] == "+7 999 123 45 67"

    def test_mask_personal_data_with_various_field_names(self, sample_personal_data: List[Dict[str, Any]]) -> None:
        """Тестирование маскировки данных с различными названиями полей."""
        for data in sample_personal_data:
            result = mask_personal_data(data)

            # Проверяем, что имя не изменилось
            assert result["name"] == data["name"]

            # Проверяем маскировку карты (если есть)
            for card_field in ["card", "card_number", "bank_card", "credit_card"]:
                if card_field in data:
                    assert "**" in result[card_field] or "ошибка" in result.get(f"{card_field}_error", "")

            # Проверяем маскировку счета (если есть)
            for account_field in ["account", "account_number", "bank_account", "savings_account"]:
                if account_field in data:
                    assert result[account_field].startswith("**") or "ошибка" in result.get(f"{account_field}_error",
                                                                                            "")

    def test_mask_personal_data_with_invalid_numbers(self) -> None:
        """Тестирование маскировки данных с некорректными номерами."""
        data = {
            "name": "Тест",
            "card": "12345",  # Неверная длина
            "account": "123",  # Неверная длина
        }

        result = mask_personal_data(data)

        assert "card_error" in result
        assert "account_error" in result
        assert "Номер карты должен содержать 16 цифр" in result["card_error"]
        assert "Номер счета должен содержать 20 цифр" in result["account_error"]

    def test_mask_personal_data_empty(self) -> None:
        """Тестирование маскировки пустых данных."""
        data = {}
        result = mask_personal_data(data)
        assert result == {}

    def test_mask_personal_data_no_financial_info(self) -> None:
        """Тестирование данных без финансовой информации."""
        data = {
            "name": "Иван",
            "age": 30,
            "city": "Москва",
        }
        result = mask_personal_data(data)
        assert result == data


class TestMaskFinancialInfo:
    """Тесты для функции mask_financial_info."""

    @pytest.mark.parametrize("info_type, info_value, expected", [
        ("card", "7000792289606361", "7000 79** **** 6361"),
        ("credit_card", "1234567890123456", "1234 56** **** 3456"),
        ("debit_card", "5555555555554444", "5555 55** **** 4444"),
        ("account", "73654108430135874305", "**4305"),
        ("bank_account", "40817810099910004321", "**4321"),
    ])
    def test_valid_financial_info(self, info_type: str, info_value: str, expected: str) -> None:
        """Тестирование корректной финансовой информации."""
        result = mask_financial_info(info_type, info_value)
        assert result == expected

    @pytest.mark.parametrize("info_type", [
        "unknown_type",
        "invalid",
        "",
        "some_other_type",
    ])
    def test_invalid_info_type(self, info_type: str) -> None:
        """Тестирование некорректного типа информации."""
        with pytest.raises(ValueError, match=f"Неизвестный тип информации: {info_type}"):
            mask_financial_info(info_type, "1234567890123456")


class TestProcessUserData:
    """Тесты для функции process_user_data."""

    def test_process_user_data(self, sample_personal_data: List[Dict[str, Any]]) -> None:
        """Тестирование обработки списка пользователей."""
        result = process_user_data(sample_personal_data)

        assert len(result) == len(sample_personal_data)

        for i, user in enumerate(result):
            original_user = sample_personal_data[i]

            # Проверяем, что нефинансовые поля не изменились
            for field in ["name", "phone", "email", "address"]:
                if field in original_user:
                    assert user[field] == original_user[field]