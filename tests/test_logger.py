"""
Тесты для модуля logger.
"""

import logging
import os
import shutil
from typing import Generator

import pytest

from src.logger import setup_logger


@pytest.fixture
def temp_log_dir() -> Generator[str, None, None]:
    """Фикстура для создания временной директории для логов."""
    # Создаем временную директорию, которая будет использоваться как корень проекта
    temp_dir = os.path.join(os.getcwd(), "temp_test_logs")
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir, ignore_errors=True)
    os.makedirs(temp_dir, exist_ok=True)

    # Сохраняем текущую директорию
    original_dir = os.getcwd()

    # Переходим во временную директорию
    os.chdir(temp_dir)

    yield temp_dir

    # Возвращаемся в исходную директорию
    os.chdir(original_dir)

    # Очищаем после тестов
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir, ignore_errors=True)


class TestLogger:
    """Тесты для функций логирования."""

    def test_setup_logger_creates_logs_directory(self, temp_log_dir: str) -> None:
        """Тест создания директории logs."""
        # Создаем логгер
        logger = setup_logger("test_logger", "test.log")

        # Проверяем, что директория logs создана в текущей директории
        logs_dir = os.path.join(os.getcwd(), "logs")
        assert os.path.exists(logs_dir), f"Директория {logs_dir} не создана"

        # Закрываем обработчики
        for handler in logger.handlers[:]:
            handler.close()
            logger.removeHandler(handler)

    def test_setup_logger_creates_log_file(self, temp_log_dir: str) -> None:
        """Тест создания файла лога."""
        # Создаем логгер
        logger = setup_logger("test_logger", "test.log")

        # Проверяем, что файл создан
        log_file = os.path.join(os.getcwd(), "logs", "test.log")
        assert os.path.exists(log_file), f"Файл {log_file} не создан"

        # Закрываем обработчики
        for handler in logger.handlers[:]:
            handler.close()
            logger.removeHandler(handler)

    def test_setup_logger_writes_to_file(self, temp_log_dir: str) -> None:
        """Тест записи в файл лога."""
        # Создаем логгер и пишем сообщение
        logger = setup_logger("test_logger", "test.log")
        test_message = "Test log message"
        logger.info(test_message)

        # Закрываем обработчики
        for handler in logger.handlers[:]:
            handler.close()
            logger.removeHandler(handler)

        # Проверяем содержимое файла
        log_file = os.path.join(os.getcwd(), "logs", "test.log")
        assert os.path.exists(log_file)

        with open(log_file, "r", encoding="utf-8") as f:
            content = f.read()
            assert test_message in content

    def test_setup_logger_respects_log_level(self, temp_log_dir: str) -> None:
        """Тест соблюдения уровня логирования."""
        # Создаем логгер с уровнем WARNING
        logger = setup_logger("test_logger", "test.log", level=logging.WARNING)

        # Пишем сообщения разных уровней
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")

        # Закрываем обработчики
        for handler in logger.handlers[:]:
            handler.close()
            logger.removeHandler(handler)

        # Проверяем, что только WARNING и ERROR попали в лог
        log_file = os.path.join(os.getcwd(), "logs", "test.log")
        assert os.path.exists(log_file)

        with open(log_file, "r", encoding="utf-8") as f:
            content = f.read()
            assert "Debug message" not in content
            assert "Info message" not in content
            assert "Warning message" in content
            assert "Error message" in content
