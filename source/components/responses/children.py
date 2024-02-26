from dataclasses import dataclass
from datetime import date
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
class CDataCollectResponse:
    __slots__ = {"legalEntityID", "categoryName", "amount", "date", "type"}
    legalEntityID: str
    categoryName: str
    amount: Decimal
    date: str
    type: str
