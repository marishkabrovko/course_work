import pytest
import pandas as pd
from unittest.mock import patch
from src.reports import spending_by_category

# Фикстура с данными, имитирующими содержание operations.xlsx
@pytest.fixture
def sample_transactions():
    data = {
        "Дата операции": ["31.12.2021 16:44:00", "31.12.2021 16:44:00"],
        "Дата платежа": ["31.12.2021", "31.12.2021"],
        "Номер карты": ["*7197", "*7197"],
        "Статус": ["OK", "OK"],
        "Сумма платежа": [-160.89, -200.00],
        "Категория": ["Супермаркеты", "Переводы"],
        "Кэшбэк": [3.0, 4.0],
        "Описание": ["Колхоз", "Трансфер"],
        "Бонусы (включая кэшбэк)": [3, 4],
    }
    return pd.DataFrame(data)

# Параметризованный тест для проверки различных категорий
@pytest.mark.parametrize(
    "category, date, expected_spent, expected_cashback",
    [
        ("Переводы", "31.12.2021", 200.0, 4.0),
        ("Супермаркеты", "31.12.2021", 160.89, 3.0),
        ("Несуществующая категория", "31.12.2021", 0.0, 0.0),
    ],
)
@patch("src.reports.calculate_spending_and_cashback")
@patch("src.reports.get_top_transactions")
@patch("src.reports.load_user_settings")
@patch("src.reports.fetch_currency_rates")
@patch("src.reports.fetch_stock_prices")
@patch("pandas.read_excel")
def test_spending_by_category(
    mock_read_excel,
    mock_fetch_stock_prices,
    mock_fetch_currency_rates,
    mock_load_user_settings,
    mock_get_top_transactions,
    mock_calculate_spending_and_cashback,
    sample_transactions,
    category,
    date,
    expected_spent,
    expected_cashback,
):
    # Настраиваем mock-объект для чтения Excel-файла
    mock_read_excel.return_value = sample_transactions

    # Настраиваем mock-объекты для остальных зависимостей
    mock_calculate_spending_and_cashback.return_value = (expected_spent, expected_cashback)
    mock_get_top_transactions.return_value = sample_transactions.to_dict(orient="records")
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

    # Вызов тестируемой функции
    result = spending_by_category(sample_transactions, category, date)

    # Проверка результата
    assert result["cards"][0]["total_spent"] == expected_spent
    assert result["cards"][0]["cashback"] == expected_cashback
    assert len(result["top_transactions"]) == len(mock_get_top_transactions.return_value)

