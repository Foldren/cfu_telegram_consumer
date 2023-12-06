from dataclasses import dataclass


@dataclass
class CreateCategoryRequest:
    userID: str
    name: str
    level: int
    observersID: list[str] = None
    parentID: int = None





