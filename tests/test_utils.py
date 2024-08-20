import pytest
import pandas as pd
from src.utils import (
    parse_date,
    generate_greeting,
    get_start_of_month,
    calculate_spending_and_cashback,
    get_top_transactions,
    load_user_settings
)
import json


@pytest.fixture
def mock_user_settings(tmp_path):
    settings = {
        "user_currencies": ["USD", "EUR"],
        "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    }
    settings_file = tmp_path / "user_settings.json"
    with settings_file.open("w") as f:
        json.dump(settings, f)
    return settings_file


@pytest.mark.parametrize(
    "date_time_str, expected",
    [
        ("2023-08-20 14:30:00", (2023, 8, 20, 14, 30, 0)),
        ("2021-12-01 00:00:00", (2021, 12, 1, 0, 0, 0))
    ]
)
def test_parse_date(date_time_str, expected):
    assert parse_date(date_time_str) == expected


@pytest.mark.parametrize(
    "hour, expected_greeting",
    [
        (6, "Доброе утро"),
        (13, "Добрый день"),
        (19, "Добрый вечер"),
        (23, "Доброй ночи"),
        (4, "Доброй ночи")
    ]
)
def test_generate_greeting(hour, expected_greeting):
    assert generate_greeting(hour) == expected_greeting


@pytest.mark.parametrize(
    "year, month, expected_start",
    [
        (2023, 8, "2023-08-01"),
        (2021, 12, "2021-12-01")
    ]
)
def test_get_start_of_month(year, month, expected_start):
    assert get_start_of_month(year, month) == expected_start


@pytest.mark.parametrize(
    "amounts, expected_total, expected_cashback",
    [
        ([100.0, 200.0, 300.0], 600.0, 6.0),
        ([500.0, 700.0], 1200.0, 12.0)
    ]
)
def test_calculate_spending_and_cashback(amounts, expected_total, expected_cashback):
    df = pd.DataFrame({"amount": amounts})
    total_spent, cashback = calculate_spending_and_cashback(df)
    assert total_spent == expected_total
    assert cashback == expected_cashback


def test_get_top_transactions():
    data = {
        "date": ["2023-08-01", "2023-08-15", "2023-08-20"],
        "amount": [100.0, 200.0, 300.0],
        "category": ["Категория1", "Категория2", "Категория3"],
        "description": ["Описание1", "Описание2", "Описание3"]
    }
    df = pd.DataFrame(data)
    top_transactions = get_top_transactions(df, top_n=2)
    assert len(top_transactions) == 2
    assert top_transactions[0]['amount'] == 300.0
    assert top_transactions[1]['amount'] == 200.0


def test_load_user_settings(mock_user_settings, monkeypatch):
    monkeypatch.setattr("utils.USER_SETTINGS_PATH", str(mock_user_settings))
    settings = load_user_settings()
    assert settings["user_currencies"] == ["USD", "EUR"]
    assert settings["user_stocks"] == ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
