from dataclasses import dataclass

from components.responses.children import DCategory


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





