from tortoise import Tortoise
from config import TORTOISE_CONFIG


async def init_db():
    await Tortoise.init(TORTOISE_CONFIG)
    await Tortoise.generate_schemas(safe=True)
