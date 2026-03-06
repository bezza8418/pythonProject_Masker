"""
Модуль для работы с JSON-файлами, содержащими данные о транзакциях.
"""

import json
import logging
import os
from typing import Any, Dict, List

from src.logger import setup_logger

# Настраиваем логер для модуля utils с уровнем DEBUG
logger = setup_logger(__name__, 'utils.log', level=logging.DEBUG)


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает данные о транзакциях из JSON-файла.

    Args:
        file_path: Путь до JSON-файла

    Returns:
        Список словарей с данными о транзакциях.
        Если файл пустой, содержит не список или не найден, возвращает пустой список.
    """
    logger.info(f"Попытка загрузки транзакций из файла: {file_path}")
    logger.debug(f"Абсолютный путь к файлу: {os.path.abspath(file_path)}")

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        logger.debug(f"Тип загруженных данных: {type(data)}")

        # Проверяем, что данные являются списком
        if isinstance(data, list):
            logger.info(f"Успешно загружено {len(data)} транзакций из {file_path}")
            if data:
                logger.debug(f"Первые 3 транзакции: {data[:3]}")
            return data

        logger.warning(f"Данные в файле {file_path} не являются списком")
        return []

    except FileNotFoundError:
        logger.error(f"Файл {file_path} не найден")
        return []
    except PermissionError:
        logger.error(f"Нет прав доступа к файлу {file_path}")
        return []
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка парсинга JSON в файле {file_path}: {e}")
        return []
    except Exception as e:
        logger.error(f"Неожиданная ошибка при загрузке файла {file_path}: {e}")
        return []
