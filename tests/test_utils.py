from unittest.mock import mock_open, patch

import pandas as pd
import pytest

from src.utils import (calculate_spending_and_cashback, fetch_currency_rates,
                       fetch_stock_prices, get_start_of_month,
                       get_top_transactions, load_user_settings)


# Тест для load_user_settings
@patch(
    "builtins.open",
    new_callable=mock_open,
    read_data='{"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "AMZN"]}',
)
def test_load_user_settings(mock_open):
    settings = load_user_settings("user_settings.json")
    assert settings == {
        "user_currencies": ["USD", "EUR"],
        "user_stocks": ["AAPL", "AMZN"],
    }


# Тест для get_start_of_month
def test_get_start_of_month():
    result = get_start_of_month("2024-08-20")
    assert result == "2024-08-01"


# Тест для calculate_spending_and_cashback
def test_calculate_spending_and_cashback():
    df = pd.DataFrame({"Сумма операции": [100.0, 200.0, 50.0]})
    total_spent, cashback = calculate_spending_and_cashback(df)
    assert total_spent == 350.0
    assert cashback == 3.5


# Тест для get_top_transactions
def test_get_top_transactions():
    df = pd.DataFrame(
        {
            "Дата операции": ["2024-08-20", "2024-08-21", "2024-08-22"],
            "Сумма платежа": [300.0, 200.0, 100.0],
            "Категория": ["Категория1", "Категория2", "Категория3"],
            "Описание": ["Описание1", "Описание2", "Описание3"],
        }
    )
    top_transactions = get_top_transactions(df)
    assert len(top_transactions) == 3
    assert top_transactions[0]["Сумма платежа"] == 300.0


# Тест для fetch_currency_rates
@patch("src.utils.requests.get")
def test_fetch_currency_rates(mock_requests_get):
    mock_response = {"rates": {"USD": 73.21, "EUR": 87.08}}
    mock_requests_get.return_value.json.return_value = mock_response
    currencies = ["USD", "EUR"]
    rates = fetch_currency_rates(currencies)
    assert len(rates) == 2
    assert rates[0]["currency"] == "USD"
    assert rates[0]["rate"] == 73.21


# Тест для fetch_stock_prices
@patch("src.utils.requests.get")
def test_fetch_stock_prices(mock_requests_get):
    mock_response = {"rates": {"AAPL": 150.12, "AMZN": 3173.18}}
    mock_requests_get.return_value.json.return_value = mock_response
    stocks = ["AAPL", "AMZN"]
    prices = fetch_stock_prices(stocks)
    assert len(prices) == 2
    assert prices[0]["stock"] == "AAPL"
    assert prices[0]["price"] == 150.12
