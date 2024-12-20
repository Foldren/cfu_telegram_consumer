from dataclasses import dataclass


@dataclass
class CreateCounterpartyRequest:
    __slots__ = {"userID", "name", "inn", "categoryID"}
    userID: str
    name: str
    inn: str
    categoryID: int | None


@dataclass
class UpdateCounterpartyRequest:
    counterpartyID: int
    userID: str
    categoryID: int | None = None
    name: str = None
    inn: str = None


@dataclass
class DeleteCounterpartiesRequest:
    __slots__ = {"counterpartiesID", "userID"}
    counterpartiesID: list[int]
    userID: str


@dataclass
class GetCounterpartiesRequest:
    userID: str
    showMode: str = 'distributed'









