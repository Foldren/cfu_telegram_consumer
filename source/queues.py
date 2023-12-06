from faststream.rabbit import RabbitQueue
from config import TELEGRAM_QUEUE


telegram_queue = RabbitQueue(name=TELEGRAM_QUEUE)  # , robust=False, durable=True)
