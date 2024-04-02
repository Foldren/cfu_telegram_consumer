from faststream.rabbit import RabbitRouter
from components.queues import telegram_queue

router = RabbitRouter()


# @router.subscriber(queue=telegram_queue)
# async def purge_messages():
#     pass
