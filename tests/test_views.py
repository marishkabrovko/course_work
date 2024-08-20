import pytest
from src.views import main_page
from src.utils import load_user_settings


@pytest.fixture
def mock_user_settings(monkeypatch):
    mock_settings = {
        "user_currencies": ["USD", "EUR"],
        "user_stocks": ["AAPL", "AMZN"]
    }
    monkeypatch.setattr("utils.load_user_settings", lambda: mock_settings)


@pytest.fixture
def mock_currency_rates(monkeypatch):
    mock_rates = [
        {"currency": "USD", "rate": 73.21},
        {"currency": "EUR", "rate": 87.08}
    ]
    monkeypatch.setattr("utils.get_currency_rates", lambda x: mock_rates)


@pytest.fixture
def mock_stock_prices(monkeypatch):
    mock_prices = [
        {"stock": "AAPL", "price": 150.12},
        {"stock": "AMZN", "price": 3173.18}
    ]
    monkeypatch.setattr("utils.get_stock_prices", lambda x: mock_prices)


@pytest.fixture
def mock_transactions(monkeypatch):
    import pandas as pd
    data = {
        "date": ["2023-08-01", "2023-08-15", "2023-08-20"],
        "card_last_digits": ["1234", "1234", "5678"],
        "amount": [100.0, 200.0, 300.0]
    }
    df = pd.DataFrame(data)
    monkeypatch.setattr("utils.get_transactions", lambda x, y, z: df)


def test_main_page(mock_user_settings, mock_currency_rates, mock_stock_prices, mock_transactions):
    date_time_str = "2023-08-20 14:30:00"
    response = main_page(date_time_str)

    assert response['greeting'] == "Добрый день"

    assert len(response['cards']) == 2
    assert response['cards'][0]['last_digits'] == "1234"
    assert response['cards'][0]['total_spent'] == 300.0
    assert response['cards'][0]['cashback'] == 3.0

    assert len(response['currency_rates']) == 2
    assert response['currency_rates'][0]['currency'] == "USD"
    assert response['currency_rates'][0]['rate'] == 73.21

    assert len(response['stock_prices']) == 2
    assert response['stock_prices'][0]['stock'] == "AAPL"
    assert response['stock_prices'][0]['price'] == 150.12


def test_parse_date():
    from src.utils import parse_date
    date_time_str = "2023-08-20 14:30:00"
    year, month, day, hour, minute, second = parse_date(date_time_str)
    assert year == 2023
    assert month == 8
    assert day == 20
    assert hour == 14
    assert minute == 30
    assert second == 0


def test_generate_greeting():
    from src.utils import generate_greeting
    assert generate_greeting(6) == "Доброе утро"
    assert generate_greeting(13) == "Добрый день"
    assert generate_greeting(19) == "Добрый вечер"
    assert generate_greeting(23) == "Доброй ночи"
