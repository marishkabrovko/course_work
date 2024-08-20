import requests
from utils import load_user_settings, get_currency_rates, get_stock_prices, get_transactions, generate_greeting, \
    calculate_spending_and_cashback, get_top_transactions, parse_date, get_start_of_month


def main_page(date_time_str):
    year, month, day, hour, _, _ = parse_date(date_time_str)
    greeting = generate_greeting(hour)
    user_settings = load_user_settings()
    currency_rates = get_currency_rates(user_settings['user_currencies'])
    stock_prices = get_stock_prices(user_settings['user_stocks'])

    start_date = get_start_of_month(year, month)
    end_date = f"{year:04d}-{month:02d}-{day:02d}"
    transactions = get_transactions('data/operations.xlsx', start_date, end_date)

    cards_info = []
    for card_last_digits in transactions['card_last_digits'].unique():
        card_transactions = transactions[transactions['card_last_digits'] == card_last_digits]
        total_spent, cashback = calculate_spending_and_cashback(card_transactions)
        cards_info.append({
            "last_digits": card_last_digits,
            "total_spent": total_spent,
            "cashback": cashback
        })

    top_transactions = get_top_transactions(transactions)

    response = {
        "greeting": greeting,
        "cards": cards_info,
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices
    }

    return response
