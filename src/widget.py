from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(account_info: str) -> str:
    """
    Функция обрабатывающая информацию о картах и счетах.
    Входной аргумент: строка, содержащая тип и номер карты или счета.
    Выход функции: строка с замаскированным номером.
    """
    # Разделяем на тип и номер
    parts = account_info.rsplit(" ", 1)
    if len(parts) != 2:
        return account_info
    acc_type, number = parts[0], parts[1]
    # Очищаем номер от пробелов и других нецифровых символов
    clean_number = ""
    for char in number:
        if char.isdigit():
            clean_number += char
    # Проверяем, это счет или карта
    if acc_type.lower() in ["счет", "account"]:
        try:
            # Используем функцию get_mask_account из mask.py
            masked_number = get_mask_account(clean_number)
            return f"{acc_type} {masked_number}"
        except ValueError as e:
            # Если номер некорректен, возвращаем оригинал с пометкой
            return f"{acc_type} {number} (ошибка: {str(e)})"
    else:
        # Это карта (Visa, MasterCard, МИР и т.д.)
        try:
            # Используем функцию get_mask_card_number из mask.py
            masked_number = get_mask_card_number(clean_number)
            return f"{acc_type} {masked_number}"
        except ValueError as e:
            # Если номер некорректен, возвращаем оригинал с пометкой
            return f"{acc_type} {number} (ошибка: {str(e)})"


def get_date(date_string: str) -> str:
    """
    Функция, которая принимает на вход строку с датой в формате
    "2024-03-11T02:26:18.671407"
    и возвращает строку с датой в формате "ДД.ММ.ГГГГ"
    """
    # Разделяем дату и время
    date_part = date_string.split("T")[0]

    # Разделяем год, месяц, день
    year, month, day = date_part.split("-")

    # Форматируем в ДД.ММ.ГГГГ
    return f"{day}.{month}.{year}"
