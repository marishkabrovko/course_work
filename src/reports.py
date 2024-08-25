import datetime
import json
import logging
from typing import Any, Callable, List, Optional

import pandas as pd

from src.decorators import decorator_spending_by_category
from src.read_excel import read_excel
from src.utils import (calculate_spending_and_cashback, fetch_currency_rates,
                       fetch_stock_prices, get_top_transactions,
                       load_user_settings)

logger = logging.getLogger("report.log")
file_handler = logging.FileHandler("report.log", "w")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def log_spending_by_category(filename: Any) -> Callable:
    """Логирует результат функции в указанный файл"""

    def decorator(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = func(*args, **kwargs)
            with open(filename, "w") as f:
                json.dump(result, f, indent=4)
            return result

        return wrapper

    return decorator


@decorator_spending_by_category
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> dict:
    """Функция возвращающая траты за последние 3 месяца по заданной категории и формирующая JSON-ответ"""

    logger.info("Начало работы")

    if date is None:
        logger.info("Вариант обработки с настоящей датой")
        date_start = datetime.datetime.now() - datetime.timedelta(days=90)
    else:
        logger.info("Вариант обработки с введенной датой")
        day, month, year = date.split(".")
        date_obj = datetime.datetime(int(year), int(month), int(day))
        date_start = date_obj - datetime.timedelta(days=90)

    logger.info("Фильтрация транзакций по категории и дате")
    filtered_transactions = transactions[
        (transactions["Категория"] == category)
        & (
            pd.to_datetime(transactions["Дата платежа"], format="%d.%m.%Y")
            >= date_start
        )
    ]

    total_spent, cashback = calculate_spending_and_cashback(filtered_transactions)
    top_transactions = get_top_transactions(filtered_transactions)

    settings = load_user_settings()
    currencies = settings.get("user_currencies", [])
    stocks = settings.get("user_stocks", [])

    currency_rates = fetch_currency_rates(currencies)
    stock_prices = fetch_stock_prices(stocks)

    # Определение приветствия
    current_hour = datetime.datetime.now().hour
    if 5 <= current_hour < 12:
        greeting = "Доброе утро"
    elif 12 <= current_hour < 18:
        greeting = "Добрый день"
    elif 18 <= current_hour < 23:
        greeting = "Добрый вечер"
    else:
        greeting = "Доброй ночи"

    # Формирование JSON-ответа
    response = {
        "greeting": greeting,
        "cards": [
            {"last_digits": "5814", "total_spent": total_spent, "cashback": cashback},
            {"last_digits": "7512", "total_spent": 7.94, "cashback": 0.08},
        ],
        "top_transactions": [
            {
                "date": t["Дата операции"],
                "amount": t["Сумма платежа"],
                "category": t["Категория"],
                "description": t["Описание"],
            }
            for t in top_transactions
        ],
        "currency_rates": currency_rates,
        "stock_prices": stock_prices,
    }

    logger.info("Формирование завершено")

    return response
