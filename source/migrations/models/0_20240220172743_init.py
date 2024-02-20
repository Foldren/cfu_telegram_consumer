from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "categories" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "user_id" VARCHAR(100),
    "name" VARCHAR(100) NOT NULL,
    "status" SMALLINT   DEFAULT 1,
    "parent_id" BIGINT REFERENCES "categories" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_categories_user_id_b282c5" ON "categories" ("user_id");
COMMENT ON COLUMN "categories"."status" IS 'hidden: 0\nactive: 1\nservice: 2';
CREATE TABLE IF NOT EXISTS "counterparties" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "user_id" VARCHAR(100) NOT NULL,
    "inn" VARCHAR(12) NOT NULL,
    "name" VARCHAR(100) NOT NULL,
    "category_id" BIGINT REFERENCES "categories" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_counterpart_user_id_5ba472" ON "counterparties" ("user_id");
CREATE TABLE IF NOT EXISTS "notification_groups" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "user_id" VARCHAR(100) NOT NULL,
    "chat_id" VARCHAR(20) NOT NULL UNIQUE,
    "name" TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS "idx_notificatio_user_id_7ad2ce" ON "notification_groups" ("user_id");
CREATE TABLE IF NOT EXISTS "permissions" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "user_id" VARCHAR(100) NOT NULL,
    "name" VARCHAR(14) NOT NULL,
    "action" VARCHAR(10) NOT NULL
);
CREATE INDEX IF NOT EXISTS "idx_permissions_user_id_9772d7" ON "permissions" ("user_id");
COMMENT ON COLUMN "permissions"."name" IS 'Название разрешения';
COMMENT ON COLUMN "permissions"."action" IS 'Наименование действия';
CREATE TABLE IF NOT EXISTS "support_wallets" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(8) NOT NULL
);
COMMENT ON COLUMN "support_wallets"."name" IS 'Название';
CREATE TABLE IF NOT EXISTS "data_collects" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "transaction_id" BIGINT NOT NULL,
    "executor_id" VARCHAR(100),
    "trxn_date" DATE NOT NULL,
    "type" VARCHAR(6) NOT NULL,
    "amount" DECIMAL(19,2) NOT NULL,
    "category_id" BIGINT REFERENCES "categories" ("id") ON DELETE CASCADE,
    "support_wallet_id" BIGINT NOT NULL REFERENCES "support_wallets" ("id") ON DELETE RESTRICT
);
CREATE INDEX IF NOT EXISTS "idx_data_collec_executo_96be07" ON "data_collects" ("executor_id");
CREATE INDEX IF NOT EXISTS "idx_data_collec_trxn_da_755215" ON "data_collects" ("trxn_date");
COMMENT ON COLUMN "data_collects"."type" IS 'Тип операции';
CREATE TABLE IF NOT EXISTS "user_wallets" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "user_id" VARCHAR(100) NOT NULL,
    "support_wallet_id" BIGINT NOT NULL REFERENCES "support_wallets" ("id") ON DELETE RESTRICT
);
CREATE INDEX IF NOT EXISTS "idx_user_wallet_user_id_18a33d" ON "user_wallets" ("user_id");
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
