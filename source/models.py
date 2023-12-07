from enum import Enum, IntEnum
from tortoise import Model
from tortoise.fields import TextField, BooleanField, ForeignKeyField, OnDelete, \
    ForeignKeyRelation, ReverseRelation, BigIntField, CharField, IntEnumField, CharEnumField


class CategoryLevel(IntEnum):
    lvl_1 = 1
    lvl_2 = 2
    lvl_3 = 3
    lvl_4 = 4
    lvl_5 = 5


class Category(Model):
    id = BigIntField(pk=True)
    user_id = CharField(max_length=100, index=True)
    parent: ForeignKeyRelation['Category'] = ForeignKeyField('models.Category', on_delete=OnDelete.CASCADE,
                                                             related_name="children", null=True)
    children: ReverseRelation["Category"]  # Связь один ко многим к самому себе (выводим дочерние элементы)
    counterparties: ReverseRelation['Counterparty']
    name = CharField(max_length=100)
    status = BooleanField(default=1, null=True)
    level = IntEnumField(enum_type=CategoryLevel, default=1, null=True, description="Уровень категории расходов")

    class Meta:
        table = "categories"

# ----------------------------------------------------------------------------------------------------------------------


class Counterparty(Model):
    id = BigIntField(pk=True)
    user_id = CharField(max_length=100, index=True)
    category: ForeignKeyRelation['Category'] = ForeignKeyField('models.Category',
                                                               on_delete=OnDelete.SET_NULL,
                                                               related_name="counterparties",
                                                               null=True)
    inn = CharField(max_length=12)
    name = CharField(max_length=100)

    class Meta:
        table = "counterparties"

# ----------------------------------------------------------------------------------------------------------------------


class NotifyGroup(Model):
    id = BigIntField(pk=True)
    user_id = CharField(max_length=100, index=True)
    chat_id = CharField(max_length=20, unique=True)
    name = TextField(maxlength=300)

    class Meta:
        table = "notification_groups"

# ----------------------------------------------------------------------------------------------------------------------


class PermissionName(str, Enum):
    report_request = 'report_request'
    buttons = 'buttons'


class PermissionAction(str, Enum):
    conciliate = 'conciliate'
    approve = 'approve'
    treasure = 'treasure'
    timekeep = 'timekeep'


class Permission(Model):
    id = BigIntField(pk=True)
    user_id = CharField(max_length=100, index=True)
    name = CharEnumField(enum_type=PermissionName, description='Название разрешения')
    action = CharEnumField(enum_type=PermissionAction, description='Наименование действия')

    class Meta:
        table = "permissions"

# ----------------------------------------------------------------------------------------------------------------------


class WalletNames(str, Enum):
    cash = 'Наличные'
    another = 'Другой'
    tinkoff = 'Тинькофф'
    module = 'Модуль'
    tochka = 'Точка'


class Wallet(Model):
    id = BigIntField(pk=True)
    user_id = CharField(max_length=100, index=True)
    name = CharEnumField(enum_type=WalletNames, description='Название')

    class Meta:
        table = "wallets"
