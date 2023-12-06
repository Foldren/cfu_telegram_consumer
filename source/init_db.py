from tortoise import Tortoise
from config import POSTGRES_URL


async def init_db():
    await Tortoise.init(
        db_url=POSTGRES_URL,
        modules={'models': ["models"]},
    )
    # await Tortoise.generate_schemas(safe=True)
