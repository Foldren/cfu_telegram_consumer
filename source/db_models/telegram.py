from enum import Enum, IntEnum
from tortoise import Model
from tortoise.fields import TextField, ForeignKeyField, OnDelete, \
    ForeignKeyRelation, ReverseRelation, BigIntField, CharField, CharEnumField, DecimalField, DateField, IntEnumField


class CategoryStatus(IntEnum):
    hidden = 0
    active = 1
    service = 2
    static = 3


class Category(Model):
    id = BigIntField(pk=True)
    user_id = CharField(max_length=100, index=True, null=True)
    parent: ForeignKeyRelation['Category'] = ForeignKeyField('telegram.Category', on_delete=OnDelete.CASCADE,
                                                             related_name="children", null=True)
    children: ReverseRelation["Category"]  # Связь один ко многим к самому себе (выводим дочерние элементы)
    counterparties: ReverseRelation['Counterparty']
    data_collects: ReverseRelation['DataCollect']
    name = CharField(max_length=100)
    status = IntEnumField(enum_type=CategoryStatus, default=1, null=True)

    class Meta:
        table = "categories"


# ----------------------------------------------------------------------------------------------------------------------


class Counterparty(Model):
    id = BigIntField(pk=True)
    user_id = CharField(max_length=100, index=True)
    category: ForeignKeyRelation['Category'] = ForeignKeyField('telegram.Category',
                                                               on_delete=OnDelete.CASCADE,
                                                               related_name="counterparties",
                                                               null=True)  # Если None, значит подгруженный
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


class WalletName(str, Enum):
    cash = 'Наличные'
    another = 'Другой'
    tinkoff = 'Тинькофф'
    module = 'Модуль'
    tochka = 'Точка'


class SupportWallet(Model):
    id = BigIntField(pk=True)
    name = CharEnumField(enum_type=WalletName, description='Название')
    user_wallets: ReverseRelation['UserWallet']
    data_collects: ReverseRelation['DataCollect']

    class Meta:
        table = "support_wallets"


# ----------------------------------------------------------------------------------------------------------------------


class UserWallet(Model):
    id = BigIntField(pk=True)
    user_id = CharField(max_length=100, index=True)
    support_wallet: ForeignKeyRelation['SupportWallet'] = ForeignKeyField('telegram.SupportWallet',
                                                                          on_delete=OnDelete.RESTRICT,
                                                                          related_name="user_wallets", null=False)

    class Meta:
        table = "user_wallets"


# ----------------------------------------------------------------------------------------------------------------------


class DataCollectType(str, Enum):
    income = "Доход"
    cost = "Расход"


class DataCollect(Model):
    id = BigIntField(pk=True)
    transaction: ForeignKeyRelation['Transaction'] = ForeignKeyField('telegram.Transaction',
                                                                     on_delete=OnDelete.CASCADE,
                                                                     related_name="data_collects")
    executor_id = CharField(max_length=100, index=True, null=True)  # id исполнителя (как legal_entity так и user_id)
    support_wallet: ForeignKeyRelation['SupportWallet'] = ForeignKeyField('telegram.SupportWallet',
                                                                          on_delete=OnDelete.RESTRICT,
                                                                          related_name="data_collects")
    category: ForeignKeyRelation['Category'] = ForeignKeyField('telegram.Category',
                                                               on_delete=OnDelete.CASCADE,
                                                               related_name="data_collects")
    type = CharEnumField(enum_type=DataCollectType, description='Тип операции')
    amount = DecimalField(max_digits=19, decimal_places=2)

    class Meta:
        table = "data_collects"


# ----------------------------------------------------------------------------------------------------------------------


class Transaction(Model):
    id = BigIntField(pk=True)
    date = DateField(index=True)
    data_collects: ReverseRelation['DataCollect']
