"""Модуль для маскирования банковских реквизитов."""

from typing import Any, Dict, List, Union

from src.logger import setup_logger

# Настраиваем логер для модуля masks
logger = setup_logger(__name__, 'masks.log')


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
    logger.info(f"Начало маскировки номера карты: {card_number[:4]}***")

    # Удаляем все пробелы из номера
    digits_only = "".join(filter(lambda x: x.isdigit(), card_number))

    # Проверяем, что номер содержит 16 цифр
    if len(digits_only) != 16:
        logger.error(f"Неверная длина номера карты: {len(digits_only)}")
        raise ValueError("Номер карты должен содержать 16 цифр")

    # Форматируем: ХХХХ ХХ** **** ХХХХ
    masked = f"{digits_only[:4]} {digits_only[4:6]}** **** {digits_only[12:]}"

    logger.info(f"Номер карты успешно замаскирован: {masked}")
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
    logger.info(f"Начало маскировки номера счета: {account_number[:4]}***")

    # Удаляем все нецифровые символы
    digits_only = "".join(filter(lambda x: x.isdigit(), account_number))

    # Проверяем, что номер содержит 20 цифр
    if len(digits_only) != 20:
        logger.error(f"Неверная длина номера счета: {len(digits_only)}")
        raise ValueError("Номер счета должен содержать 20 цифр")

    # Показываем только последние 4 цифры
    masked = f"**{digits_only[-4:]}"

    logger.info(f"Номер счета успешно замаскирован: {masked}")
    return masked


def mask_personal_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Главная функция маскировки персональных данных.
    Использует уже существующие функции маскировки из проекта.
    """
    logger.info(f"Начало маскировки персональных данных. Ключи: {list(data.keys())}")

    if not data:
        logger.warning("Получен пустой словарь данных")
        return {}

    # Создаем копию, чтобы не изменять оригинальные данные
    result = data.copy()

    # Маскируем номера карт для всех возможных названий полей
    card_fields = [
        "card",
        "card_number",
        "credit_card",
        "debit_card",
        "bank_card",
        "payment_card",
        "cardNumber",
    ]

    masked_count = 0
    for field in card_fields:
        if field in result:
            value = result[field]
            if value is not None and str(value).strip():
                try:
                    result[field] = get_mask_card_number(str(value))
                    masked_count += 1
                    logger.debug(f"Замаскировано поле карты: {field}")
                except ValueError as e:
                    logger.error(f"Ошибка маскировки поля {field}: {e}")
                    result[f"{field}_error"] = "Неверный номер карты"

    # Маскируем номера счетов для всех возможных названий полей
    account_fields = [
        "account",
        "account_number",
        "bank_account",
        "savings_account",
        "current_account",
        "accountNumber",
    ]

    for field in account_fields:
        if field in result:
            value = result[field]
            if value is not None and str(value).strip():
                try:
                    result[field] = get_mask_account(str(value))
                    masked_count += 1
                    logger.debug(f"Замаскировано поле счета: {field}")
                except ValueError as e:
                    logger.error(f"Ошибка маскировки поля {field}: {e}")
                    result[f"{field}_error"] = "Неверный номер счета"

    logger.info(f"Маскировка завершена. Замаскировано полей: {masked_count}")
    return result


def process_user_data(users_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Функция обработки списка пользователей с маскировкой данных.
    """
    logger.info(f"Начало обработки списка пользователей. Количество: {len(users_data)}")

    result = [mask_personal_data(user) for user in users_data]

    logger.info(f"Обработка завершена. Обработано пользователей: {len(result)}")
    return result


def mask_financial_info(info_type: str, info_value: Union[str, int]) -> str:
    """
    Универсальная функция для маскировки финансовой информации
    """
    logger.info(f"Маскировка финансовой информации. Тип: {info_type}")

    value_str = str(info_value)
    if info_type.lower() in ["card", "credit_card", "debit_card"]:
        result = get_mask_card_number(value_str)
        logger.info("Финансовая информация (карта) замаскирована")
        return result
    elif info_type.lower() in ["account", "bank_account"]:
        result = get_mask_account(value_str)
        logger.info("Финансовая информация (счет) замаскирована")
        return result
    else:
        logger.error(f"Неизвестный тип информации для маскировки: {info_type}")
        raise ValueError(f"Неизвестный тип информации: {info_type}")
