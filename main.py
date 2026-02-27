"""
Основной модуль для демонстрации работы функций.
"""

import os
from src.utils import load_transactions
from src.external_api import get_transaction_amount_in_rub


def main():
    """Основная функция для демонстрации работы."""
    # Путь к файлу с транзакциями
    project_root = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(project_root, "data", "operations.json")

    # Загружаем транзакции
    transactions = load_transactions(file_path)

    if not transactions:
        print("Не удалось загрузить транзакции")
        return

    print(f"Загружено {len(transactions)} транзакций\n")

    # Выводим информацию о каждой транзакции
    for i, transaction in enumerate(transactions[:5], 1):  # Показываем первые 5
        try:
            amount_rub = get_transaction_amount_in_rub(transaction)
            description = transaction.get("description", "Неизвестно")
            print(f"{i}. {description}")
            print(f"   Сумма в рублях: {amount_rub:.2f} RUB")
            print()
        except Exception as e:
            print(f"{i}. Ошибка обработки: {e}")


if __name__ == "__main__":
    main()
