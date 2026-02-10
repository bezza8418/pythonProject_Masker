"""Модуль для маскирования банковских реквизитов."""

from typing import Any, Dict, List, Union


def get_mask_card_number(card_number: str) -> str:
    """
    Функция принимает на вход номер карты и возвращает ее маску.
    Номер карты замаскирован и отображается в формате XXXX XX** **** XXXX,
    где X — это цифра номера.
    То есть видны первые 6 цифр и последние 4 цифры,
    остальные символы отображаются звездочками, номер разбит по блокам по 4 цифры,
    разделенным пробелами.
    Пример работы функции:
    входной аргумент: 7000792289606361
    выход функции: 7000 79** **** 6361
    """
    # Удаляем все пробелы из номера
    digits_only = "".join(filter(lambda x: x.isdigit(), card_number))

    # Проверяем, что номер содержит 16 цифр
    if len(digits_only) != 16:
        raise ValueError("Номер карты должен содержать 16 цифр")

    # Форматируем: ХХХХ ХХ** **** ХХХХ
    masked = f"{digits_only[:4]} {digits_only[4:6]}** **** {digits_only[12:]}"
    return masked


def get_mask_account(account_number: str) -> str:
    """
    Функция принимает на вход номер счета и возвращает его маску.
    Номер счета замаскирован и отображается в формате **XXXX,
    где X — это цифра номера.
    То есть видны только последние 4 цифры номера, а перед ними — две звездочки.
    Пример работы функции:
    входной аргумент: 73654108430135874305
    выход функции: **4305
    """
    # Удаляем все нецифровые символы
    digits_only = "".join(filter(lambda x: x.isdigit(), account_number))

    # Проверяем, что номер содержит 20 цифр
    if len(digits_only) != 20:
        raise ValueError("Номер счета должен содержать 20 цифр")

    # Показываем только последние 4 цифры
    masked = f"**{digits_only[-4:]}"
    return masked


def mask_personal_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Главная функция маскировки персональных данных.
    Использует уже существующие функции маскировки из проекта.
    """
    # Создаем копию, чтобы не изменять оригинальные данные
    result = data.copy()

    # Список возможных названий полей для карт
    card_fields = ["card", "card_number", "credit_card", "debit_card", "bank_card", "payment_card", "cardNumber"]

    # Список возможных названий полей для счетов
    account_fields = [
        "account",
        "account_number",
        "bank_account",
        "savings_account",
        "current_account",
        "accountNumber",
    ]

    # Маскируем номера карт
    for field in card_fields:
        if field in result[field]:
            try:
                result[field] = get_mask_card_number(str(result[field]))
            except ValueError as e:
                # Если номер не корректен, оставляем как есть или помечаем ошибкой
                result[f"{field}_error"] = str(e)
    # Маскируем номера счетов
    for field in account_fields:
        if field in result and result[field]:
            try:
                result[field] = get_mask_account(str(result[field]))
            except ValueError as e:
                # Если номер не корректен, оставляем как есть или помечаем ошибкой
                result[f"{field}_error"] = str(e)

    return result


def process_user_data(users_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Функция обработки списка пользователей с маскировкой данных.
    """
    return [mask_personal_data(user) for user in users_data]


def mask_financial_info(info_type: str, info_value: Union[str, int]) -> str:
    """
    Универсальная функция для маскировки финансовой информации
    """
    value_str = str(info_value)
    if info_type.lower() in ["card", "credit_card", "debit_card"]:
        return get_mask_card_number(value_str)
    elif info_type.lower() in ["account", "bank_account"]:
        return get_mask_account(value_str)
    else:
        raise ValueError(f"Неизвестный тип информации: {info_type}")
