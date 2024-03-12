from dataclasses import dataclass
from decimal import Decimal


@dataclass
class CCategory:
    __slots__ = {"id", "name", "status", "hasChildren"}
    id: int
    name: str
    status: bool
    hasChildren: bool


@dataclass
class CCounterparty:
    __slots__ = {"id", "name", "inn", "categoryID", "categoryName"}
    id: int
    name: str
    inn: str
    categoryID: int
    categoryName: str


@dataclass
class CBalanceResponse:
    __slots__ = {"balance", "currency"}
    balance: Decimal
    currency: str


@dataclass
class CExpensesResponse:
    __slots__ = {"cash", "nonCash"}
    cash: CBalanceResponse
    nonCash: CBalanceResponse


@dataclass
class CCashBalanceOnHandResponse:
    __slots__ = {"userID", "balance"}
    userID: str
    balance: CBalanceResponse


@dataclass
class CLinkerValue:
    __slots__ = {"currentValue", "prevValue"}
    currentValue: int
    prevValue: int


@dataclass
class CLinkerGetDashboardPnlExpenses:
    __slots__ = {"salary", "rent", "package", "anotherExpenses"}
    salary: CLinkerValue  # Зарплата
    rent: CLinkerValue  # Аренда
    package: CLinkerValue  # Упаковка
    anotherExpenses: CLinkerValue  # Прочие расходы
