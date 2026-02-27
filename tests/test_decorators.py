"""
Тесты для модуля decorators.
"""

import os
import tempfile
from typing import Generator

import pytest

from src.decorators import log


@pytest.fixture
def temp_log_file() -> Generator[str, None, None]:
    """Фикстура для создания временного файла лога."""
    with tempfile.NamedTemporaryFile(mode="w+", encoding="utf-8", delete=False) as tmp:
        tmp_path = tmp.name
    yield tmp_path
    # Очистка после теста
    if os.path.exists(tmp_path):
        os.unlink(tmp_path)


class TestLogDecorator:
    """Тесты для декоратора log."""

    def test_log_to_console_success(self, capsys: pytest.CaptureFixture) -> None:
        """Тест логирования успешного выполнения в консоль."""

        @log()
        def test_function(a: int, b: int) -> int:
            return a + b

        result = test_function(2, 3)

        assert result == 5
        captured = capsys.readouterr()
        assert captured.out == "test_function ok\n"
        assert captured.err == ""

    def test_log_to_console_error(self, capsys: pytest.CaptureFixture) -> None:
        """Тест логирования ошибки в консоль."""

        @log()
        def test_function(a: int, b: int) -> float:
            return a / b

        with pytest.raises(ZeroDivisionError):
            test_function(5, 0)

        captured = capsys.readouterr()
        assert (
            "test_function error: ZeroDivisionError. Inputs: (5, 0), {}" in captured.out
        )

    def test_log_to_file_success(self, temp_log_file: str) -> None:
        """Тест логирования успешного выполнения в файл."""

        @log(filename=temp_log_file)
        def test_function(a: int, b: int) -> int:
            return a * b

        result = test_function(4, 5)

        assert result == 20

        with open(temp_log_file, "r", encoding="utf-8") as f:
            content = f.read()
        assert content == "test_function ok\n"

    def test_log_to_file_error(self, temp_log_file: str) -> None:
        """Тест логирования ошибки в файл."""

        @log(filename=temp_log_file)
        def test_function(a: int, b: int) -> int:
            return a // b

        with pytest.raises(ZeroDivisionError):
            test_function(10, 0)

        with open(temp_log_file, "r", encoding="utf-8") as f:
            content = f.read()
        assert "test_function error: ZeroDivisionError. Inputs: (10, 0), {}" in content

    def test_log_with_multiple_arguments(self, capsys: pytest.CaptureFixture) -> None:
        """Тест логирования с разными типами аргументов."""

        @log()
        def test_function(a: int, b: str, c: list) -> str:
            return f"{a} {b} {c}"

        result = test_function(1, "hello", [1, 2, 3])

        assert result == "1 hello [1, 2, 3]"
        captured = capsys.readouterr()
        assert captured.out == "test_function ok\n"

    def test_log_with_different_exceptions(self, capsys: pytest.CaptureFixture) -> None:
        """Тест логирования разных типов исключений."""

        @log()
        def test_function(value: int) -> int:
            if value == 1:
                raise ValueError("Invalid value")
            elif value == 2:
                raise KeyError("Key not found")
            return value

        # Тест ValueError
        with pytest.raises(ValueError):
            test_function(1)
        captured = capsys.readouterr()
        assert "test_function error: ValueError. Inputs: (1,), {}" in captured.out

        # Тест KeyError
        with pytest.raises(KeyError):
            test_function(2)
        captured = capsys.readouterr()
        assert "test_function error: KeyError. Inputs: (2,), {}" in captured.out

    def test_log_preserves_function_metadata(self) -> None:
        """Тест сохранения метаданных функции."""

        @log()
        def test_function(a: int, b: int) -> int:
            """Тестовая функция."""
            return a + b

        assert test_function.__name__ == "test_function"
        assert test_function.__doc__ == "Тестовая функция."
        assert test_function.__annotations__ == {"a": int, "b": int, "return": int}

    def test_log_without_filename_creates_no_file(self) -> None:
        """Тест, что без filename не создается файл."""

        @log()
        def test_function(a: int, b: int) -> int:
            return a + b

        test_function(1, 2)

        # Проверяем, что никакой файл не создался
        import glob

        log_files = glob.glob("*.log")
        assert not any("test_function" in f for f in log_files)

    def test_log_appends_to_existing_file(self, temp_log_file: str) -> None:
        """Тест добавления логов в существующий файл."""

        # Первый вызов
        @log(filename=temp_log_file)
        def func1(x: int) -> int:
            return x * 2

        func1(5)

        # Второй вызов с другой функцией
        @log(filename=temp_log_file)
        def func2(y: int) -> int:
            return y + 10

        func2(7)

        with open(temp_log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        assert len(lines) == 2
        assert lines[0] == "func1 ok\n"
        assert lines[1] == "func2 ok\n"

    def test_log_with_empty_filename(self, capsys: pytest.CaptureFixture) -> None:
        """Тест с пустым filename (должен писать в консоль)."""

        @log(filename="")
        def test_function() -> str:
            return "test"

        result = test_function()
        assert result == "test"

        captured = capsys.readouterr()
        assert captured.out == "test_function ok\n"
