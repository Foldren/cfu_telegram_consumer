from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "permissions";
        DROP TABLE IF EXISTS "user_wallets";
        DROP TABLE IF EXISTS "notification_groups";
        DROP TABLE IF EXISTS "support_wallets";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ;"""
