from faststream.rabbit import RabbitRouter

router = RabbitRouter()


# @router.subscriber(queue=telegram_queue)
# async def purge_messages():
#     pass
