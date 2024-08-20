import pandas as pd
import json
import logging
from typing import List, Dict, Tuple


# Настройка логирования
logging.basicConfig(level=logging.INFO)

USER_SETTINGS_PATH = "user_settings.json"


def parse_date(date_time_str: str) -> Tuple[int, int, int, int, int, int]:
    dt = pd.to_datetime(date_time_str, format="%Y-%m-%d %H:%M:%S")
    return dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second


def generate_greeting(hour: int) -> str:
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_start_of_month(year: int, month: int) -> str:
    return f"{year:04d}-{month:02d}-01"


def calculate_spending_and_cashback(df: pd.DataFrame) -> Tuple[float, float]:
    total_spent = df['amount'].sum()
    cashback = total_spent * 0.01
    return total_spent, cashback


def get_top_transactions(df: pd.DataFrame, top_n: int = 5) -> List[Dict]:
    top_transactions = df.nlargest(top_n, 'amount').to_dict(orient='records')
    return top_transactions


def load_user_settings() -> Dict:
    try:
        with open(USER_SETTINGS_PATH, "r") as f:
            settings = json.load(f)
    except FileNotFoundError:
        logging.error(f"User settings file not found: {USER_SETTINGS_PATH}")
        settings = {"user_currencies": [], "user_stocks": []}
    except json.JSONDecodeError:
        logging.error(f"Error decoding JSON from user settings file: {USER_SETTINGS_PATH}")
        settings = {"user_currencies": [], "user_stocks": []}
    return settings
