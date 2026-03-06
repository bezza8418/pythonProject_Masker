"""
Тесты для модуля file_readers.
"""

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
        import json
        json.dump(data, f)
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
def temp_excel_file() -> Generator[str, None, None]:
    """Фикстура для создания временного Excel-файла."""
    data = [
        {"id": 1, "amount": 100, "currency": "RUB"},
        {"id": 2, "amount": 200, "currency": "USD"},
    ]
    with tempfile.NamedTemporaryFile(
        suffix=".xlsx", delete=False
    ) as f:
        df = pd.DataFrame(data)
        df.to_excel(f.name, index=False)
        temp_path = f.name
    yield temp_path
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

    def test_read_json_file_not_found(self):
        """Тест чтения несуществующего JSON-файла."""
        result = read_json_file("nonexistent.json")
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
