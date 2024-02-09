from os import environ, getcwd
from dotenv import load_dotenv


IS_THIS_LOCAL = "Pycharm" in str(getcwd()); load_dotenv() if IS_THIS_LOCAL else None
TELEGRAM_QUEUE = "telegram_queue"
POSTGRES_URL = environ['POSTGRES_URL']
RABBITMQ_URL = environ['RABBITMQ_URL']
AERICH_CONFIG = {
    "connections": {"default": environ['POSTGRES_URL']},
    "apps": {
        "models": {
            "models": ["source.models", "aerich.models"],
            "default_connection": "default"
        },
    }
}
