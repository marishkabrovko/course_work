import json
import functools
import logging
import sys
from typing import Optional, Callable, Any, Dict
import pandas as pd
from datetime import datetime, timedelta


def log(filename: Optional[str] = None) -> Callable:
    """Декоратор для логирования выполнения функций."""

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            logger = logging.getLogger(func.__name__)
            logger.setLevel(logging.INFO)

            if filename:
                handler = logging.FileHandler(filename)
            else:
                handler = logging.StreamHandler(sys.stdout)

            handler.setLevel(logging.INFO)
            formatter = logging.Formatter("%(message)s")
            handler.setFormatter(formatter)
            logger.addHandler(handler)

            try:
                result = func(*args, **kwargs)
                logger.info(f"{func.__name__} ok")
                return result
            except Exception as e:
                logger.error(f"{func.__name__} error: {e}. Inputs: {args}, {kwargs}")
                raise
            finally:
                logger.removeHandler(handler)
                handler.close()

        return wrapper

    return decorator


def save_report(filename: Optional[str] = None) -> Callable:
    """Декоратор для сохранения отчета в файл."""

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = func(*args, **kwargs)
            # Используем значение по умолчанию, если filename не передан
            if filename is None:
                filename = "report.json"

            # Преобразование значений в стандартные типы перед сохранением в JSON
            if isinstance(result, dict):
                result = {k: int(v) for k, v in result.items()}

            with open(filename, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=4)
            logging.info(f"Report saved to {filename}")
            return result

        return wrapper

    return decorator


@log()  # Логируем информацию о выполнении функции
@save_report()  # Сохраняем отчет в файл с именем по умолчанию
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> Dict[str, int]:
    """Возвращает траты по заданной категории за последние три месяца."""
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')

    date = datetime.strptime(date, '%Y-%m-%d')
    three_months_ago = date - timedelta(days=90)

    # Преобразование даты в колонке
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], format='%Y-%m-%d')

    # Фильтрация данных по категории и дате
    filtered_data = transactions[
        (transactions["Категория"] == category) &
        (transactions["Дата операции"] >= three_months_ago)
        ]

    # Подсчет трат
    total_spending = filtered_data["Сумма операции"].sum()

    return {category: total_spending}
