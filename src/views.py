# src/views.py

import json
from datetime import datetime
from typing import Dict

import pandas as pd

from src.utils import (calculate_spending_and_cashback, fetch_currency_rates,
                       fetch_stock_prices, get_start_of_month,
                       get_top_transactions, load_user_settings)


def main_page(dt_str: str) -> Dict:
    """Функция для страницы «Главная»."""
    if not dt_str:
        raise ValueError("Дата и время не предоставлены")

    try:
        date_time = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        raise ValueError("Неверный формат даты и времени")

    start_of_month = get_start_of_month(date_time.strftime("%Y-%m-%d"))

    # Загрузка данных из Excel
    try:
        df = pd.read_excel("data/operations.xlsx")
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Файл данных не найден: {e}")
    except Exception as e:
        raise Exception(f"Ошибка при чтении файла данных: {e}")

    # Фильтрация данных
    filtered_df = df[
        (df["Дата операции"] >= start_of_month) & (df["Дата операции"] <= dt_str)
    ]

    # Расчеты
    total_spent, cashback = calculate_spending_and_cashback(filtered_df)
    top_transactions = get_top_transactions(filtered_df)

    # Загрузка настроек пользователя
    settings = load_user_settings()
    currencies = settings.get("user_currencies", [])
    stocks = settings.get("user_stocks", [])

    # Получение данных
    currency_rates = fetch_currency_rates(currencies)
    stock_prices = fetch_stock_prices(stocks)

    # Приветствие
    hour = date_time.hour
    if 5 <= hour < 12:
        greeting = "Доброе утро"
    elif 12 <= hour < 18:
        greeting = "Добрый день"
    elif 18 <= hour < 23:
        greeting = "Добрый вечер"
    else:
        greeting = "Доброй ночи"

    response = {
        "greeting": greeting,
        "cards": [
            {"last_digits": "5814", "total_spent": total_spent, "cashback": cashback},
            {"last_digits": "7512", "total_spent": 7.94, "cashback": 0.08},
        ],
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices,
    }

    return response
