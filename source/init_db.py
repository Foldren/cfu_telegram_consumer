from datetime import date
from tortoise import Tortoise
from config import TORTOISE_CONFIG
from models import Category
from aerich import Command


async def init_db():
    await Tortoise.init(TORTOISE_CONFIG)
    await Tortoise.generate_schemas(safe=True)

    if date(2024, 2, 20) == date.today():
        command = Command(tortoise_config=TORTOISE_CONFIG, app='models', location="./migrations")
        await command.init()
        await command.upgrade(True)

    service_categories = await Category.filter(status=2).all()

    if not service_categories:
        service_categories_list = [
            Category(name="Перевод", status=2),
            Category(name="Выдача под отчет", status=2),
            Category(name="Получение под отчет", status=2),
            Category(name="Возврат подотчётных средств", status=2),
            Category(name="Получение подотчётных средств", status=2),
        ]

        await Category.bulk_create(service_categories_list)

