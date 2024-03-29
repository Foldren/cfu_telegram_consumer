from os import environ, getcwd
from dotenv import load_dotenv


load_dotenv()

IS_THIS_LOCAL = "Pycharm" in str(getcwd())

TELEGRAM_QUEUE = "telegram_queue"

RABBITMQ_URL = environ['RABBITMQ_URL']

TORTOISE_CONFIG = {
    "connections": {
        "telegram": environ['TG_PG_URL'],
        "bank": environ['BANK_PG_URL']
    },
    "apps": {
        "telegram": {"models": ["db_models.telegram", "aerich.models"], "default_connection": "telegram"},
        "bank": {"models": ["db_models.bank"], "default_connection": "bank"}
    }
}

INN_MARKETPLACES = [9701048328, 7705935687, 7721546864, 7704217370, 7704357909]

# Для операций в телеграм боте
SERVICE_CATEGORIES = ["Выдача в подотчет", "Возврат подотчета"]

# Не редактируемые категории
STATIC_CATEGORIES = ["Зарплата", "Аренда", "Упаковка"]
