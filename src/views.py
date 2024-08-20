import json
import logging
import requests
import pandas as pd
import os
from dotenv import load_dotenv
from src.utils import (
    parse_date,
    generate_greeting,
    get_start_of_month,
    calculate_spending_and_cashback,
    get_top_transactions,
    load_user_settings
)

load_dotenv()

API_KEY = os.getenv("API_KEY")
CURRENCY_BASE_URL = "https://api.apilayer.com/exchangerates_data/latest"
STOCK_BASE_URL = "https://api.example.com/stocks"

logging.basicConfig(level=logging.INFO)


def fetch_currency_rates(currencies):
    rates = []
    url = f"{CURRENCY_BASE_URL}?symbols={','.join(currencies)}"
    headers = {"apikey": API_KEY}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        for currency in currencies:
            rate = data['rates'].get(currency)
            if rate:
                rates.append({
                    "currency": currency,
                    "rate": rate
                })
            else:
                logging.warning(f"Rate for currency {currency} not found.")
    else:
        logging.error(f"Error fetching currency data: {response.status_code}")

    return rates


def fetch_stock_prices(stocks):
    prices = []
    url = f"{STOCK_BASE_URL}?stocks={','.join(stocks)}"
    headers = {"apikey": API_KEY}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        for stock in stocks:
            price = data.get(stock)
            if price:
                prices.append({
                    "stock": stock,
                    "price": price
                })
            else:
                logging.warning(f"Price for stock {stock} not found.")
    else:
        logging.error(f"Error fetching stock data: {response.status_code}")

    return prices


def main_page(date_time_str):
    year, month, day, hour, minute, second = parse_date(date_time_str)
    settings = load_user_settings()
    start_date = get_start_of_month(year, month)
    df = pd.read_excel("data/operations.xlsx")
    df_filtered = df[(df['date'] >= start_date) & (df['date'] <= date_time_str[:10])]
    total_spent, cashback = calculate_spending_and_cashback(df_filtered)
    top_transactions = get_top_transactions(df_filtered, top_n=5)
    currency_rates = fetch_currency_rates(settings["user_currencies"])
    stock_prices = fetch_stock_prices(settings["user_stocks"])
    response = {
        "greeting": generate_greeting(hour),
        "cards": [
            {
                "last_digits": "****",
                "total_spent": total_spent,
                "cashback": cashback
            }
        ],
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices
    }
    return json.dumps(response, ensure_ascii=False, indent=4)
