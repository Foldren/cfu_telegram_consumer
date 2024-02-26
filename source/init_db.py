from datetime import date
from tortoise import Tortoise
from config import TORTOISE_CONFIG
from models import SupportWallet
from aerich import Command


async def init_db():
    await Tortoise.init(TORTOISE_CONFIG)
    await Tortoise.generate_schemas(safe=True)

    # if date(2024, 2, 22) == date.today():
    #     command = Command(tortoise_config=TORTOISE_CONFIG, app='models', location="./migrations")
    #     await command.init()
    #     await command.upgrade(True)

    support_wallets = await SupportWallet.all()

    if not support_wallets:
        support_wallets_obj = [
            SupportWallet(name='Наличные'),
            SupportWallet(name='Другой'),
            SupportWallet(name='Тинькофф'),
            SupportWallet(name='Модуль'),
            SupportWallet(name='Точка')
        ]
        await SupportWallet.bulk_create(support_wallets_obj, ignore_conflicts=True)
