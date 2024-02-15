from os import environ, getcwd
from dotenv import load_dotenv

load_dotenv()

IS_THIS_LOCAL = "Pycharm" in str(getcwd())
TELEGRAM_QUEUE = "telegram_queue"
RABBITMQ_URL = environ['RABBITMQ_URL']
TORTOISE_CONFIG = {
    "connections": {"default": environ['CFU_TEL_CON_PG_URL']},
    "apps": {
        "models": {
            "models": ["source.models", "aerich.models"],
            "default_connection": "default"
        }
    }
}
