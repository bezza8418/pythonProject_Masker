"""
Тесты для модуля logger.
"""

import logging
import os
import shutil

from src.logger import setup_logger

# import pytest


def get_logs_dir() -> str:
    """Возвращает путь к папке logs в корне проекта."""
    tests_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(tests_dir)
    return os.path.join(project_root, "logs")


class TestLogger:
    """Тесты для функций логирования."""

    def setup_method(self):
        """Подготовка перед каждым тестом."""
        self.logs_dir = get_logs_dir()
        # Удаляем папку logs, если она существует
        if os.path.exists(self.logs_dir):
            shutil.rmtree(self.logs_dir, ignore_errors=True)

    def teardown_method(self):
        """Очистка после каждого теста."""
        # Удаляем папку logs после теста
        if os.path.exists(self.logs_dir):
            shutil.rmtree(self.logs_dir, ignore_errors=True)

    def test_setup_logger_creates_logs_directory(self) -> None:
        """Тест создания директории logs."""
        # Создаем логгер
        logger = setup_logger("test_logger", "test.log")

        # Проверяем, что директория logs создана
        assert os.path.exists(self.logs_dir), f"Директория {self.logs_dir} не создана"

        # Закрываем обработчики
        for handler in logger.handlers[:]:
            handler.close()
            logger.removeHandler(handler)

    def test_setup_logger_creates_log_file(self) -> None:
        """Тест создания файла лога."""
        # Создаем логгер
        logger = setup_logger("test_logger", "test.log")

        # Проверяем, что файл создан
        log_file = os.path.join(self.logs_dir, "test.log")
        assert os.path.exists(log_file), f"Файл {log_file} не создан"

        # Закрываем обработчики
        for handler in logger.handlers[:]:
            handler.close()
            logger.removeHandler(handler)

    def test_setup_logger_writes_to_file(self) -> None:
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
        log_file = os.path.join(self.logs_dir, "test.log")
        assert os.path.exists(log_file)

        with open(log_file, "r", encoding="utf-8") as f:
            content = f.read()
            assert test_message in content

    def test_setup_logger_respects_log_level(self) -> None:
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

        # Проверяем содержимое файла
        log_file = os.path.join(self.logs_dir, "test.log")
        assert os.path.exists(log_file)

        with open(log_file, "r", encoding="utf-8") as f:
            content = f.read()
            assert "Debug message" not in content
            assert "Info message" not in content
            assert "Warning message" in content
            assert "Error message" in content
