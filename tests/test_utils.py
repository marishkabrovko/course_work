import pytest
import json
from unittest.mock import patch
from src.utils import (
    parse_date,
    generate_greeting,
    get_start_of_month,
    calculate_spending_and_cashback,
    get_top_transactions,
    load_user_settings
)
import pandas as pd


# Тест для функции parse_date
def test_parse_date():
    date_time_str = "2023-08-20 14:30:00"
    year, month, day, hour, minute, second = parse_date(date_time_str)
    assert (year, month, day, hour, minute, second) == (2023, 8, 20, 14, 30, 0)


# Тест для функции generate_greeting
def test_generate_greeting():
    assert generate_greeting(8) == "Доброе утро"
    assert generate_greeting(13) == "Добрый день"
    assert generate_greeting(19) == "Добрый вечер"
    assert generate_greeting(23) == "Доброй ночи"


# Тест для функции get_start_of_month
def test_get_start_of_month():
    start_date = get_start_of_month(2023, 8)
    assert start_date == "2023-08-01"


# Тест для функции calculate_spending_and_cashback
@patch('pandas.read_excel')
def test_calculate_spending_and_cashback(mock_read_excel):
    data = {
        "date": ["2023-08-01", "2023-08-15", "2023-08-20"],
        "amount": [100.0, 200.0, 300.0],
        "category": ["Категория1", "Категория2", "Категория3"],
        "description": ["Описание1", "Описание2", "Описание3"]
    }
    df = pd.DataFrame(data)
    mock_read_excel.return_value = df
    df_filtered = df[df['date'] <= "2023-08-20"]
    total_spent, cashback = calculate_spending_and_cashback(df_filtered)
    assert total_spent == 600.0
    assert cashback == 6.0


# Тест для функции get_top_transactions
@patch('pandas.read_excel')
def test_get_top_transactions(mock_read_excel):
    data = {
        "date": ["2023-08-01", "2023-08-15", "2023-08-20"],
        "amount": [100.0, 200.0, 300.0],
        "category": ["Категория1", "Категория2", "Категория3"],
        "description": ["Описание1", "Описание2", "Описание3"]
    }
    df = pd.DataFrame(data)
    mock_read_excel.return_value = df
    df_filtered = df[df['date'] <= "2023-08-20"]
    top_transactions = get_top_transactions(df_filtered, top_n=3)
    assert len(top_transactions) == 3
    assert top_transactions[0]['amount'] == 300.0


# Тест для функции load_user_settings
@patch('builtins.open', new_callable=pytest.mock.mock_open, read_data='{"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "AMZN"]}')
def test_load_user_settings(mock_open):
    settings = load_user_settings()
    assert settings["user_currencies"] == ["USD", "EUR"]
    assert settings["user_stocks"] == ["AAPL", "AMZN"]
