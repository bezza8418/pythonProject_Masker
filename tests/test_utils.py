"""
Тесты для модуля utils.
"""

import json
import os
import tempfile
from typing import Any, Dict, Generator, List

import pytest

from src.utils import load_transactions


@pytest.fixture
def temp_json_file() -> Generator[str, None, None]:
    """Фикстура для создания временного JSON файла."""
    with tempfile.NamedTemporaryFile(
        mode="w+", encoding="utf-8", suffix=".json", delete=False
    ) as tmp:
        tmp_path = tmp.name
    yield tmp_path
    # Очистка после теста
    if os.path.exists(tmp_path):
        os.unlink(tmp_path)


@pytest.fixture
def sample_transactions_data() -> List[Dict[str, Any]]:
    """Фикстура с тестовыми данными транзакций."""
    return [
        {
            "id": 441945886,
            "state": "EXECUTED",
            "date": "2019-08-26T10:50:58.294041",
            "operationAmount": {
                "amount": "31957.58",
                "currency": {"name": "руб.", "code": "RUB"},
            },
            "description": "Перевод организации",
            "from": "Maestro 1596837868705199",
            "to": "Счет 64686473678894779589",
        },
        {
            "id": 41428829,
            "state": "EXECUTED",
            "date": "2019-07-03T18:35:29.512374",
            "operationAmount": {
                "amount": "8221.37",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод организации",
            "from": "MasterCard 7158300734726758",
            "to": "Счет 35383033474447895560",
        },
    ]


class TestLoadTransactions:
    """Тесты для функции load_transactions."""

    def test_load_transactions_success(
        self, temp_json_file: str, sample_transactions_data: List[Dict[str, Any]]
    ) -> None:
        """Тест успешной загрузки транзакций из JSON файла."""
        # Записываем тестовые данные в файл
        with open(temp_json_file, "w", encoding="utf-8") as f:
            json.dump(sample_transactions_data, f)

        # Загружаем данные
        result = load_transactions(temp_json_file)

        # Проверяем результат
        assert len(result) == 2
        assert result[0]["id"] == 441945886
        assert result[1]["id"] == 41428829
        assert result[0]["operationAmount"]["currency"]["code"] == "RUB"
        assert result[1]["operationAmount"]["currency"]["code"] == "USD"

    def test_load_transactions_file_not_found(self) -> None:
        """Тест загрузки из несуществующего файла."""
        result = load_transactions("/path/to/nonexistent/file.json")
        assert result == []

    def test_load_transactions_empty_file(self, temp_json_file: str) -> None:
        """Тест загрузки из пустого файла."""
        # Создаем пустой файл
        with open(temp_json_file, "w", encoding="utf-8") as _:
            pass

        result = load_transactions(temp_json_file)
        assert result == []

    def test_load_transactions_invalid_json(self, temp_json_file: str) -> None:
        """Тест загрузки из файла с некорректным JSON."""
        # Записываем некорректный JSON
        with open(temp_json_file, "w", encoding="utf-8") as f:
            f.write("{invalid json}")

        result = load_transactions(temp_json_file)
        assert result == []

    def test_load_transactions_not_a_list(self, temp_json_file: str) -> None:
        """Тест загрузки из файла, где данные не являются списком."""
        # Записываем словарь вместо списка
        with open(temp_json_file, "w", encoding="utf-8") as f:
            json.dump({"key": "value"}, f)

        result = load_transactions(temp_json_file)
        assert result == []

    def test_load_transactions_empty_list(self, temp_json_file: str) -> None:
        """Тест загрузки из файла с пустым списком."""
        with open(temp_json_file, "w", encoding="utf-8") as f:
            json.dump([], f)

        result = load_transactions(temp_json_file)
        assert result == []

    def test_load_transactions_with_operations_json(self) -> None:
        """Тест загрузки из реального файла operations.json."""
        # Предполагаем, что файл находится в директории data/
        import os

        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(project_root, "data", "operations.json")

        if os.path.exists(file_path):
            result = load_transactions(file_path)
            assert isinstance(result, list)
            # Проверяем структуру первой транзакции, если список не пуст
            if result:
                assert "id" in result[0]
                assert "state" in result[0]
                assert "date" in result[0]
                assert "operationAmount" in result[0]
        else:
            # Пропускаем тест, если файл не существует
            pytest.skip("Файл operations.json не найден")

    def test_load_transactions_permission_error(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Тест ошибки доступа к файлу."""

        def mock_open(*args, **kwargs):
            raise PermissionError("Permission denied")

        monkeypatch.setattr("builtins.open", mock_open)

        result = load_transactions("/path/to/file.json")
        assert result == []
