"""
Модуль с декораторами для логирования выполнения функций.
"""

import functools
import sys
from typing import Any, Callable, Optional, TextIO


def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для логирования вызовов функций.

    Args:
        filename: Опциональный путь к файлу для записи логов.
                 Если не указан, логи выводятся в консоль.

    Returns:
        Callable: Обернутая функция с логированием.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Настраиваем вывод логов
            log_output: TextIO
            if filename:
                # Запись в файл
                log_output = open(filename, "a", encoding="utf-8")
            else:
                # Вывод в консоль
                log_output = sys.stdout

            try:
                # Выполняем функцию
                result = func(*args, **kwargs)

                # Логируем успешное выполнение
                log_output.write(f"{func.__name__} ok\n")
                log_output.flush()

                return result

            except Exception as e:
                # Логируем ошибку
                error_msg = f"{func.__name__} error: {type(e).__name__}. Inputs: {args}, {kwargs}\n"
                log_output.write(error_msg)
                log_output.flush()

                # Пробрасываем исключение дальше
                raise

            finally:
                # Закрываем файл, если он был открыт
                if filename and not log_output.closed:
                    log_output.close()

        return wrapper

    return decorator
