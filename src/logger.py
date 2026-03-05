"""
Модуль для настройки логирования в проекте.
"""

import logging
import os


def setup_logger(name: str, log_file: str, level: int = logging.INFO) -> logging.Logger:
    """
    Настраивает и возвращает логер для указанного модуля.

    Args:
        name: Имя логера (обычно __name__ модуля)
        log_file: Имя файла для записи логов
        level: Уровень логирования

    Returns:
        logging.Logger: Настроенный логер
    """
    # Создаем папку logs, если её нет
    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
    os.makedirs(log_dir, exist_ok=True)

    # Полный путь к файлу лога
    log_path = os.path.join(log_dir, log_file)

    # Создаем логер
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Очищаем существующие обработчики (для перезаписи при каждом запуске)
    if logger.handlers:
        logger.handlers.clear()

    # Создаем обработчик для записи в файл (режим 'w' для перезаписи)
    file_handler = logging.FileHandler(log_path, mode='w', encoding='utf-8')
    file_handler.setLevel(level)

    # Настраиваем формат логов
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)

    # Добавляем обработчик к логеру
    logger.addHandler(file_handler)

    return logger
