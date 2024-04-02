from datetime import date
from aerich import Command
from tortoise import Tortoise
from config import TORTOISE_CONFIG
from db_models.telegram import SupportWallet


async def init_db():
    if date(2024, 4, 2) == date.today():
        command = Command(tortoise_config=TORTOISE_CONFIG, app='telegram', location="./migrations")
        await command.init()
        await command.upgrade(True)

    await Tortoise.init(TORTOISE_CONFIG)
    await Tortoise.generate_schemas(safe=True)

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
