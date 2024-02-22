from dataclasses import dataclass


@dataclass
class GetDataCollectsRequest:
    __slots__ = {"userID", "legalEntities", "dateFrom", "dateTo"}
    userID: str
    legalEntities: list[str]
    dateFrom: str
    dateTo: str
