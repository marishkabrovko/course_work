import json
from datetime import datetime
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
            "Дата операции": datetime(2024, 8, 20),
            "Сумма платежа": 300.0,
            "Категория": "Категория3",
            "Описание": "Описание3",
        },
        {
            "Дата операции": datetime(2024, 8, 10),
            "Сумма платежа": 200.0,
            "Категория": "Категория2",
            "Описание": "Описание2",
        },
    ]

    # Запрос к функции
    response = main_page(df, "2024-08-20 15:00:00")

    # Преобразование ответа из JSON строки в Python объект
    response_json = json.loads(response)

    # Проверка результатов
    assert isinstance(
        response_json, dict
    )  # Убедитесь, что возвращается словарь (после загрузки JSON)
    assert "greeting" in response_json
    assert "cards" in response_json
    assert "top_transactions" in response_json
    assert "currency_rates" in response_json
    assert "stock_prices" in response_json

    # Дополнительные проверки в зависимости от содержания вашего ответа
    assert response_json["greeting"] == "Добрый день"  # Проверьте приветствие
    assert len(response_json["cards"]) == 2  # Убедитесь, что количество карточек верно
    assert response_json["cards"][0]["total_spent"] == 600.0  # Проверьте сумму расходов
    assert response_json["cards"][0]["cashback"] == 6.0  # Проверьте кэшбэк

    # Проверка топовых транзакций
    assert len(response_json["top_transactions"]) == 2
    assert response_json["top_transactions"][0]["amount"] == 300.0
    assert response_json["top_transactions"][0]["category"] == "Категория3"
    assert response_json["top_transactions"][0]["description"] == "Описание3"
