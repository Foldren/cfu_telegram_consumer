from dataclasses import dataclass
from components.responses.children import CDataCollectResponse


@dataclass
class GetDataCollectsResponse:
    __slots__ = {"data_collects"}
    data_collects: list[CDataCollectResponse]
