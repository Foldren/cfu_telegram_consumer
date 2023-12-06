from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "categories" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "user_id" VARCHAR(100) NOT NULL,
    "name" VARCHAR(100) NOT NULL,
    "status" BOOL   DEFAULT True,
    "level" SMALLINT   DEFAULT 1,
    "parent_id" BIGINT REFERENCES "categories" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_categories_user_id_b282c5" ON "categories" ("user_id");
COMMENT ON COLUMN "categories"."level" IS 'Уровень категории расходов';
CREATE TABLE IF NOT EXISTS "contragents" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "user_id" VARCHAR(100) NOT NULL,
    "inn" VARCHAR(12) NOT NULL,
    "name" VARCHAR(100) NOT NULL,
    "category_id" BIGINT REFERENCES "categories" ("id") ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS "idx_contragents_user_id_99e211" ON "contragents" ("user_id");
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
CREATE TABLE IF NOT EXISTS "wallets" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "user_id" VARCHAR(100) NOT NULL,
    "name" VARCHAR(8) NOT NULL
);
CREATE INDEX IF NOT EXISTS "idx_wallets_user_id_3ba268" ON "wallets" ("user_id");
COMMENT ON COLUMN "wallets"."name" IS 'Название';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
