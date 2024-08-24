from datetime import datetime

import pandas as pd

from src.reports import spending_by_category
from src.services import cashback_analysis
from src.utils import (calculate_spending_and_cashback, fetch_currency_rates,
                       fetch_stock_prices, get_top_transactions,
                       load_user_settings)
# Импорт функций из модулей
from src.views import main_page


def load_transactions(file_path):
    """Загружает данные транзакций из файла Excel."""
    try:
        transactions = pd.read_excel(file_path)
        return transactions
    except FileNotFoundError as e:
        print(f"Файл данных не найден: {e}")
        return None
    except Exception as e:
        print(f"Ошибка при чтении файла данных: {e}")
        return None


def run_main_page():
    """Выполняет операции для отображения главной страницы."""
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    transactions = load_transactions("data/operations.xlsx")

    if transactions is not None:
        result = main_page(transactions, current_datetime)
        print("Результат работы главной страницы:")
        print(result)


def run_spending_by_category():
    """Запускает анализ трат по категории."""
    transactions = load_transactions("data/operations.xlsx")
    if transactions is not None:
        category = "Супермаркеты"  # Пример категории
        result = spending_by_category(transactions, category)
        print("Результат анализа трат по категории:")
        print(result)


def run_cashback_analysis():
    """Запускает анализ кешбэка по категориям."""
    transactions = load_transactions("data/operations.xlsx")
    if transactions is not None:
        year = 2023
        month = 8
        result = cashback_analysis(transactions, year, month)
        print("Результат анализа кешбэка:")
        print(result)


def main():
    """Основная функция для запуска всех частей проекта."""
    print("Запуск главной страницы...")
    run_main_page()

    print("\nЗапуск анализа трат по категории...")
    run_spending_by_category()

    print("\nЗапуск анализа кешбэка...")
    run_cashback_analysis()


if __name__ == "__main__":
    main()
