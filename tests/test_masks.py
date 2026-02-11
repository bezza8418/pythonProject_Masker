import pytest
from src.masks import get_mask_card_number, get_mask_account, mask_personal_data


def test_get_mask_card_number_basic():
    """Базовый тест маскировки номера карты."""
    result = get_mask_card_number("7000792289606361")
    assert result == "7000 79** **** 6361"


def test_get_mask_card_number_with_spaces():
    """Тест маскировки номера карты с пробелами."""
    result = get_mask_card_number("7000 7922 8960 6361")
    assert result == "7000 79** **** 6361"


def test_get_mask_card_number_invalid():
    """Тест некорректного номера карты."""
    with pytest.raises(ValueError):
        get_mask_card_number("12345")


def test_get_mask_account_basic():
    """Базовый тест маскировки номера счета."""
    result = get_mask_account("73654108430135874305")
    assert result == "**4305"


def test_get_mask_account_with_spaces():
    """Тест маскировки номера счета с пробелами."""
    result = get_mask_account("7365 4108 4301 3587 4305")
    assert result == "**4305"


def test_get_mask_account_invalid():
    """Тест некорректного номера счета."""
    with pytest.raises(ValueError):
        get_mask_account("12345")


def test_mask_personal_data_basic():
    """Базовый тест маскировки персональных данных."""
    data = {
        "name": "Иван",
        "card": "7000792289606361",
        "account": "73654108430135874305",
    }

    result = mask_personal_data(data)

    assert result["name"] == "Иван"
    assert result["card"] == "7000 79** **** 6361"
    assert result["account"] == "**4305"


def test_mask_personal_data_with_card_number_field():
    """Тест с полем card_number вместо card."""
    data = {
        "name": "Петр",
        "card_number": "5555555555554444",
    }

    result = mask_personal_data(data)
    assert result["card_number"] == "5555 55** **** 4444"


def test_mask_personal_data_empty():
    """Тест пустых данных."""
    assert mask_personal_data({}) == {}


def test_mask_personal_data_no_financial():
    """Тест данных без финансовой информации."""
    data = {"name": "Иван", "age": 30}
    assert mask_personal_data(data) == data


def test_mask_personal_data_with_invalid_card():
    """Тест маскировки с некорректным номером карты."""
    data = {
        "name": "Тест",
        "card": "12345",  # Неверная длина
    }

    result = mask_personal_data(data)
    # Проверяем, что поле card_error добавлено или карта осталась без изменений
    assert "card_error" in result or result["card"] == "12345"


def test_mask_personal_data_with_invalid_account():
    """Тест маскировки с некорректным номером счета."""
    data = {
        "name": "Тест",
        "account": "123",  # Неверная длина
    }

    result = mask_personal_data(data)
    # Проверяем, что поле account_error добавлено или счет остался без изменений
    assert "account_error" in result or result["account"] == "123"


def test_mask_personal_data_with_none_values():
    """Тест маскировки со значениями None."""
    data = {
        "name": "Тест",
        "card": None,
        "account": None,
    }

    result = mask_personal_data(data)
    assert result["name"] == "Тест"
    assert result["card"] is None
    assert result["account"] is None


def test_mask_personal_data_with_empty_strings():
    """Тест маскировки с пустыми строками."""
    data = {
        "name": "Тест",
        "card": "",
        "account": "",
    }

    result = mask_personal_data(data)
    assert result["name"] == "Тест"
    assert result["card"] == ""
    assert result["account"] == ""


def test_mask_financial_info():
    """Тест функции mask_financial_info."""
    from src.masks import mask_financial_info

    # Тест для карты
    result = mask_financial_info("card", "7000792289606361")
    assert result == "7000 79** **** 6361"

    # Тест для счета
    result = mask_financial_info("account", "73654108430135874305")
    assert result == "**4305"

    # Тест для неверного типа
    with pytest.raises(ValueError, match="Неизвестный тип информации"):
        mask_financial_info("invalid", "1234567890123456")


def test_process_user_data():
    """Тест функции process_user_data."""
    from src.masks import process_user_data

    users = [
        {"name": "Иван", "card": "7000792289606361"},
        {"name": "Петр", "account": "73654108430135874305"},
    ]

    result = process_user_data(users)
    assert len(result) == 2
    assert result[0]["name"] == "Иван"
    assert result[1]["name"] == "Петр"