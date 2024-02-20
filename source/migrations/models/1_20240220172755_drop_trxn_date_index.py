from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX "idx_data_collec_trxn_da_755215";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE INDEX "idx_data_collec_trxn_da_755215" ON "data_collects" ("trxn_date");"""
