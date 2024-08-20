import json
import os
import requests
import pandas as pd
import logging
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.apilayer.com/exchangerates_data"


def parse_date(date_time_str):
    date_part, time_part = date_time_str.split(" ")
    year, month, day = map(int, date_part.split("-"))
    hour, minute, second = map(int, time_part.split(":"))
    return year, month, day, hour, minute, second


def generate_greeting(hour):
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 22:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_start_of_month(year, month):
    return f"{year:04d}-{month:02d}-01"


def load_user_settings(filepath='user_settings.json'):
    with open(filepath, 'r') as file:
        settings = json.load(file)
    return settings


def get_currency_rates(currencies):
    headers = {
        "apikey": API_KEY
    }
    rates = []
    for currency in currencies:
        url = f"{BASE_URL}/latest?base={currency}&symbols=RUB"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            rate = data['rates'].get('RUB', None)
            if rate:
                rates.append({"currency": currency, "rate": rate})
            else:
                logging.error(f"Rate for RUB not found in response for {currency}")
        else:
            logging.error(f"Error fetching rate for {currency}: {response.status_code}")
    return rates


def get_stock_prices(stocks):
    headers = {
        "apikey": API_KEY
    }
    prices = []
    for stock in stocks:
        url = f"https://api.example.com/stocks/{stock}"  # Замените на реальный URL
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            prices.append({"stock": stock, "price": data['price']})
        else:
            logging.error(f"Error fetching price for {stock}: {response.status_code}")
    return prices


def get_transactions(filepath, start_date_str, end_date_str):
    df = pd.read_excel(filepath)
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
    filtered_df = df[(df['date'] >= start_date_str) & (df['date'] <= end_date_str)]
    return filtered_df


def calculate_spending_and_cashback(transactions):
    total_spent = transactions['amount'].sum()
    cashback = round(total_spent / 100, 2)
    return total_spent, cashback


def get_top_transactions(transactions, top_n=5):
    top_transactions = transactions.nlargest(top_n, 'amount')
    return top_transactions.to_dict(orient='records')
