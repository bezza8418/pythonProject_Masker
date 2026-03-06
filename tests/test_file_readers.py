"""
Тесты для модуля file_readers.
"""

import json
import os
import tempfile
from typing import Generator

import pandas as pd
import pytest

from src.file_readers import (
    read_csv_file,
    read_excel_file,
    read_json_file,
    read_transactions,
)


@pytest.fixture
def temp_json_file() -> Generator[str, None, None]:
    """Фикстура для создания временного JSON-файла."""
    data = [
        {"id": 1, "amount": 100, "currency": "RUB"},
        {"id": 2, "amount": 200, "currency": "USD"},
    ]
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False, encoding="utf-8"
    ) as f:
        json.dump(data, f)
        temp_path = f.name
    yield temp_path
    os.unlink(temp_path)


@pytest.fixture
def temp_json_not_list_file() -> Generator[str, None, None]:
    """Фикстура для создания JSON-файла с данными не в виде списка."""
    data = {"key": "value", "another": "data"}
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False, encoding="utf-8"
    ) as f:
        json.dump(data, f)
        temp_path = f.name
    yield temp_path
    os.unlink(temp_path)


@pytest.fixture
def temp_invalid_json_file() -> Generator[str, None, None]:
    """Фикстура для создания некорректного JSON-файла."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False, encoding="utf-8"
    ) as f:
        f.write("{invalid json}")
        temp_path = f.name
    yield temp_path
    os.unlink(temp_path)


@pytest.fixture
def temp_csv_file() -> Generator[str, None, None]:
    """Фикстура для создания временного CSV-файла."""
    data = [
        {"id": 1, "amount": 100, "currency": "RUB"},
        {"id": 2, "amount": 200, "currency": "USD"},
    ]
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".csv", delete=False, encoding="utf-8"
    ) as f:
        df = pd.DataFrame(data)
        df.to_csv(f.name, index=False)
        temp_path = f.name
    yield temp_path
    os.unlink(temp_path)


@pytest.fixture
def temp_empty_csv_file() -> Generator[str, None, None]:
    """Фикстура для создания пустого CSV-файла."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".csv", delete=False, encoding="utf-8"
    ) as f:
        f.write("")  # Пустой файл
        temp_path = f.name
    yield temp_path
    os.unlink(temp_path)


@pytest.fixture
def temp_excel_file() -> Generator[str, None, None]:
    """Фикстура для создания временного Excel-файла."""
    data = [
        {"id": 1, "amount": 100, "currency": "RUB"},
        {"id": 2, "amount": 200, "currency": "USD"},
    ]
    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as f:
        df = pd.DataFrame(data)
        df.to_excel(f.name, index=False)
        temp_path = f.name
    yield temp_path
    os.unlink(temp_path)


@pytest.fixture
def temp_protected_file() -> Generator[str, None, None]:
    """Фикстура для создания файла без прав доступа."""
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        temp_path = f.name
    # Делаем файл недоступным для чтения
    try:
        os.chmod(temp_path, 0o000)
    except PermissionError:
        pass  # На Windows может не работать, игнорируем
    yield temp_path
    try:
        os.chmod(temp_path, 0o666)  # Восстанавливаем права для удаления
    except PermissionError:
        pass
    os.unlink(temp_path)


