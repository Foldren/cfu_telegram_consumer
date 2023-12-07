from dataclasses import dataclass


@dataclass
class CreateCategoryRequest:
    userID: str
    name: str
    level: int
    observersID: list[str] = None
    parentID: int = None


@dataclass
class UpdateCategoryRequest:
    id: int
    userID: str
    name: str = None
    observersID: list[str] = None
    status: bool = None


@dataclass
class DeleteCategoriesRequest:
    __slots__ = {"categoriesID", "userID"}
    categoriesID: list[int]
    userID: str


@dataclass
class GetCategoriesRequest:
    userID: str
    parentID: int = None






