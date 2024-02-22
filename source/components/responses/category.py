from dataclasses import dataclass
from components.responses.children import CCategory, CExpensesResponse, CCashBalanceOnHandResponse


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
    categories: list[CCategory]


@dataclass
class ExpensesResponse:
    __slots__ = {"commodityCosts", "businessExpenses"}
    commodityCosts: CExpensesResponse
    businessExpenses: CExpensesResponse


@dataclass
class CashBalancesOnHandResponse:
    __slots__ = {"cashBalancesOnHand"}
    cashBalancesOnHand: list[CCashBalanceOnHandResponse]





