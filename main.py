"""
Основной модуль для демонстрации работы функций.
"""

import os
from typing import List, Dict

from src.file_readers import read_csv_file, read_excel_file
from src.processing import filter_by_state, sort_by_date
from src.search import filter_by_description
from src.utils import load_transactions
from src.widget import get_date, mask_account_card

VALID_STATUSES = ["EXECUTED", "CANCELED", "PENDING"]


def get_user_choice(prompt: str, valid_options: List[str] = None) -> str:
    """
    Получает ввод пользователя и проверяет его.

    Args:
        prompt: Приглашение для ввода
        valid_options: Список допустимых вариантов (если есть)

    Returns:
        Введенная строка
    """
    while True:
        user_input = input(prompt).strip()

        if valid_options:
            if user_input.upper() in valid_options:
                return user_input.upper()
            else:
                print(f"\nСтатус операции '{user_input}' недоступен.")
                print(f"Доступные статусы: {', '.join(valid_options)}")
        else:
            return user_input


def get_yes_no(prompt: str) -> bool:
    """
    Получает ответ Да/Нет от пользователя.

    Args:
        prompt: Приглашение для ввода

    Returns:
        True для Да, False для Нет
    """
    while True:
        answer = input(prompt).strip().lower()
        if answer in ["да", "yes", "y", "д"]:
            return True
        elif answer in ["нет", "no", "n", "н"]:
            return False
        else:
            print("Пожалуйста, введите 'Да' или 'Нет'")


def print_transactions(transactions: List[Dict]) -> None:
    """
    Красиво выводит список транзакций.

    Args:
        transactions: Список транзакций
    """
    if not transactions:
        print("\nНе найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print(f"\nВсего банковских операций в выборке: {len(transactions)}\n")

    for transaction in transactions:
        # Форматируем дату
        date_str = transaction.get("date", "")
        if date_str:
            formatted_date = get_date(date_str)
        else:
            formatted_date = "Неизвестная дата"

        # Получаем описание
        description = transaction.get("description", "Неизвестная операция")

        # Форматируем счет/карту отправителя и получателя
        from_info = transaction.get("from", "")
        to_info = transaction.get("to", "")

        if from_info:
            from_masked = mask_account_card(from_info)
        else:
            from_masked = "Неизвестно"

        if to_info:
            to_masked = mask_account_card(to_info)
        else:
            to_masked = "Неизвестно"

        # Получаем сумму и валюту
        operation_amount = transaction.get("operationAmount", {})
        amount = operation_amount.get("amount", "0")
        currency = operation_amount.get("currency", {}).get("code", "RUB")

        print(f"{formatted_date} {description}")
        if from_info:
            print(f"{from_masked} -> {to_masked}")
        else:
            print(f"-> {to_masked}")
        print(f"Сумма: {amount} {currency}\n")


def main():
    """Основная функция для демонстрации работы."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = get_user_choice("Ваш выбор: ")

    # Определяем путь к файлу
    project_root = os.path.dirname(os.path.abspath(__file__))

    if choice == "1":
        print("\nДля обработки выбран JSON-файл.")
        file_path = os.path.join(project_root, "data", "operations.json")
        transactions = load_transactions(file_path)
    elif choice == "2":
        print("\nДля обработки выбран CSV-файл.")
        file_path = os.path.join(project_root, "data", "transactions.csv")
        transactions = read_csv_file(file_path)
    elif choice == "3":
        print("\nДля обработки выбран XLSX-файл.")
        file_path = os.path.join(project_root, "data", "transactions_excel.xlsx")
        transactions = read_excel_file(file_path)
    else:
        print("Неверный выбор. Завершение программы.")
        return

    if not transactions:
        print("Не удалось загрузить транзакции. Проверьте наличие файлов в папке data/")
        return

    # Фильтрация по статусу
    print("\nВведите статус, по которому необходимо выполнить фильтрацию.")
    print(f"Доступные для фильтровки статусы: {', '.join(VALID_STATUSES)}")

    status = get_user_choice("Ваш выбор: ", VALID_STATUSES)
    filtered_by_status = filter_by_state(transactions, status)
    print(f"\nОперации отфильтрованы по статусу \"{status}\"")

    # Сортировка по дате
    if get_yes_no("\nОтсортировать операции по дате? Да/Нет: "):
        sort_order = get_user_choice("Отсортировать по возрастанию или по убыванию? ",
                                     ["ПО ВОЗРАСТАНИЮ", "ПО УБЫВАНИЮ"])
        reverse = sort_order == "ПО УБЫВАНИЮ"
        filtered_by_status = sort_by_date(filtered_by_status, reverse)

    # Фильтрация по рублевым транзакциям
    if get_yes_no("\nВыводить только рублевые транзакции? Да/Нет: "):
        ruble_transactions = []
        for transaction in filtered_by_status:
            operation_amount = transaction.get("operationAmount", {})
            currency = operation_amount.get("currency", {}).get("code", "")
            if currency == "RUB":
                ruble_transactions.append(transaction)
        filtered_by_status = ruble_transactions

    # Фильтрация по слову в описании
    if get_yes_no("\nОтфильтровать список транзакций по определенному слову в описании? Да/Нет: "):
        search_word = input("Введите слово для поиска: ").strip()
        if search_word:
            filtered_by_status = filter_by_description(filtered_by_status, search_word)

    # Вывод результата
    print("\nРаспечатываю итоговый список транзакций...")
    print_transactions(filtered_by_status)


if __name__ == "__main__":
    main()
