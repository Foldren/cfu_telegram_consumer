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

# Для операций в телеграм боте
SERVICE_CATEGORIES = [
    "Выдача в подотчет", "Возврат подотчета"
]

# Не редактируемые категории
STATIC_CATEGORIES = [
    "Зарплата", "Аренда", "Упаковка"
]
