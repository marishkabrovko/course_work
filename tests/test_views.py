import pytest
import json
from unittest.mock import patch
from src.views import main_page


# Тест для функции main_page
@patch('src.views.load_user_settings')
@patch('src.views.get_start_of_month')
@patch('src.views.calculate_spending_and_cashback')
@patch('src.views.get_top_transactions')
@patch('src.views.fetch_currency_rates')
@patch('src.views.fetch_stock_prices')
def test_main_page(mock_fetch_stock_prices, mock_fetch_currency_rates, mock_get_top_transactions,
                   mock_calculate_spending_and_cashback, mock_get_start_of_month, mock_load_user_settings):
    # Мокируем возвращаемые значения
    mock_load_user_settings.return_value = {
        "user_currencies": ["USD", "EUR"],
        "user_stocks": ["AAPL", "AMZN"]
    }

    mock_get_start_of_month.return_value = "2024-08-01"

    mock_calculate_spending_and_cashback.return_value = (600.0, 6.0)

    mock_get_top_transactions.return_value = [
        {"date": "2024-08-01", "amount": 300.0, "category": "Категория1", "description": "Описание1"},
        {"date": "2024-08-15", "amount": 200.0, "category": "Категория2", "description": "Описание2"},
        {"date": "2024-08-20", "amount": 100.0, "category": "Категория3", "description": "Описание3"}
    ]

    mock_fetch_currency_rates.return_value = [
        {"currency": "USD", "rate": 73.21},
        {"currency": "EUR", "rate": 87.08}
    ]

    mock_fetch_stock_prices.return_value = [
        {"stock": "AAPL", "price": 150.12},
        {"stock": "AMZN", "price": 3173.18}
    ]

    # Вызов тестируемой функции
    date_time_str = "2024-08-20 15:30:00"
    response = main_page(date_time_str)
    response_json = json.loads(response)

    # Проверка содержимого JSON-ответа
    assert response_json["greeting"] == "Добрый день"
    assert response_json["cards"][0]["total_spent"] == 600.0
    assert response_json["cards"][0]["cashback"] == 6.0

    assert len(response_json["top_transactions"]) == 3
    assert response_json["top_transactions"][0]["amount"] == 300.0

    assert len(response_json["currency_rates"]) == 2
    assert response_json["currency_rates"][0]["currency"] == "USD"
    assert response_json["currency_rates"][0]["rate"] == 73.21

    assert len(response_json["stock_prices"]) == 2
    assert response_json["stock_prices"][0]["stock"] == "AAPL"
    assert response_json["stock_prices"][0]["price"] == 150.12

    # Запуск тестов
    if __name__ == "__main__":
        pytest.main()
