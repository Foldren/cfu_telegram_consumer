from os import environ, getcwd
from dotenv import load_dotenv

load_dotenv()

IS_THIS_LOCAL = "Pycharm" in str(getcwd())
TELEGRAM_QUEUE = "telegram_queue"
RABBITMQ_URL = environ['RABBITMQ_URL']
TORTOISE_CONFIG = {
    "connections": {"default": 'postgres://test_admin:8QzjHW9y_07qExB9OydT36u6CqkbI4@188.120.240.205:2000/test'},
    "apps": {
        "models": {
            "models": ["models", "aerich.models"],
            "default_connection": "default"
        }
    }
}
