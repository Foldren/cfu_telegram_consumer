from datetime import datetime
from enum import IntEnum, Enum
from tortoise import Model
from tortoise.fields import BigIntField, ForeignKeyRelation, ForeignKeyField, ReverseRelation, TextField, OnDelete, \
    BinaryField, DateField, IntEnumField, CharField, CharEnumField, DecimalField
from tortoise.timezone import now


class SupportBankName(str, Enum):
    tinkoff = "Тинькофф"
    module = "Модуль"
    tochka = "Точка"


class SupportBank(Model):
    id = BigIntField(pk=True)
    name = CharEnumField(enum_type=SupportBankName, description='Название банка')
    logo_url = TextField(maxlength=320, null=True, default='')
    user_banks: ReverseRelation['UserBank']
    data_collects: ReverseRelation['DataCollect']

    class Meta:
        table = "support_banks"

# ----------------------------------------------------------------------------------------------------------------------


class UserBank(Model):
    id = BigIntField(pk=True)
    user_id = CharField(max_length=100, index=True)
    support_bank: ForeignKeyRelation['SupportBank'] = ForeignKeyField('bank.SupportBank', on_delete=OnDelete.CASCADE,
                                                                      related_name="user_banks")
    payment_accounts: ReverseRelation['PaymentAccount']
    name = CharField(max_length=50)
    token = BinaryField()

    class Meta:
        table = "user_banks"


# ----------------------------------------------------------------------------------------------------------------------

class PaymentAccountStatus(IntEnum):
    active = 1
    close = 0


def get_start_current_year_date():
    return datetime(year=now().year, day=1, month=1)


class PaymentAccount(Model):
    id = BigIntField(pk=True)
    legal_entity_id = CharField(max_length=100, index=True)
    user_bank: ForeignKeyRelation['UserBank'] = ForeignKeyField('bank.UserBank', on_delete=OnDelete.CASCADE,
                                                                related_name="payment_accounts")
    data_collects: ReverseRelation['PaymentAccount']
    start_date = DateField(null=True, default=get_start_current_year_date)
    number = CharField(max_length=50, unique=True)
    balance = CharField(max_length=30, null=True, default="0")
    status = IntEnumField(enum_type=PaymentAccountStatus, description="Статус расчётного счета", default=1)

    class Meta:
        table = "payment_accounts"

# ----------------------------------------------------------------------------------------------------------------------


class DataCollectType(str, Enum):
    income = "Доход"
    cost = "Расход"


class DataCollect(Model):
    id = BigIntField(pk=True)
    payment_account: ForeignKeyRelation['PaymentAccount'] = ForeignKeyField('bank.PaymentAccount',
                                                                            on_delete=OnDelete.CASCADE,
                                                                            related_name="data_collects")
    support_bank: ForeignKeyRelation['SupportBank'] = ForeignKeyField('bank.SupportBank',
                                                                      on_delete=OnDelete.RESTRICT,
                                                                      related_name="data_collects")
    trxn_id = CharField(max_length=100, null=True)
    trxn_date = DateField(index=True)
    counterparty_name = CharField(max_length=100)
    counterparty_inn = CharField(max_length=30, default='', null=True)
    type = CharEnumField(enum_type=DataCollectType, description='Тип операции')
    amount = DecimalField(max_digits=19, decimal_places=2)

    class Meta:
        table = "data_collects"
