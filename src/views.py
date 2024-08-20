# src/views.py

import json
import logging
from datetime import datetime
from src.utils import (
    parse_date,
    generate_greeting,
    get_start_of_month,
    calculate_spending_and_cashback,
    get_top_transactions,
    fetch_currency_rates,
    fetch_stock_prices,
    load_user_settings
)

logging.basicConfig(level=logging.INFO)


def main_page(date_time_str: str):
    # Парсим входную дату
    try:
        year, month, day, hour, minute, second = parse_date(date_time_str)
    except ValueError as e:
        logging.error(f"Date parsing error: {e}")
        return json.dumps({"error": "Invalid date format"}), 400

    # Генерируем приветствие
    greeting = generate_greeting(hour)

    # Загружаем настройки пользователя
    user_settings = load_user_settings()
    user_currencies = user_settings.get("user_currencies", [])
    user_stocks = user_settings.get("user_stocks", [])

    # Вычисляем начало месяца
    start_date = get_start_of_month(year, month)

    # Загружаем данные из Excel (заглушка, замените на реальную логику)
    df_filtered = pd.DataFrame()  # Замените на реальную логику чтения Excel файла

    # Вычисляем расходы и кешбэк
    total_spent, cashback = calculate_spending_and_cashback(df_filtered)

    # Получаем топ-3 транзакции
    top_transactions = get_top_transactions(df_filtered, top_n=3)

    # Получаем курсы валют
    currency_rates = fetch_currency_rates(user_currencies)

    # Получаем цены акций
    stock_prices = fetch_stock_prices(user_stocks)

    # Формируем JSON-ответ
    response = {
        "greeting": greeting,
        "cards": [
            {"last_digits": "****", "total_spent": total_spent, "cashback": cashback}
        ],
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices
    }

    return json.dumps(response, ensure_ascii=False, indent=4)
