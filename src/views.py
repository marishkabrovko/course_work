import json
from datetime import datetime
from typing import Dict, Any

import pandas as pd

from src.utils import (calculate_spending_and_cashback, fetch_currency_rates,
                       fetch_stock_prices, get_start_of_month,
                       get_top_transactions, load_user_settings)


def main_page(df: pd.DataFrame, dt_str: str) -> str:
    """Функция для страницы «Главная», принимает на вход DataFrame и строку с датой и временем."""

    if not dt_str:
        raise ValueError("Дата и время не предоставлены")

    try:
        date_time = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        raise ValueError("Неверный формат даты и времени")

    start_of_month = get_start_of_month(date_time.strftime("%Y-%m-%d"))

    # Фильтрация данных по дате
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

    # Формирование JSON-ответа
    response = {
        "greeting": greeting,
        "cards": [
            {"last_digits": "5814", "total_spent": round(total_spent, 2), "cashback": round(cashback, 2)},
            {"last_digits": "7512", "total_spent": 7.94, "cashback": 0.08},
        ],
        "top_transactions": [
            {
                "date": tx["Дата операции"].strftime("%d.%m.%Y"),
                "amount": round(tx["Сумма платежа"], 2),
                "category": tx["Категория"],
                "description": tx.get("Описание", "")
            } for tx in top_transactions
        ],
        "currency_rates": [
            {"currency": rate["currency"], "rate": round(rate["rate"], 2)} for rate in currency_rates
        ],
        "stock_prices": [
            {"stock": stock["stock"], "price": round(stock["price"], 2)} for stock in stock_prices
        ]
    }

    # Преобразование ответа в JSON-строку
    return json.dumps(response, ensure_ascii=False, indent=4)
