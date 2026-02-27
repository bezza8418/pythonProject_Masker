"""
Модуль для работы с JSON-файлами, содержащими данные о транзакциях.
"""

import json
import os
from typing import Any, Dict, List


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает данные о транзакциях из JSON-файла.

    Args:
        file_path: Путь до JSON-файла

    Returns:
        Список словарей с данными о транзакциях.
        Если файл пустой, содержит не список или не найден, возвращает пустой список.
    """
    # Проверяем существование файла
    if not os.path.exists(file_path):
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Проверяем, что данные являются списком
        if not isinstance(data, list):
            return []

        return data

    except json.JSONDecodeError, FileNotFoundError, PermissionError:
        # В случае любой ошибки при чтении/парсинге возвращаем пустой список
        return []
