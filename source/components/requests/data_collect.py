from dataclasses import dataclass


@dataclass
class GetDataCollectsRequest:
    __slots__ = {"userID", "legalEntitiesID", "dateFrom", "dateTo"}
    userID: str
    legalEntitiesID: list[str]
    dateFrom: str
    dateTo: str
