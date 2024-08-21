import pytest
import pandas as pd
from src.reports import spending_by_category


def test_spending_by_category():
    """Тестирует функцию spending_by_category."""

    # Пример данных
    data = {
        "Дата операции": ["2024-05-15", "2024-06-10", "2024-07-20", "2024-08-01"],
        "Категория": ["Продукты", "Продукты", "Рестораны", "Продукты"],
        "Сумма операции": [1000, 1500, 2000, 1200],
    }
    df = pd.DataFrame(data)

    # Ожидаемый результат
    expected_result = {"Продукты": 2700}  # Траты за три месяца с 2024-08-01

    # Вызов функции с данными из теста
    result = spending_by_category(df, "Продукты", "2024-08-01")

    # Проверка на корректность результата
    assert result == expected_result, f"Expected {expected_result}, but got {result}"
