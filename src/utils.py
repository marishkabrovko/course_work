import json
import logging
import os
from typing import Dict, List, Tuple

import pandas as pd
import requests
from dotenv import load_dotenv

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения из .env файла
load_dotenv()

# Загрузка API ключей из .env файла
CURRENCY_API_KEY = os.getenv("CURRENCY_API_KEY")
STOCK_API_KEY = os.getenv("STOCK_API_KEY")


def load_user_settings(filename="user_settings.json") -> Dict:
    """Загрузка настроек пользователя из JSON-файла."""
    try:
        with open(filename, "r") as file:
            settings = json.load(file)
    except FileNotFoundError as e:
        logger.error(f"Файл настроек не найден: {e}")
        settings = {"user_currencies": [], "user_stocks": []}
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка чтения файла настроек: {e}")
        settings = {"user_currencies": [], "user_stocks": []}
    return settings


def get_start_of_month(dt: str) -> str:
    """Возвращает первый день месяца для данной даты."""
    date = pd.to_datetime(dt)
    start_of_month = date.replace(day=1)
    return start_of_month.strftime("%Y-%m-%d")


def calculate_spending_and_cashback(dataframe: pd.DataFrame) -> Tuple[float, float]:
    """Вычисляет общие расходы и кешбэк."""
    total_spent = dataframe["Сумма операции"].sum()
    cashback = total_spent / 100  # 1 рубль на каждые 100 рублей
    return total_spent, cashback


def get_top_transactions(dataframe: pd.DataFrame, top_n: int = 5) -> List[Dict]:
    """Возвращает топ N транзакций по сумме платежа."""
    top_transactions = dataframe.nlargest(top_n, "Сумма платежа")
    return top_transactions[
        ["Дата операции", "Сумма платежа", "Категория", "Описание"]
    ].to_dict(orient="records")


def fetch_currency_rates(currencies: List[str]) -> List[Dict]:
    """Получает курсы валют из API."""
    url = f"https://api.apilayer.com/exchangerates_data/latest"
    headers = {"apikey": CURRENCY_API_KEY}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        rates = [
            {"currency": currency, "rate": data["rates"].get(currency, 0.0)}
            for currency in currencies
        ]
    except requests.RequestException as e:
        logger.error(f"Ошибка при запросе курсов валют: {e}")
        rates = [{"currency": currency, "rate": 0.0} for currency in currencies]
    return rates


def fetch_stock_prices(stocks: List[str]) -> List[Dict]:
    """Получает цены акций из API."""
    url = f"https://api.apilayer.com/exchangerates_data/latest"
    headers = {"apikey": STOCK_API_KEY}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        stock_prices = [
            {"stock": stock, "price": data["rates"].get(stock, 0.0)} for stock in stocks
        ]
    except requests.RequestException as e:
        logger.error(f"Ошибка при запросе цен акций: {e}")
        stock_prices = [{"stock": stock, "price": 0.0} for stock in stocks]
    return stock_prices
