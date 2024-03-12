from dataclasses import dataclass
from components.responses.children import CLinkerValue, CLinkerGetDashboardPnlExpenses


@dataclass
class LinkerGetDashboardPnlResponse:
    __slots__ = {"anotherRevenue", "expenses"}
    anotherRevenue: CLinkerValue  # Прочая выручка
    expenses: CLinkerGetDashboardPnlExpenses
