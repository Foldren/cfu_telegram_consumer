from dataclasses import dataclass


@dataclass
class CashBalancesOnHandRequest:
    __slots__ = {"usersID", "legalEntitiesID"}
    usersID: list[str]
    legalEntitiesID: list[str]


@dataclass
class ExpensesRequest:
    __slots__ = {"dateFrom", "dateTo", "legalEntities", "userID"}
    dateFrom: str
    dateTo: str
    legalEntities: list[str]
    userID: str


@dataclass
class CreateCategoryRequest:
    userID: str
    name: str
    observersID: list[str] = None
    parentID: int = None


@dataclass
class UpdateCategoryRequest:
    categoryID: int
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






