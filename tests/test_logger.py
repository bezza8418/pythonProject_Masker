"""
Тесты для модуля logger.
"""

import logging
import os
import tempfile
from typing import Generator

import pytest

from src.logger import setup_logger


@pytest.fixture
def temp_log_dir() -> Generator[str, None, None]:
    """Фикстура для создания временной директории для логов."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield tmp_dir


class TestLogger:
    """Тесты для функций логирования."""

    def test_setup_logger_creates_file(self, temp_log_dir: str) -> None:
        """Тест создания файла лога."""
        # Сохраняем оригинальную функцию для восстановления после теста
        original_join = os.path.join
        original_makedirs = os.makedirs

        def mock_join(*args):
            return original_join(temp_log_dir, args[-1])

        def mock_makedirs(path, exist_ok=False):
            pass

        os.path.join = mock_join
        os.makedirs = mock_makedirs

        try:
            logger = setup_logger("test_logger", "test.log")
            logger.info("Test message")

            log_file = os.path.join(temp_log_dir, "test.log")
            assert os.path.exists(log_file)

            with open(log_file, "r", encoding="utf-8") as f:
                content = f.read()
                assert "Test message" in content
        finally:
            os.path.join = original_join
            os.makedirs = original_makedirs

    def test_setup_logger_overwrites_file(self, temp_log_dir: str) -> None:
        """Тест перезаписи файла лога."""
        original_join = os.path.join
        original_makedirs = os.makedirs

        def mock_join(*args):
            return original_join(temp_log_dir, args[-1])

        def mock_makedirs(path, exist_ok=False):
            pass

        os.path.join = mock_join
        os.makedirs = mock_makedirs

        try:
            # Первая запись
            logger1 = setup_logger("test_logger", "test.log")
            logger1.info("First message")

            # Вторая запись (должна перезаписать)
            logger2 = setup_logger("test_logger", "test.log")
            logger2.info("Second message")

            log_file = os.path.join(temp_log_dir, "test.log")
            with open(log_file, "r", encoding="utf-8") as f:
                content = f.read()
                assert "First message" not in content
                assert "Second message" in content
        finally:
            os.path.join = original_join
            os.makedirs = original_makedirs

    def test_setup_logger_handles_different_levels(self, temp_log_dir: str) -> None:
        """Тест разных уровней логирования."""
        original_join = os.path.join
        original_makedirs = os.makedirs

        def mock_join(*args):
            return original_join(temp_log_dir, args[-1])

        def mock_makedirs(path, exist_ok=False):
            pass

        os.path.join = mock_join
        os.makedirs = mock_makedirs

        try:
            logger = setup_logger("test_logger", "test.log", level=logging.WARNING)

            logger.debug("Debug message")
            logger.info("Info message")
            logger.warning("Warning message")
            logger.error("Error message")

            log_file = os.path.join(temp_log_dir, "test.log")
            with open(log_file, "r", encoding="utf-8") as f:
                content = f.read()
                assert "Debug message" not in content
                assert "Info message" not in content
                assert "Warning message" in content
                assert "Error message" in content
        finally:
            os.path.join = original_join
            os.makedirs = original_makedirs

    def test_setup_logger_format(self, temp_log_dir: str) -> None:
        """Тест формата логов."""
        original_join = os.path.join
        original_makedirs = os.makedirs

        def mock_join(*args):
            return original_join(temp_log_dir, args[-1])

        def mock_makedirs(path, exist_ok=False):
            pass

        os.path.join = mock_join
        os.makedirs = mock_makedirs

        try:
            logger = setup_logger("test_logger", "test.log")
            logger.info("Test message")

            log_file = os.path.join(temp_log_dir, "test.log")
            with open(log_file, "r", encoding="utf-8") as f:
                line = f.readline().strip()
                # Проверяем формат: timestamp - name - level - message
                parts = line.split(" - ")
                assert len(parts) >= 4
                assert parts[1] == "test_logger"
                assert parts[2] == "INFO"
                assert parts[3] == "Test message"
        finally:
            os.path.join = original_join
            os.makedirs = original_makedirs
