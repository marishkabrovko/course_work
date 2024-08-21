import pytest
import json
from src.services import cashback_analysis


def test_cashback_analysis():
    """Тестирует функцию cashback_analysis."""

    # Пример данных
    data = [
        {"Дата операции": "2024-08-01", "Категория": "Продукты", "Кешбэк": 50},
        {"Дата операции": "2024-08-15", "Категория": "Рестораны", "Кешбэк": 100},
        {"Дата операции": "2024-08-20", "Категория": "Продукты", "Кешбэк": 75},
        {"Дата операции": "2024-07-10", "Категория": "Продукты", "Кешбэк": 20},
    ]

    expected_result = {"Продукты": 125, "Рестораны": 100}

    result = cashback_analysis(data, 2024, 8)

    assert (
        json.loads(result) == expected_result
    ), f"Expected {expected_result}, but got {json.loads(result)}"
