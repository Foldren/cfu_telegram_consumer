from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "data_collects" ADD "transaction_id_id" BIGINT NOT NULL;
        ALTER TABLE "data_collects" DROP COLUMN "trxn_date";
        ALTER TABLE "data_collects" DROP COLUMN "transaction_id";
        ALTER TABLE "data_collects" ALTER COLUMN "category_id" SET NOT NULL;
        CREATE TABLE IF NOT EXISTS "transaction" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "date" DATE NOT NULL
);
CREATE INDEX IF NOT EXISTS "idx_transaction_date_efa78f" ON "transaction" ("date");
        ALTER TABLE "data_collects" ADD CONSTRAINT "fk_data_col_transact_c130e111" FOREIGN KEY ("transaction_id_id") REFERENCES "transaction" ("id") ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "data_collects" DROP CONSTRAINT "fk_data_col_transact_c130e111";
        ALTER TABLE "data_collects" ADD "trxn_date" DATE NOT NULL;
        ALTER TABLE "data_collects" ADD "transaction_id" BIGINT NOT NULL;
        ALTER TABLE "data_collects" DROP COLUMN "transaction_id_id";
        ALTER TABLE "data_collects" ALTER COLUMN "category_id" DROP NOT NULL;
        DROP TABLE IF EXISTS "transaction";"""