class TestFileReaders:
    """Тесты для функций чтения файлов."""

    def test_read_json_file_success(self, temp_json_file: str):
        """Тест успешного чтения JSON-файла."""
        result = read_json_file(temp_json_file)
        assert len(result) == 2
        assert result[0]["id"] == 1
        assert result[0]["amount"] == 100
        assert result[0]["currency"] == "RUB"

    def test_read_json_file_not_list(self, temp_json_not_list_file: str):
        """Тест JSON-файла с данными не в виде списка."""
        result = read_json_file(temp_json_not_list_file)
        assert result == []

    def test_read_json_file_not_found(self):
        """Тест чтения несуществующего JSON-файла."""
        result = read_json_file("nonexistent.json")
        assert result == []

    def test_read_json_file_invalid(self, temp_invalid_json_file: str):
        """Тест чтения некорректного JSON-файла."""
        result = read_json_file(temp_invalid_json_file)
        assert result == []

    def test_read_json_file_permission_error(self, temp_protected_file: str):
        """Тест ошибки доступа к файлу."""
        result = read_json_file(temp_protected_file)
        assert result == []

    def test_read_csv_file_success(self, temp_csv_file: str):
        """Тест успешного чтения CSV-файла."""
        result = read_csv_file(temp_csv_file)
        assert len(result) == 2
        assert result[0]["id"] == 1
        assert result[0]["amount"] == 100
        assert result[0]["currency"] == "RUB"

    def test_read_csv_file_not_found(self):
        """Тест чтения несуществующего CSV-файла."""
        result = read_csv_file("nonexistent.csv")
        assert result == []

    def test_read_csv_file_permission_error(self, temp_protected_file: str):
        """Тест ошибки доступа к CSV-файлу."""
        result = read_csv_file(temp_protected_file)
        assert result == []

    def test_read_csv_file_empty(self, temp_empty_csv_file: str):
        """Тест чтения пустого CSV-файла."""
        result = read_csv_file(temp_empty_csv_file)
        assert result == []

    def test_read_excel_file_success(self, temp_excel_file: str):
        """Тест успешного чтения Excel-файла."""
        result = read_excel_file(temp_excel_file)
        assert len(result) == 2
        assert result[0]["id"] == 1
        assert result[0]["amount"] == 100
        assert result[0]["currency"] == "RUB"

    def test_read_excel_file_not_found(self):
        """Тест чтения несуществующего Excel-файла."""
        result = read_excel_file("nonexistent.xlsx")
        assert result == []

    def test_read_excel_file_permission_error(self, temp_protected_file: str):
        """Тест ошибки доступа к Excel-файлу."""
        result = read_excel_file(temp_protected_file)
        assert result == []

    def test_read_transactions_json(self, temp_json_file: str):
        """Тест универсальной функции с JSON."""
        result = read_transactions(temp_json_file)
        assert len(result) == 2

    def test_read_transactions_csv(self, temp_csv_file: str):
        """Тест универсальной функции с CSV."""
        result = read_transactions(temp_csv_file)
        assert len(result) == 2

    def test_read_transactions_excel(self, temp_excel_file: str):
        """Тест универсальной функции с Excel."""
        result = read_transactions(temp_excel_file)
        assert len(result) == 2

    def test_read_transactions_unsupported_format(self):
        """Тест с неподдерживаемым форматом."""
        with pytest.raises(ValueError, match="Неподдерживаемый формат"):
            read_transactions("file.txt")

    def test_read_csv_file_empty_data_error(self, temp_csv_file: str):
        """Тест обработки EmptyDataError."""
        # Создаем CSV, который вызовет EmptyDataError
        with open(temp_csv_file, 'w', encoding='utf-8') as f:
            f.write('')  # Пустой файл - уже тестируем в test_read_csv_file_empty
        result = read_csv_file(temp_csv_file)
        assert result == []

    def test_read_csv_file_unicode_error(self, temp_csv_file: str):
        """Тест обработки UnicodeDecodeError."""
        # Записываем бинарные данные, не в UTF-8
        with open(temp_csv_file, 'wb') as f:
            f.write(b'\xff\xfe\x00\x01')  # Невалидный UTF-8
        result = read_csv_file(temp_csv_file)
        assert result == []

    def test_read_excel_file_value_error(self, temp_excel_file: str):
        """Тест обработки ValueError при чтении Excel."""
        # Записываем что-то, что не является Excel
        with open(temp_excel_file, 'w', encoding='utf-8') as f:
            f.write("This is not an Excel file")
        result = read_excel_file(temp_excel_file)
        assert result == []
