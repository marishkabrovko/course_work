import datetime
import json
import logging
from turtle import pd
from typing import Any, Callable, List, Optional

import pandas as pd

from src.decorators import decorator_spending_by_category
from src.read_excel import read_excel

logger = logging.getLogger("report.log")
file_handler = logging.FileHandler("report.log", "w")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def log_spending_by_category(filename: Any) -> Callable:
    """Логирует результат функции в указанный файл"""

    def decorator(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = func(*args, **kwargs).to_dict("records")
            with open(filename, "w") as f:
                json.dump(result, f, indent=4)
            return result

        return wrapper

    return decorator


@decorator_spending_by_category
def spending_by_category(
    transactions: pd.DataFrame, category: str, date: Optional[str] = None
) -> list[Any]:
    """Функция возвращающая траты за последние 3 месяца по заданной категории"""
    logger.info("Начало работы")
    list_by_category = []
    final_list = []
    if date is None:
        logger.info("Вариант обработки с настоящей датой")
        date_start = datetime.datetime.now() - datetime.timedelta(days=90)
        logger.info("Формирование списка по категории")
        for i in transactions:
            if i["Категория"] == category:
                list_by_category.append(i)
        logger.info("Фильтрация на пропущенные даты")
        for i in list_by_category:
            if i["Дата платежа"] == "nan" or type(i["Дата платежа"]) == float:
                continue
            elif (
                date_start
                <= datetime.datetime.strptime(str(i["Дата платежа"]), "%d.%m.%Y")
                <= date_start + datetime.timedelta(days=90)
            ):
                final_list.append(i["Сумма платежа"])
        return final_list
    else:
        logger.info("Вариант обработки с введенной датой")
        day, month, year = date.split(".")
        date_obj = datetime.datetime(int(year), int(month), int(day))
        date_start = date_obj - datetime.timedelta(days=90)
        logger.info("Формирование списка по категории")
        for i in transactions:
            if i["Категория"] == category:
                list_by_category.append(i)
        logger.info("Фильтрация на пропущенные даты")
        for i in list_by_category:
            if i["Дата платежа"] == "nan" or type(i["Дата платежа"]) == float:
                continue
            else:
                day_, month_, year_ = i["Дата платежа"].split(".")
                date_obj_ = datetime.datetime(int(year), int(month), int(day))
                if date_start <= date_obj_ <= date_start + datetime.timedelta(days=90):
                    final_list.append(i["Сумма платежа"])
                    logger.info("Формирование списка по тратам")
        return final_list
