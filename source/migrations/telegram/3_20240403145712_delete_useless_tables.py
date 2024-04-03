from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "data_collects" DROP CONSTRAINT IF EXISTS "fk_data_col_support__e5a55a62";
        ALTER TABLE "data_collects" DROP COLUMN "support_wallet_id";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "data_collects" ADD "support_wallet_id" BIGINT NOT NULL;
        ALTER TABLE "data_collects" ADD CONSTRAINT "fk_data_col_support__e5a55a62" FOREIGN KEY ("support_wallet_id") REFERENCES "support_wallets" ("id") ON DELETE RESTRICT;"""
