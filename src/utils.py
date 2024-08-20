# src/utils.py

import json
import requests
import pandas as pd
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)


def parse_date(date_time_str):
    try:
        dt = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
        return dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second
    except ValueError:
        raise ValueError("Invalid date format")


def generate_greeting(hour):
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_start_of_month(year, month):
    return f"{year}-{month:02d}-01"


def calculate_spending_and_cashback(df):
    total_spent = df["amount"].sum()
    cashback = total_spent / 100
    return total_spent, cashback


def get_top_transactions(df, top_n=3):
    top_transactions = df.nlargest(top_n, "amount")[["date", "amount", "category", "description"]]
    return top_transactions.to_dict(orient="records")


def fetch_currency_rates(currencies):
    API_KEY = "DLQ8Gc6x9Rz7TkYRRNIKLtdJZTqrSU8z"
    BASE_URL = "https://api.apilayer.com/exchangerates_data/latest"
    headers = {"apikey": API_KEY}

    response = requests.get(BASE_URL, headers=headers)
    data = response.json()

    rates = [{"currency": currency, "rate": data["rates"].get(currency, "N/A")} for currency in currencies]
    return rates


def fetch_stock_prices(stocks):
    API_KEY = "DLQ8Gc6x9Rz7TkYRRNIKLtdJZTqrSU8z"
    BASE_URL = "https://api.apilayer.com/exchangerates_data/latest"
    headers = {"apikey": API_KEY}

    response = requests.get(BASE_URL, headers=headers)
    data = response.json()

    # Замените на реальный API для получения цен акций
    # Заглушка
    prices = [{"stock": stock, "price": "N/A"} for stock in stocks]
    return prices


def load_user_settings():
    with open('user_settings.json', 'r', encoding='utf-8') as file:
        settings = json.load(file)
    return settings
