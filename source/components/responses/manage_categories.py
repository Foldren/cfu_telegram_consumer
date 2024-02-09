from dataclasses import dataclass
from components.responses.children import DCategory, DExpensesResponse, DCashBalanceOnHandResponse, DLowerCategory


@dataclass
class CreateCategoryResponse:
    __slots__ = {"id"}
    id: int


@dataclass
class UpdateCategoryResponse:
    __slots__ = {"id"}
    id: int


@dataclass
class DeleteCategoriesResponse:
    __slots__ = {"categoriesID"}
    categoriesID: list[int]


@dataclass
class GetCategoriesResponse:
    __slots__ = {"categories"}
    categories: list[DCategory]


@dataclass
class GetLowerCategoriesResponse:
    __slots__ = {"categories"}
    categories: list[DLowerCategory]


@dataclass
class ExpensesResponse:
    __slots__ = {"commodityCosts", "businessExpenses"}
    commodityCosts: DExpensesResponse
    businessExpenses: DExpensesResponse


@dataclass
class CashBalancesOnHandResponse:
    __slots__ = {"cashBalancesOnHand"}
    cashBalancesOnHand: list[DCashBalanceOnHandResponse]





