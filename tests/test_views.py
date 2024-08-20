from unittest.mock import patch

import pandas as pd
import pytest

from src.views import main_page


@patch("src.views.pd.read_excel")
@patch("src.views.calculate_spending_and_cashback")
@patch("src.views.get_top_transactions")
@patch("src.views.fetch_currency_rates")
@patch("src.views.fetch_stock_prices")
@patch("src.views.load_user_settings")
def test_main_page(
    mock_load_user_settings,
    mock_fetch_stock_prices,
    mock_fetch_currency_rates,
    mock_get_top_transactions,
    mock_calculate_spending_and_cashback,
    mock_read_excel,
):
    # Настроим моки
    mock_load_user_settings.return_value = {
        "user_currencies": ["USD", "EUR"],
        "user_stocks": ["AAPL", "AMZN"],
    }

    mock_fetch_currency_rates.return_value = [
        {"currency": "USD", "rate": 73.21},
        {"currency": "EUR", "rate": 87.08},
    ]

    mock_fetch_stock_prices.return_value = [
        {"stock": "AAPL", "price": 150.12},
        {"stock": "AMZN", "price": 3173.18},
    ]

    # Создание DataFrame для тестирования
    df = pd.DataFrame(
        {
            "Дата операции": ["2024-08-01", "2024-08-10", "2024-08-20"],
            "Сумма операции": [100.0, 200.0, 300.0],
            "Сумма платежа": [100.0, 200.0, 300.0],
            "Категория": ["Категория1", "Категория2", "Категория3"],
            "Описание": ["Описание1", "Описание2", "Описание3"],
        }
    )
    mock_read_excel.return_value = df

    mock_calculate_spending_and_cashback.return_value = (600.0, 6.0)

    mock_get_top_transactions.return_value = [
        {
            "Дата операции": "2024-08-20",
            "Сумма платежа": 300.0,
            "Категория": "Категория3",
            "Описание": "Описание3",
        },
        {
            "Дата операции": "2024-08-10",
            "Сумма платежа": 200.0,
            "Категория": "Категория2",
            "Описание": "Описание2",
        },
    ]

    # Запрос к функции
    response = main_page("2024-08-20 15:00:00")

    # Проверка ответа
    assert response["greeting"] == "Добрый день"
    assert response["cards"][0]["total_spent"] == 600.0
    assert response["currency_rates"][0]["currency"] == "USD"
    assert response["stock_prices"][0]["stock"] == "AAPL"
