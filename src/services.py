import json
import logging
from datetime import datetime

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)


def cashback_analysis(data, year, month):
    """
    Анализирует данные транзакций и рассчитывает сумму кешбэка по категориям за указанный месяц и год.

    :param data: Список транзакций (каждая транзакция представлена словарем).
    :param year: Год для анализа.
    :param month: Месяц для анализа.
    :return: JSON с суммой кешбэка по категориям.
    """
    logging.info("Начало анализа кешбэка для %d-%02d", year, month)

    # Инициализируем словарь для хранения сумм кешбэка по категориям
    cashback_by_category = {}

    for transaction in data:
        try:
            # Парсинг даты операции
            transaction_date = datetime.strptime(
                transaction["Дата операции"], "%Y-%m-%d"
            )
            transaction_year = transaction_date.year
            transaction_month = transaction_date.month

            # Проверка соответствия года и месяца
            if transaction_year == year and transaction_month == month:
                category = transaction["Категория"]
                cashback = transaction.get("Кешбэк", 0)

                if category in cashback_by_category:
                    cashback_by_category[category] += cashback
                else:
                    cashback_by_category[category] = cashback

                logging.debug("Добавлен кешбэк %d для категории %s", cashback, category)
        except KeyError as e:
            logging.error("Ошибка доступа к ключу: %s", e)
        except ValueError as e:
            logging.error("Ошибка обработки даты: %s", e)

    logging.info("Анализ завершен. Найденные категории: %s", cashback_by_category)

    # Возвращаем результаты в формате JSON
    return json.dumps(cashback_by_category, ensure_ascii=False)
