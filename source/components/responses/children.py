from dataclasses import dataclass


@dataclass
class DCategory:
    __slots__ = {"id", "name", "status", "level"}
    id: int
    name: str
    status: bool
    level: int
