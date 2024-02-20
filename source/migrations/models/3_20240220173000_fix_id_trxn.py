from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "data_collects" DROP CONSTRAINT "fk_data_col_transact_c130e111";
        ALTER TABLE "data_collects" RENAME COLUMN "transaction_id_id" TO "transaction_id";
        ALTER TABLE "data_collects" ADD CONSTRAINT "fk_data_col_transact_40ca7f48" FOREIGN KEY ("transaction_id") REFERENCES "transaction" ("id") ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "data_collects" DROP CONSTRAINT "fk_data_col_transact_40ca7f48";
        ALTER TABLE "data_collects" RENAME COLUMN "transaction_id" TO "transaction_id_id";
        ALTER TABLE "data_collects" ADD CONSTRAINT "fk_data_col_transact_c130e111" FOREIGN KEY ("transaction_id_id") REFERENCES "transaction" ("id") ON DELETE CASCADE;"""
