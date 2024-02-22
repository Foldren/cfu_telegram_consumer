from os import environ, getcwd
from dotenv import load_dotenv

load_dotenv()

IS_THIS_LOCAL = "Pycharm" in str(getcwd())
TELEGRAM_QUEUE = "telegram_queue"
RABBITMQ_URL = environ['RABBITMQ_URL']
TORTOISE_CONFIG = {
    "connections": {
        "default": #{
        #     "engine": "tortoise.backends.sqlite",
        #     "credentials": {
        #         "file_path": environ['SQLITE_URL'],
        #         "foreign_keys": "ON",
        #     },
        # }
        environ['PG_TEST_URL'] if IS_THIS_LOCAL else environ['PG_URL']
        # Если не локальная авторизуемся по ссылке
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
