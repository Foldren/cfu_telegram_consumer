from os import environ, getcwd
from dotenv import load_dotenv

load_dotenv()

IS_THIS_LOCAL = "Pycharm" in str(getcwd())

TELEGRAM_QUEUE = "telegram_queue"

RABBITMQ_URL = environ['RABBITMQ_URL']

TORTOISE_CONFIG = {
    "connections": {
        "default": environ['PG_URL']
    },
    "apps": {
        "models": {
            "models": ["models", "aerich.models"],
            "default_connection": "default"
        }
    }
}

SERVICE_CATEGORIES = [
    # Для виджета платформы
    "Выручка от маркетплейсов", "Прочая выручка", "Себестоимость", "Зарплата", "Аренда",
    "Реклама", "Персонал", "Хозтовары",
    # Для операций в телеграм боте
    "Выдача в подотчет", "Возврат подотчета"
]
