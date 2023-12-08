from dataclasses import dataclass


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
