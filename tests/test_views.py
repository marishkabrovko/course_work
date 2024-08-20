import pytest
import json
from unittest.mock import patch
from src.views import main_page
import pandas as pd


@pytest.fixture
def mock_excel_data(tmp_path):
    data = {
        "date": ["2023-08-01", "2023-08-15", "2023-08-20"],
        "amount": [100.0, 200.0, 300.0],
        "category": ["Категория1", "Категория2", "Категория3"],
        "description": ["Описание1", "Описание2", "Описание3"]
    }
    df = pd.DataFrame(data)
    excel_file = tmp_path / "operations.xlsx"
    df.to_excel(excel_file, index=False)
    return excel_file


@patch('src.views.fetch_currency_rates')
@patch('src.views.fetch_stock_prices')
@patch('src.utils.load_user_settings')
@patch('pandas.read_excel')
@patch('requests.get')
def test_main_page(mock_requests_get, mock_read_excel, mock_load_user_settings, mock_fetch_stock_prices,
                   mock_fetch_currency_rates, mock_excel_data):
    def mock_requests_get_side_effect(url, headers=None):
        if "latest" in url:
            return MockResponse({
                "rates": {
                    "USD": 73.21,
                    "EUR": 87.08
                }
            }, 200)
        elif "stocks" in url:
            return MockResponse({
                "AAPL": 150.12,
                "AMZN": 3173.18
            }, 200)
        return MockResponse({}, 404)

    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    mock_requests_get.side_effect = mock_requests_get_side_effect

    mock_read_excel.return_value = pd.read_excel(mock_excel_data)
    mock_load_user_settings.return_value = {
        "user_currencies": ["USD", "EUR"],
        "user_stocks": ["AAPL", "AMZN"]
    }
    mock_fetch_currency_rates.return_value = [
        {"currency": "USD", "rate": 73.21},
        {"currency": "EUR", "rate": 87.08}
    ]
    mock_fetch_stock_prices.return_value = [
        {"stock": "AAPL", "price": 150.12},
        {"stock": "AMZN", "price": 3173.18}
    ]

    response_json = main_page("2023-08-20 14:30:00")
    response = json.loads(response_json)

    assert response["greeting"] == "Добрый день"
    assert len(response["cards"]) == 1
    assert response["cards"][0]["total_spent"] == 600.0
    assert response["cards"][0]["cashback"] == 6.0
    assert len(response["top_transactions"]) == 3
    assert response["currency_rates"][0]["currency"] == "USD"
    assert response["stock_prices"][0]["stock"] == "AAPL"
