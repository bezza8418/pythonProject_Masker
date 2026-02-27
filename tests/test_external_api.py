"""
Тесты для модуля external_api.
"""

from unittest.mock import Mock, patch

import pytest
import requests

from src.external_api import convert_amount, get_exchange_rate, get_transaction_amount_in_rub


class TestGetExchangeRate:
    """Тесты для функции get_exchange_rate."""

    @patch('src.external_api.requests.get')
    def test_get_exchange_rate_success_usd(self, mock_get: Mock) -> None:
        """Тест успешного получения курса USD к RUB."""
        # Настраиваем мок-ответ
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "rates": {"RUB": 92.45}
        }
        mock_get.return_value = mock_response

        # Вызываем функцию
        rate = get_exchange_rate("USD")

        # Проверяем результат
        assert rate == 92.45
        mock_get.assert_called_once()

    @patch('src.external_api.requests.get')
    def test_get_exchange_rate_success_eur(self, mock_get: Mock) -> None:
        """Тест успешного получения курса EUR к RUB."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "rates": {"RUB": 99.12}
        }
        mock_get.return_value = mock_response

        rate = get_exchange_rate("EUR")
        assert rate == 99.12

    @patch('src.external_api.requests.get')
    def test_get_exchange_rate_api_error(self, mock_get: Mock) -> None:
        """Тест ошибки API."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": False,
            "error": {"info": "Invalid API key"}
        }
        mock_get.return_value = mock_response

        with pytest.raises(Exception, match="API вернул ошибку"):
            get_exchange_rate("USD")

    @patch('src.external_api.requests.get')
    def test_get_exchange_rate_request_exception(self, mock_get: Mock) -> None:
        """Тест исключения при запросе."""
        mock_get.side_effect = requests.RequestException("Connection error")

        with pytest.raises(Exception, match="Ошибка при запросе к API"):
            get_exchange_rate("USD")

    @patch('src.external_api.API_KEY', None)
    def test_get_exchange_rate_no_api_key(self) -> None:
        """Тест отсутствия API ключа."""
        with pytest.raises(ValueError, match="API ключ не найден"):
            get_exchange_rate("USD")

    @patch('src.external_api.requests.get')
    def test_get_exchange_rate_missing_rate(self, mock_get: Mock) -> None:
        """Тест отсутствия курса в ответе."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "rates": {}
        }
        mock_get.return_value = mock_response

        with pytest.raises(Exception, match="Не удалось получить курс"):
            get_exchange_rate("USD")


class TestConvertAmount:
    """Тесты для функции convert_amount."""

    @patch('src.external_api.get_exchange_rate')
    def test_convert_amount_usd_to_rub(self, mock_get_rate: Mock) -> None:
        """Тест конвертации USD в RUB."""
        mock_get_rate.return_value = 92.45

        result = convert_amount(100, "USD")

        assert result == 9245.0
        mock_get_rate.assert_called_once_with("USD")

    @patch('src.external_api.get_exchange_rate')
    def test_convert_amount_eur_to_rub(self, mock_get_rate: Mock) -> None:
        """Тест конвертации EUR в RUB."""
        mock_get_rate.return_value = 99.12

        result = convert_amount(50.50, "EUR")

        assert result == 5005.56  # 50.50 * 99.12 = 5005.56
        mock_get_rate.assert_called_once_with("EUR")

    def test_convert_amount_rub_to_rub(self) -> None:
        """Тест конвертации RUB в RUB (без изменения)."""
        result = convert_amount(1000, "RUB")
        assert result == 1000.0

    def test_convert_amount_string_amount(self) -> None:
        """Тест конвертации суммы в виде строки."""
        result = convert_amount("150.75", "RUB")
        assert result == 150.75

    @patch('src.external_api.get_exchange_rate')
    def test_convert_amount_invalid_amount(self, mock_get_rate: Mock) -> None:
        """Тест с некорректной суммой."""
        with pytest.raises(ValueError, match="Некорректная сумма"):
            convert_amount("invalid", "USD")

    def test_convert_amount_unsupported_currency(self) -> None:
        """Тест с неподдерживаемой валютой."""
        with pytest.raises(ValueError, match="Неподдерживаемая валюта"):
            convert_amount(100, "GBP")

    @patch('src.external_api.get_exchange_rate')
    def test_convert_amount_api_error(self, mock_get_rate: Mock) -> None:
        """Тест ошибки при получении курса."""
        mock_get_rate.side_effect = Exception("API error")

        with pytest.raises(Exception, match="Ошибка конвертации"):
            convert_amount(100, "USD")


class TestGetTransactionAmountInRub:
    """Тесты для функции get_transaction_amount_in_rub."""

    @patch('src.external_api.convert_amount')
    def test_get_transaction_amount_rub(self, mock_convert: Mock) -> None:
        """Тест получения суммы RUB транзакции."""
        transaction = {
            "operationAmount": {
                "amount": "5000.00",
                "currency": {"code": "RUB"}
            }
        }
        mock_convert.return_value = 5000.0

        result = get_transaction_amount_in_rub(transaction)

        assert result == 5000.0
        mock_convert.assert_called_once_with("5000.00", "RUB")

    @patch('src.external_api.convert_amount')
    def test_get_transaction_amount_usd(self, mock_convert: Mock) -> None:
        """Тест получения суммы USD транзакции в рублях."""
        transaction = {
            "operationAmount": {
                "amount": "100.50",
                "currency": {"code": "USD"}
            }
        }
        mock_convert.return_value = 9291.23  # 100.50 * 92.45

        result = get_transaction_amount_in_rub(transaction)

        assert result == 9291.23
        mock_convert.assert_called_once_with("100.50", "USD")

    def test_get_transaction_amount_missing_amount(self) -> None:
        """Тест отсутствия суммы в транзакции."""
        transaction = {
            "operationAmount": {
                "currency": {"code": "USD"}
            }
        }

        with pytest.raises(ValueError, match="Некорректная структура транзакции"):
            get_transaction_amount_in_rub(transaction)

    def test_get_transaction_amount_missing_operation_amount(self) -> None:
        """Тест отсутствия operationAmount в транзакции."""
        transaction = {
            "amount": "100",
            "currency": "USD"
        }

        with pytest.raises(ValueError, match="Некорректная структура транзакции"):
            get_transaction_amount_in_rub(transaction)

    def test_get_transaction_amount_invalid_structure(self) -> None:
        """Тест некорректной структуры транзакции."""
        transaction = {"id": 1, "description": "test"}

        with pytest.raises(ValueError, match="Некорректная структура транзакции"):
            get_transaction_amount_in_rub(transaction)

    @patch('src.external_api.convert_amount')
    def test_get_transaction_amount_convert_error(self, mock_convert: Mock) -> None:
        """Тест ошибки конвертации."""
        transaction = {
            "operationAmount": {
                "amount": "100",
                "currency": {"code": "USD"}
            }
        }
        mock_convert.side_effect = Exception("Conversion error")

        with pytest.raises(Exception, match="Ошибка конвертации"):
            get_transaction_amount_in_rub(transaction)
