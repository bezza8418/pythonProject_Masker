"""
Модуль для чтения финансовых транзакций из различных форматов файлов.
Поддерживает форматы: JSON, CSV, XLSX.
"""

import json
from typing import Any, Dict, List

import pandas as pd
from pandas.errors import EmptyDataError, ParserError


def read_json_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает транзакции из JSON-файла.

    Args:
        file_path: Путь до JSON-файла

    Returns:
        Список словарей с данными о транзакциях
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            return data
        else:
            return []
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []
    except PermissionError:
        return []


def read_csv_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает транзакции из CSV-файла с помощью pandas.

    Args:
        file_path: Путь до CSV-файла

    Returns:
        Список словарей с данными о транзакциях
    """
    try:
        df = pd.read_csv(file_path)
        # Преобразуем DataFrame в список словарей
        transactions = df.to_dict(orient='records')
        return transactions
    except FileNotFoundError:
        return []
    except PermissionError:
        return []
    except EmptyDataError:
        # Файл пустой
        return []
    except ParserError:
        # Ошибка парсинга CSV
        return []
    except UnicodeDecodeError:
        # Проблема с кодировкой
        return []


def read_excel_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает транзакции из Excel-файла с помощью pandas.

    Args:
        file_path: Путь до Excel-файла

    Returns:
        Список словарей с данными о транзакциях
    """
    try:
        df = pd.read_excel(file_path)
        # Преобразуем DataFrame в список словарей
        transactions = df.to_dict(orient='records')
        return transactions
    except FileNotFoundError:
        return []
    except PermissionError:
        return []
    except ValueError:
        # Ошибка при чтении Excel (например, файл поврежден)
        return []
    except ImportError:
        # Нет нужной библиотеки для чтения Excel
        return []


def read_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Универсальная функция для чтения транзакций из файла.
    Автоматически определяет формат по расширению файла.

    Args:
        file_path: Путь до файла

    Returns:
        Список словарей с данными о транзакциях
    """
    if file_path.endswith('.json'):
        return read_json_file(file_path)
    elif file_path.endswith('.csv'):
        return read_csv_file(file_path)
    elif file_path.endswith(('.xlsx', '.xls')):
        return read_excel_file(file_path)
    else:
        raise ValueError(f"Неподдерживаемый формат файла: {file_path}")
