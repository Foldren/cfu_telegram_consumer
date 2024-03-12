from asyncio import run
from faststream import FastStream
from faststream.rabbit import RabbitBroker
from tortoise import run_async
from config import RABBITMQ_URL
from init_db import init_db
from routers import category, counterparty, purge, custom

broker = RabbitBroker(RABBITMQ_URL)
app = FastStream(broker)

broker.include_routers(purge.router, category.router, counterparty.router, custom.router)


async def main():
    await app.run()


if __name__ == "__main__":
    run_async(init_db())
    run(main())
