from dataclasses import dataclass
from decimal import Decimal


@dataclass
class DCategory:
    __slots__ = {"id", "name", "status", "level"}
    id: int
    name: str
    status: bool
    level: int


@dataclass
class DCounterparty:
    __slots__ = {"id", "name", "inn", "categoryID", "categoryName"}
    id: int
    name: str
    inn: str
    categoryID: int
    categoryName: str


@dataclass
class DBalanceResponse:
    __slots__ = {"balance", "currency"}
    balance: Decimal
    currency: str


@dataclass
class DExpensesResponse:
    __slots__ = {"cash", "nonCash"}
    cash: DBalanceResponse
    nonCash: DBalanceResponse


@dataclass
class DCashBalanceOnHandResponse:
    __slots__ = {"userID", "balance"}
    userID: str
    balance: DBalanceResponse
