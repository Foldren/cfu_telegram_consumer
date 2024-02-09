from dataclasses import dataclass
from components.responses.children import DCounterparty


@dataclass
class CreateCounterpartyResponse:
    __slots__ = {"id"}
    id: int


@dataclass
class UpdateCounterpartyResponse:
    __slots__ = {"id"}
    id: int


@dataclass
class DeleteCounterpartiesResponse:
    __slots__ = {"counterpartiesID"}
    counterpartiesID: list[int]


@dataclass
class GetCounterpartiesResponse:
    __slots__ = {"counterparties"}
    counterparties: list[DCounterparty]





